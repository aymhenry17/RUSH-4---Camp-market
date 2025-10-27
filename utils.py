#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Set, Tuple

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import new_code_cell


def snapshot_files(directory: Path, exts: Tuple[str, ...]) -> Dict[Path, float]:
    """Capture l'état actuel des fichiers dans un répertoire."""
    snap: Dict[Path, float] = {}
    if not directory.exists():
        return snap
    for p in directory.iterdir():
        if p.is_file() and p.suffix.lower() in exts:
            snap[p] = p.stat().st_mtime
    return snap


def move_new_or_updated(
    src_dir: Path,
    dst_dir: Path,
    exts: Tuple[str, ...],
    before: Dict[Path, float],
    exclude_dirs: Set[Path] | None = None,
) -> None:
    """Déplace les fichiers nouveaux ou modifiés vers le dossier de destination."""
    exclude_dirs = exclude_dirs or set()
    dst_dir.mkdir(parents=True, exist_ok=True)
    if not src_dir.exists():
        return
    for p in src_dir.iterdir():
        if p.is_dir():
            if p in exclude_dirs:
                continue
            continue
        if p.suffix.lower() not in exts:
            continue
        mtime = p.stat().st_mtime
        if p not in before or mtime > before.get(p, 0):
            target = dst_dir / p.name
            counter = 1
            while target.exists():
                stem, suf = p.stem, p.suffix
                target = dst_dir / f"{stem}_{counter}{suf}"
                counter += 1
            try:
                shutil.move(str(p), str(target))
            except Exception:
                pass


def inject_matplotlib_capture_cell(nb, output_dir: Path) -> None:
    """Injecte une cellule pour capturer automatiquement les graphiques matplotlib avec des noms descriptifs."""
    code = r"""
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUTPUT_DIR = r"__OUTPUT_DIR__"
os.makedirs(OUTPUT_DIR, exist_ok=True)
_orig_show = plt.show
_counter = {'i': 0}
_saved = set()

def _sanitize_filename(name):
    # Nettoie le titre pour en faire un nom de fichier valide
    import re
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name.strip('_').lower()

def _save_all_figs():
    for num in list(plt.get_fignums()):
        fig = plt.figure(num)
        fid = id(fig)
        if fid in _saved:
            continue
        _counter['i'] += 1
        
        # Essayer de récupérer le titre du graphique
        title = ""
        if fig.axes:
            for ax in fig.axes:
                ax_title = ax.get_title()
                if ax_title:
                    title = ax_title
                    break
            if not title and hasattr(fig, '_suptitle') and fig._suptitle:
                title = fig._suptitle.get_text()
        
        # Créer un nom de fichier basé sur le titre ou un compteur
        if title:
            filename = f"{_sanitize_filename(title)}.jpg"
        else:
            filename = f"figure_{_counter['i']:03d}.jpg"
        
        path = os.path.join(OUTPUT_DIR, filename)
        
        # Gérer les doublons
        if os.path.exists(path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(OUTPUT_DIR, f"{base}_{counter}{ext}")):
                counter += 1
            path = os.path.join(OUTPUT_DIR, f"{base}_{counter}{ext}")
        
        try:
            fig.savefig(path, format='jpg', dpi=150, bbox_inches='tight')
            _saved.add(fid)
        except Exception:
            pass
        try:
            plt.close(fig)
        except Exception:
            pass

def _patched_show(*args, **kwargs):
    _save_all_figs()
    return _orig_show(*args, **kwargs)

plt.show = _patched_show
""".strip()
    code = code.replace("__OUTPUT_DIR__", str(output_dir))
    nb.cells.insert(0, new_code_cell(code))


def run_notebook(
    notebook_path: Path,
    output_dir: Path,
    executed_dir: Path,
    base_dir: Path
) -> None:
    """Exécute un notebook Jupyter et sauvegarde les résultats."""
    work_dir = notebook_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    before = snapshot_files(work_dir, (".jpg", ".csv"))

    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    inject_matplotlib_capture_cell(nb, output_dir)

    ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': str(work_dir)}})

    executed_path = executed_dir / f"{notebook_path.stem}__executed.ipynb"
    with open(executed_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    move_new_or_updated(work_dir, output_dir, (".jpg",), before, exclude_dirs={base_dir / "Data"})
    move_new_or_updated(work_dir, output_dir, (".csv",), before, exclude_dirs={base_dir / "Data"})


def run_script(
    script_path: Path,
    output_dir: Path,
    base_dir: Path
) -> None:
    """Exécute un script Python et sauvegarde les résultats."""
    work_dir = script_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    before = snapshot_files(work_dir, (".jpg", ".csv"))

    pycode = r"""
import os, runpy, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUTPUT_DIR = r"__OUTPUT_DIR__"
os.makedirs(OUTPUT_DIR, exist_ok=True)
_orig_show = plt.show
_counter = {'i': 0}
_saved = set()

def _save_all_figs():
    for num in list(plt.get_fignums()):
        fig = plt.figure(num)
        fid = id(fig)
        if fid in _saved:
            continue
        _counter['i'] += 1
        path = os.path.join(OUTPUT_DIR, f"figure_{_counter['i']:03d}.jpg")
        try:
            fig.savefig(path, format='jpg', dpi=150)
            _saved.add(fid)
        except Exception:
            pass
        try:
            plt.close(fig)
        except Exception:
            pass

def _patched_show(*args, **kwargs):
    _save_all_figs()
    return _orig_show(*args, **kwargs)

plt.show = _patched_show
runpy.run_path(r"__SCRIPT_PATH__", run_name='__main__')
"""
    pycode = pycode.replace("__OUTPUT_DIR__", str(output_dir)).replace("__SCRIPT_PATH__", str(script_path))

    env = os.environ.copy()
    env['MPLBACKEND'] = 'Agg'
    subprocess.run([sys.executable, "-c", pycode], cwd=str(work_dir), env=env, check=False)

    move_new_or_updated(work_dir, output_dir, (".jpg",), before, exclude_dirs={base_dir / "Data"})
    move_new_or_updated(work_dir, output_dir, (".csv",), before, exclude_dirs={base_dir / "Data"})

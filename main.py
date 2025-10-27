#!/usr/bin/env python3
from pathlib import Path
from utils import run_notebook, run_script


def main() -> None:
    """Point d'entrée principal pour exécuter tous les notebooks et scripts."""
    # Configuration des chemins
    BASE_DIR = Path(__file__).resolve().parent
    SCRIPTS_DIR = BASE_DIR / "Scripts"
    EXECUTED_DIR = BASE_DIR / "executed_notebooks"
    EXECUTED_DIR.mkdir(exist_ok=True)
    
    # Créer les dossiers de sortie
    for folder in ("KPI", "Segmentation", "Prédiction"):
        (BASE_DIR / folder).mkdir(exist_ok=True)
    
    # Liste des tâches à exécuter
    jobs = [
        # Cleaning
        (SCRIPTS_DIR / "Cleaning.ipynb", BASE_DIR / "Data"),
        # KPI
        (SCRIPTS_DIR / "KPI_mine.ipynb", BASE_DIR / "KPI"),
        (SCRIPTS_DIR / "RecentKPIs.ipynb", BASE_DIR / "KPI"),
        # Segmentation
        (SCRIPTS_DIR / "segmentation.ipynb", BASE_DIR / "Segmentation"),
        # Prédiction
        (SCRIPTS_DIR / "Partie 4 - prediction_model udapted.ipynb", BASE_DIR / "Prédiction"),
        (SCRIPTS_DIR / "Analyse exploratoire.ipynb", BASE_DIR / "Prédiction"),
    ]
    
    for path, out_dir in jobs:
        if not path.exists():
            print(f"⚠️ Fichier introuvable, ignoré: {path.name}")
            continue
        print(f"→ Exécution: {path.name}")
        if path.suffix.lower() == ".ipynb":
            run_notebook(path, out_dir, EXECUTED_DIR, BASE_DIR)
        elif path.suffix.lower() == ".py":
            run_script(path, out_dir, BASE_DIR)
        else:
            print(f"Type non supporté, ignoré: {path}")
    
    print("\n✅ Exécution terminée. Graphiques (JPG) et CSV déplacés dans les dossiers cibles.")


if __name__ == "__main__":
    main()

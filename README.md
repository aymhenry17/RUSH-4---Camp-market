# Camp Market - Analyse et Prédiction Client

Projet d'analyse de données marketing avec segmentation client, KPIs et modèles de prédiction.

##  Installation

### 1. Créer un environnement virtuel (recommandé)

python3 -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate     # Sur Windows

### 2. Installer les dépendances

pip install -r requirements.txt


## 📁 Structure du projet

Assurez-vous que votre projet respecte la structure suivante :

Placez vos fichiers CSV dans le dossier 
`Data/` : - `Camp_Market.csv`

RUSH-4---Camp-market/
│
├── main.py                          # ⭐ Script principal à exécuter
├── utils.py                         # Fonctions utilitaires
├── requirements.txt                 # Liste des dépendances
├── README.md                        # Ce fichier
│
├── Data/                            # 📊 Dossier contenant les datasets
│   ├── Camp_Market.csv              # Dataset brut
│   ├── Camp_Market_Cleaned.csv      # Dataset nettoyé
│   └── Camp_Market_Cleaned_Grade.csv # Dataset avec grades
│
├── Scripts/                         # 📓 Notebooks d'analyse
│   ├── Cleaning.ipynb               # Nettoyage des données
│   ├── KPI_mine.ipynb               # Analyse des KPIs principaux
│   ├── RecentKPIs.ipynb             # KPIs récents
│   ├── segmentation.ipynb           # Segmentation RFM
│   ├── Analyse exploratoire.ipynb   # Analyse exploratoire
│   └── Partie 4 - prediction_model udapted.ipynb  # Modèles de prédiction
│
├── KPI/                             # 📈 Sorties des analyses KPI
├── Segmentation/                    # 👥 Résultats de segmentation
├── Prédiction/                      # 🔮 Résultats de prédiction
└── executed_notebooks/              # 📔 Notebooks exécutés avec résultats

## ▶️ Utilisation

Exécutez le script principal qui lance automatiquement tous les notebooks :

python main.py

Le script exécutera dans l'ordre :
1. **KPI_mine.ipynb** et **RecentKPIs.ipynb** → Résultats dans `KPI/`
2. **segmentation.ipynb** → Résultats dans `Segmentation/`
3. **Partie 4 - prediction_model udapted.ipynb** et **Analyse exploratoire.ipynb** → Résultats dans `Prédiction/`

### Résultats générés

- **KPI/** : Graphiques d'analyse des KPIs et des canaux de vente
- **Segmentation/** : `customer_segmentation.csv`, `cluster_profiles.csv` et visualisations RFM
- **Prédiction/** : CSV de prédictions, courbes ROC, importance des variables
- **executed_notebooks/** : Notebooks exécutés avec leurs résultats

1. Préparation des données

Chargement du fichier Camp_Market_Cleaned.csv
Sélection et nettoyage des variables pertinentes
Construction des indicateurs RFM :

Recency : date du dernier achat (Last_Purchase)
Frequency : nombre total d’achats (Total_Purchases)
Monetary : montant total dépensé (Total_Spent)

Standardisation des variables pour garantir leur comparabilité

2. Clustering (segmentation)

Utilisation de l’algorithme K-Means pour regrouper les clients selon leurs comportements.
Détermination du nombre optimal de clusters à l’aide de :

la méthode du coude (Elbow method)
le score de silhouette

Attribution d’un cluster à chaque client.

3. Analyse et interprétation

Calcul des moyennes principales (âge, revenu, dépenses, fréquence, taille du foyer) pour décrire chaque segment.

Création de visualisations :

Graphique 3D RFM (Recency, Frequency, Monetary)
Boxplots et Pairplots pour comparer les groupes

Interprétation de chaque cluster selon son comportement d’achat :

Clients premium (forte dépense et fréquence)
Clients fidèles modérés
Clients occasionnels
Clients inactifs / récents

4. Livrables

Deux fichiers sont générés à la fin de l’analyse :

customer_segmentation.csv
Contient chaque client avec son cluster associé et ses caractéristiques principales.

cluster_profiles.csv
Résume le profil moyen de chaque segment (âge, revenu, dépenses, etc.).

🧠 Résultats attendus

Une segmentation claire et justifiée des clients.
Une meilleure compréhension des comportements d’achat.
Des recommandations marketing basées sur des données concrètes (fidélisation, réactivation, ciblage).
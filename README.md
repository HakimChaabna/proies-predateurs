# Simulation proies-prédateurs

Simulation d'un écosystème proies-prédateurs sur grille, inspirée du jeu de la vie de Conway.

L'objectif est de voir dans quelle mesure la traduction directe de comportements observés dans la réalité — sans modèle mathématique type Lotka-Volterra — peut reproduire les dynamiques de population réelles.

## Fichiers

| Fichier | Description |
|---------|-------------|
| `simulation.py` | Simulation sur grille 50×50 avec règles comportementales (chasse, déplacement, reproduction, mortalité) |
| `réel.py` | Visualisation des données de l'Isle Royale (1980–2019), loups et orignaux |

## Données

Les données réelles proviennent du programme de recherche [Wolves and Moose of Isle Royale](https://isleroyalewolf.org/) — 60 ans de suivi continu sur une île isolée du lac Supérieur (Michigan).

## À venir

- Algorithme génétique pour calibrer automatiquement les paramètres de la simulation contre les données réelles
- Moyennage statistique sur plusieurs runs
- Exploration de paramètres adaptatifs

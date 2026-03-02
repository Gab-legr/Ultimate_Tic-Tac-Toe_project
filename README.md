# Ultimate_Tic-Tac-Toe_project
Built a Pokémon-themed Ultimate Tic-Tac-Toe game in Python (OOP + Tkinter), where each move is won through turn-based Pokémon battles. Implemented and optimized a Minimax AI (with pruning/memoization) for solo play, balancing grid strategy, combat logic, and real-time GUI performance.

# Ultimate_Tic-Tac-Toe_project

Built a Pokémon-themed Ultimate Tic-Tac-Toe game in Python (OOP + Tkinter), where each move is won through turn-based Pokémon battles. Implemented and optimized a Minimax AI (with pruning/memoization) for solo play, balancing grid strategy, combat logic, and real-time GUI performance.

### EN

A Python Ultimate Tic-Tac-Toe game where each cell is won through a Pokémon battle, featuring a GUI and a Minimax-based AI.

### Project Overview

This project is a custom Ultimate Tic-Tac-Toe game with a Pokémon-inspired twist: each board cell is contested through a Pokémon battle.

The goal remains the same (win by alignment), but to capture an occupied cell, the player must defeat the opponent’s Pokémon in a turn-based duel. The game therefore combines:

- board strategy (alignment planning, forced mini-board rule),
- combat management (stats, types, damage, leveling),
- tactical choices (which Pokémon to play, when to challenge a contested cell).

The result is a hybrid experience: strategy game + battle system, with both layers constantly interacting.

---

## Main Features

- Ultimate Tic-Tac-Toe (9 mini-boards)
- Pokémon battles to capture cells
- Type effectiveness system (resistances / immunities / bonuses)
- Interactive GUI (board rendering, highlights, Pokémon info)
- Multiple game modes:
  - Player vs Player
  - Player vs AI
  - AI vs AI
- Minimax-based AI (advanced mode)
- Pokémon data loading from CSV
- Pokémon image retrieval via API (with local caching)

---

## Technical Architecture (Python, OOP)

The game was built from scratch in Python using a clear object-oriented architecture to separate game flow, board logic, combat logic, players, and GUI concerns.

### Main classes

- `Partie`: game orchestration (menu, rendering, loop, setup)
- `Plateau`: main Ultimate Tic-Tac-Toe board
- `MiniPlateau`: 3x3 sub-board
- `Case`: individual cell
- `Pokemon`: stats, type, damage, battles, info display
- `Joueur`: human player logic (cell + Pokémon selection)
- `IA`: random AI
- `IA_minimax`: advanced AI using a simplified Minimax approach

---

## Graphical Interface

The project includes an interactive GUI (grid rendering, click handling, highlights, Pokémon images, combat messages), making the game more intuitive and engaging.

The interface handles:

- game mode selection,
- Ultimate Tic-Tac-Toe board rendering,
- valid move highlighting,
- available Pokémon display,
- combat result messages.

---

## Pokémon Battle System

Each Pokémon has: HP, Attack, Defense, Speed, Type.

Damage is computed using:

- Pokémon stats,
- a damage formula,
- a type multiplier (attack effectiveness against defender type).

The battle system supports:

- wins / losses / draws,
- board-cell updates after combat,
- Pokémon leveling after battles.

---

## AI and Minimax Logic

The project includes an advanced AI based on Minimax, which evaluates possible moves by simulating future board states.

### What the Minimax AI does

- generates legal actions,
- simulates future board states,
- evaluates positions (win/loss/draw + intermediate heuristic),
- selects the move that maximizes its chances of winning.

---

## Current Limitations

- Minimax simplifies some Pokémon battle aspects in its simulations
- The code is monolithic (single file) and can be refactored
- Depends on external files/assets and `tkiteasy`

---

## Future Improvements

- Split the code into modules (`game/`, `ai/`, `gui/`, `models/`)
- Add alpha-beta pruning for faster Minimax
- Simulate Pokémon battles more accurately inside Minimax
- Add save/load game support
- Add battle history / statistics screen
- Add unit tests

---

## Skills Demonstrated

- Python (object-oriented programming)
- GUI programming
- Complex game-system design
- Game AI (Minimax)
- State management / simulation
- API and external data integration

---

### FR

Un Ultimate Tic-Tac-Toe en Python où chaque case se gagne via un duel Pokémon, avec interface graphique et IA Minimax.

## Pokémon Ultimate Tic-Tac-Toe (Python)

### Présentation du projet

Ce projet est une réinvention du morpion (Ultimate Tic-Tac-Toe) avec une mécanique inspirée de Pokémon : chaque case de la grille se dispute via un mini-combat Pokémon.

L’objectif reste de gagner au morpion (aligner 3 cases), mais pour capturer une case occupée, le joueur doit vaincre le Pokémon adverse dans un duel au tour par tour. Le jeu combine donc :

- stratégie de plateau (anticiper les alignements, gérer le mini-plateau imposé),
- gestion de combat (stats, types, dégâts, niveau),
- choix tactiques (quel Pokémon jouer, quand attaquer une case contestée).

Cela crée un gameplay hybride : un jeu de stratégie + un système de combat, qui s’influencent en permanence.

---

## Fonctionnalités principales

- Ultimate Tic-Tac-Toe (grille de 9 mini-plateaux)
- Combats Pokémon pour gagner les cases
- Système de types (efficacité / résistances / immunités)
- Interface graphique interactive (plateau, surbrillance, infos Pokémon)
- Plusieurs modes de jeu :
  - Joueur vs Joueur
  - Joueur vs IA
  - IA vs IA
- IA Minimax (mode avancé) pour le mode solo / démonstration
- Chargement de données Pokémon depuis un fichier CSV
- Récupération d’images Pokémon via API (avec cache local)

---

## Architecture technique (Python, orientée objet)

Le jeu a été développé from scratch en Python avec une architecture orientée objet claire, afin de séparer la logique du jeu, les combats, les joueurs et l’interface graphique.

### Principales classes

- `Partie` : orchestre la partie (menu, affichage, boucle de jeu, initialisation)
- `Plateau` : plateau principal (Ultimate Tic-Tac-Toe)
- `MiniPlateau` : sous-grille 3x3
- `Case` : case individuelle d’un mini-plateau
- `Pokemon` : stats, type, dégâts, combats, affichage d’informations
- `Joueur` : logique de sélection (case + Pokémon)
- `IA` : IA aléatoire
- `IA_minimax` : IA avancée utilisant Minimax (version simplifiée)

---

## Interface graphique

Le projet propose une interface graphique interactive (grille, clics, surbrillances, images Pokémon, infos de combat), ce qui rend le jeu plus immersif et plus facile à prendre en main.

L’interface gère notamment :

- la sélection des modes de jeu,
- l’affichage de la grille Ultimate Tic-Tac-Toe,
- la sélection visuelle des cases autorisées,
- l’affichage des Pokémon disponibles,
- les messages de résultat des combats.

---

## Système de combat Pokémon

Chaque Pokémon possède :

- des points de vie (HP),
- une attaque,
- une défense,
- une vitesse,
- un type.

Les dégâts sont calculés à partir :

- des statistiques des Pokémon,
- d’une formule de dégâts,
- d’un multiplicateur de type (efficacité de l’attaque selon le type adverse).

Le système inclut :

- victoires / défaites / égalités,
- mise à jour de la case (capturée, libérée, conservée),
- progression de niveau des Pokémon après combat.

---

## IA et logique Minimax

Le projet inclut une IA avancée basée sur Minimax pour choisir les coups en anticipant plusieurs tours à l’avance.

### Ce que fait l’IA Minimax

- génère les actions possibles,
- simule les états suivants du plateau,
- évalue les positions (victoire/défaite/nul + heuristique intermédiaire),
- choisit l’action maximisant ses chances de gain.

---

## Défis techniques rencontrés

- Gérer un cycle de jeu hybride (plateau + combats Pokémon)
- Synchroniser logique de jeu et interface graphique
- Limiter le temps de calcul de l’IA (Minimax)
- Concevoir une architecture OOP claire et extensible
- Intégrer des données externes (CSV + API images)

---

## Limites actuelles

- L’IA Minimax simplifie certains aspects des combats Pokémon dans ses simulations
- Le script est monolithique (tout dans un seul fichier) et peut être refactorisé
- Dépendance à des fichiers/images externes et à `tkiteasy`

---

## Améliorations futures

- Séparer le code en modules (`game/`, `ai/`, `gui/`, `models/`)
- Ajouter alpha-beta pruning pour accélérer Minimax
- Ajouter une vraie simulation des combats dans l’IA Minimax
- Ajouter sauvegarde/chargement de partie
- Ajouter écran de stats / historique des combats
- Ajouter tests unitaires

---

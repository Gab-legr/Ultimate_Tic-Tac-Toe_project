import random
import pandas as pds
import numpy as np
# import tkinter as tk
from tkiteasy import *
import requests
from PIL import Image
from io import BytesIO
from tkinter import PhotoImage
import os.path
import copy
import os

NB_POKEMONS = 60
TAILLE = 900
taille_case = (TAILLE // 2) // 9
taille_mini_plateau = (TAILLE // 2) // 3

# Dictionnaire d'efficacité d'un type contre un autre
# la clé correspond au type d'attaque
# la valeur associée est un sous dictionnaire : la clé est le type défensif
# la valeur est le coefficient indiquant l'efficacité de l'attaque
# 0 correspond à une attaque inefficace
# O,5 à une attaque peu efficace
# 1 à une attaque neutre
# 2 à une attaque très efficace (multiplie par 2 les dégats infligés)

type = {
    "Normal": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1, "Fighting": 1,
               "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0,
               "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 1},

    "Fire": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 1, "Grass": 2, "Ice": 2, "Fighting": 1,
             "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1,
             "Dragon": 0.5, "Dark": 1, "Steel": 2, "Fairy": 1},

    "Water": {"Normal": 1, "Fire": 2, "Water": 0.5, "Electric": 1, "Grass": 0.5, "Ice": 1, "Fighting": 1,
              "Poison": 1, "Ground": 2, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1,
              "Dragon": 0.5, "Dark": 1, "Steel": 1, "Fairy": 1},

    "Electric": {"Normal": 1, "Fire": 1, "Water": 2, "Electric": 0.5, "Grass": 0.5, "Ice": 1, "Fighting": 1,
                 "Poison": 1, "Ground": 0, "Flying": 2, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1,
                 "Dragon": 0.5, "Dark": 1, "Steel": 1, "Fairy": 1},

    "Grass": {"Normal": 1, "Fire": 0.5, "Water": 2, "Electric": 1, "Grass": 0.5, "Ice": 1, "Fighting": 1,
              "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1,
              "Dragon": 0.5, "Dark": 1, "Steel": 0.5, "Fairy": 1},

    "Ice": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 1, "Grass": 2, "Ice": 0.5, "Fighting": 1,
            "Poison": 1, "Ground": 2, "Flying": 2, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1,
            "Dragon": 2, "Dark": 1, "Steel": 0.5, "Fairy": 1},

    "Fighting": {"Normal": 2, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 2, "Fighting": 1,
                 "Poison": 0.5, "Ground": 1, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2,
                 "Ghost": 0, "Dragon": 1, "Dark": 2, "Steel": 2, "Fairy": 0.5},

    "Poison": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 2, "Ice": 1, "Fighting": 1,
               "Poison": 0.5, "Ground": 0.5, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0.5,
               "Dragon": 1, "Dark": 1, "Steel": 0, "Fairy": 2},

    "Ground": {"Normal": 1, "Fire": 2, "Water": 1, "Electric": 2, "Grass": 0.5, "Ice": 1, "Fighting": 1,
               "Poison": 2, "Ground": 1, "Flying": 0, "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1,
               "Dragon": 1, "Dark": 1, "Steel": 2, "Fairy": 1},

    "Flying": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 0.5, "Grass": 2, "Ice": 1, "Fighting": 2,
               "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1,
               "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 1},

    "Psychic": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1, "Fighting": 2,
                "Poison": 2, "Ground": 1, "Flying": 1, "Psychic": 0.5, "Bug": 1, "Rock": 1, "Ghost": 1,
                "Dragon": 1, "Dark": 0, "Steel": 0.5, "Fairy": 1},

    "Bug": {"Normal": 1, "Fire": 0.5, "Water": 1, "Electric": 1, "Grass": 2, "Ice": 1, "Fighting": 0.5,
            "Poison": 0.5, "Ground": 1, "Flying": 0.5, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 0.5,
            "Dragon": 1, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},

    "Rock": {"Normal": 1, "Fire": 2, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 2, "Fighting": 0.5,
             "Poison": 1, "Ground": 0.5, "Flying": 2, "Psychic": 1, "Bug": 2, "Rock": 1, "Ghost": 1,
             "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 1},

    "Ghost": {"Normal": 0, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1, "Fighting": 1,
              "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2,
              "Dragon": 1, "Dark": 0.5, "Steel": 1, "Fairy": 1},

    "Dragon": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1, "Fighting": 1,
               "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1,
               "Dragon": 2, "Dark": 1, "Steel": 0.5, "Fairy": 0},

    "Dark": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1, "Fighting": 0.5,
             "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2,
             "Dragon": 1, "Dark": 0.5, "Steel": 1, "Fairy": 0.5},

    "Steel": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Grass": 1, "Ice": 2, "Fighting": 1,
              "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1,
              "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 2},

    "Fairy": {"Normal": 1, "Fire": 0.5, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1, "Fighting": 2,
              "Poison": 0.5, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1,
              "Dragon": 2, "Dark": 2, "Steel": 0.5, "Fairy": 1}
}


class Morpion():
    def __init__(self, case):
        self.type_case = case
        self.morpion = [[self.type_case(j, i, self) for i in range(3)] for j in range(3)]
        self.gagnant = None
        self.morpion_impose = None

    def afficherCase(self, l, c):
        pass

    def afficherPlateau(self):
        print("\nPlateau :")
        for lm in range(3):
            for l in range(3):
                for cm in range(3):
                    for c in range(3):
                        self.morpion[lm][cm].afficherCase(l, c)
                    print("|", end="")

                print("\n")
            print("-" * 34 * 3)

    # Fonction qui teste si le morpion est gagné ou non
    def estGagne(self):
        # On vérifie les lignes
        for ligne in self.morpion:
            # Un morpion est gagné si les 3 pokemons appartiennent au même joueur (on vérifie avec l'id du joueur)
            if ligne[0].valeur is not None and ligne[1].valeur is not None and ligne[2].valeur is not None:
                if ligne[0].valeur.joueur.id == ligne[1].valeur.joueur.id and ligne[1].valeur.joueur.id == ligne[
                    2].valeur.joueur.id:
                    return ligne[0].valeur.joueur

        # On vérifie les colonnes
        for c in range(3):
            if self.morpion[0][c].valeur is not None and self.morpion[1][c].valeur is not None and self.morpion[2][
                c].valeur is not None:
                if self.morpion[0][c].valeur != None and self.morpion[0][c].valeur.joueur.id == self.morpion[1][
                    c].valeur.joueur.id and \
                        self.morpion[1][c].valeur.joueur.id == self.morpion[2][c].valeur.joueur.id:
                    return self.morpion[1][c].valeur.joueur

        # On vérifie les diagonales
        if self.morpion[0][0].valeur is not None and self.morpion[1][1].valeur is not None and self.morpion[2][
            2].valeur is not None:
            if self.morpion[0][0].valeur != None and self.morpion[0][0].valeur.joueur.id == self.morpion[1][
                1].valeur.joueur.id and \
                    self.morpion[1][1].valeur.joueur.id == self.morpion[2][2].valeur.joueur.id:
                return self.morpion[1][1].valeur.joueur

        if self.morpion[2][0].valeur is not None and self.morpion[1][1].valeur is not None and self.morpion[0][
            2].valeur is not None:
            if self.morpion[2][0].valeur != None and self.morpion[2][0].valeur.joueur.id == self.morpion[1][
                1].valeur.joueur.id and \
                    self.morpion[1][1].valeur.joueur.id == self.morpion[0][2].valeur.joueur.id:
                return self.morpion[1][1].valeur.joueur

        # Sinon aucun gagnant
        return None

    # Fonction qui permet de faire jouer le joueur
    def tourDeJeu2(self, joueur):
        # Supprime le texte de l'issue du combat si besoin
        if jeu.resultat_combat is not None:
            jeu.g.pause(1)
            jeu.g.supprimer(jeu.resultat_combat)
            jeu.resultat_combat = None

        #self.afficherPlateau()
        
        # Choix de la case
        if self.morpion_impose:
            self.morpion[self.morpion_impose[0]][self.morpion_impose[1]].surligner()
        ligne_morpion, colonne_morpion, ligne_case, colonne_case = joueur.obtenirCase()
        if self.morpion_impose:
            self.morpion[self.morpion_impose[0]][self.morpion_impose[1]].supprimerSurligner()

        while not self.verifierCaseValide(
                self.morpion[ligne_morpion][colonne_morpion].morpion[ligne_case][colonne_case], joueur):
            ligne_morpion, colonne_morpion, ligne_case, colonne_case = joueur.obtenirCase()
        self.morpion[ligne_morpion][colonne_morpion].morpion[ligne_case][colonne_case].surligner()

        # Si la case est déjà occupée par un pokemon on affiche les infos du poke deja present
        if not self.morpion[ligne_morpion][colonne_morpion].morpion[ligne_case][colonne_case].estVide():
            self.morpion[ligne_morpion][colonne_morpion].morpion[ligne_case][
                colonne_case].valeur.afficherInfoDefenseur()

        # Choix du pokemon
        pokemon = joueur.choisirPokemon()
        pokemon.entrerCase(self.morpion[ligne_morpion][colonne_morpion].morpion[ligne_case][colonne_case])

        self.morpion[ligne_morpion][colonne_morpion].morpion[ligne_case][colonne_case].supprimerSurligner()

        gagnant_mini_plateau = self.morpion[ligne_morpion][colonne_morpion].determinerGagnant()
        if gagnant_mini_plateau:
            self.morpion[ligne_morpion][colonne_morpion].valeur = pokemon
            self.morpion[ligne_morpion][colonne_morpion].dessinerSymbole(gagnant_mini_plateau.symbole)
            self.morpion[ligne_morpion][colonne_morpion].effacerMiniPlateau()

        # Détermine le prochain mini-plateau imposé
        self.morpion_impose = (ligne_case, colonne_case)
        if self.morpion[self.morpion_impose[0]][self.morpion_impose[1]].verifierMiniPlateauTermine() :
            self.morpion_impose = None
        jeu.plateau.joueurs[joueur.id].tours += 1
        #self.afficherPlateau()

    # Fonction qui vérifie que le joueur joue dans une case autorisée
    def verifierCaseValide(self, case, joueur):
        # Vérifie que le joueur joue dans le morpion qui lui est imposé
        if self.morpion_impose and not self.morpion[self.morpion_impose[0]][
            self.morpion_impose[1]].verifierMiniPlateauTermine():
            if (case.parent.ligne, case.parent.colonne) != self.morpion_impose:
                print("Veuillez jouer dans le bon morpion")
                return False

        # Vérifie que le mini-plateau n'est pas terminé
        if self.morpion[case.parent.ligne][case.parent.colonne].verifierMiniPlateauTermine():
            print("Le morpion est déjà complet")
            return False

        # Vérifie que la case n'est pas déjà remportée par un joueur
        if self.morpion[case.parent.ligne][case.parent.colonne].morpion[case.ligne][case.colonne].deja_win:
            print("La case a déjà été remportée par l'adversaire")
            return False

        # Vérifie que si la case est occupée, ce n'est pas par son propre pokemon
        if self.morpion[case.parent.ligne][case.parent.colonne].morpion[case.ligne][case.colonne].valeur:
            if self.morpion[case.parent.ligne][case.parent.colonne].morpion[case.ligne][
                case.colonne].valeur.joueur.id == joueur.id:
                print("Cette case est déjà occupée par un de tes pokemons")
                return False

        return True

    # Fonction qui vérifie si tous les morpions sont terminés
    def verifierPartieTerminee(self):
        for l in range(3):
            for c in range(3):
                if not self.morpion[l][c].verifierMiniPlateauTermine():
                    return False

        print("La partie est terminée")
        return True


class Plateau(Morpion):
    def __init__(self):
        # Construit un morpion avec des mini plateaux en guise de cases
        super().__init__(MiniPlateau)
        self.complet = False
        self.joueurs = [Joueur(0, "Joueur 1", "X"), Joueur(1, "Joueur 2", "O")]

    def testerEgalite(self):
        gagnant = self.joueurs[0]
        for joueur in self.joueurs[1:]:
            if joueur.nombre_mini_win > gagnant.nombre_mini_win:
                gagnant = joueur
            elif joueur.nombre_mini_win == gagnant.nombre_mini_win:
                print("Il y a égalité")

        return gagnant


class MiniPlateau(Morpion):
    def __init__(self, ligne, colonne, parent):
        # Construit un morpion avec des cases
        super().__init__(Case)
        self.gagnant = None  # Objet joueur
        self.valeur = None  # Objet Pokemon
        self.colonne = colonne  # [0,1,2]
        self.ligne = ligne  # [0,1,2]
        self.parent = parent  # Objet Morpion

    def afficherCase(self, l, c):
        self.morpion[l][c].afficherValeur()

    # Fonction qui vérifie si le mini plateau est terminé
    def verifierMiniPlateauTermine(self):
        # Si il est gagné par un joueur
        if self.estGagne():
            return True
        # Ou si toutes les cases sont déjà remportées
        for l in range(3):
            for c in range(3):
                if self.morpion[l][c].estVide() or not self.morpion[l][c].deja_win:
                    return False
        print("Mini Plateau terminé")
        return True

    def determinerGagnant(self):
        if self.estGagne():
            self.gagnant = self.estGagne()
            print(f"{self.gagnant.nom} a gagné un mini morpion")
            self.gagnant.nombre_mini_win += 1
        return self.gagnant

    # Fonction qui dessine un gros symbole X ou O sur le mini plateau remporté
    def dessinerSymbole(self, symbole):
        x = TAILLE // 4 + self.colonne * taille_mini_plateau + taille_mini_plateau // 2
        y = TAILLE // 4 + self.ligne * taille_mini_plateau + taille_mini_plateau // 2

        if symbole == "X":
            jeu.g.afficherTexte("X", x, y, "red", 120)
        elif symbole == "O":
            jeu.g.afficherTexte("O", x, y, "blue", 120)

    # Fonction qui efface tout le graphique sur un mini plateau remporté
    def effacerMiniPlateau(self):
        for l in range(3):
            for c in range(3):
                if self.morpion[l][c].contenu:
                    self.morpion[l][c].effacerSymbole()
                if self.morpion[l][c].texte_poke:
                    self.morpion[l][c].effacerTexte()

    # Fonction qui surligne le mini plateau imposé
    def surligner(self):
        x1 = self.colonne * taille_mini_plateau + TAILLE // 4
        y1 = self.ligne * taille_mini_plateau + TAILLE // 4

        x2 = x1 + taille_mini_plateau
        y2 = y1 + taille_mini_plateau

        l1 = jeu.g.dessinerLigne(x1, y1, x2, y1, "yellow", 3)
        l2 = jeu.g.dessinerLigne(x1, y2, x2, y2, "yellow", 3)
        l3 = jeu.g.dessinerLigne(x1, y1, x1, y2, "yellow", 3)
        l4 = jeu.g.dessinerLigne(x2, y1, x2, y2, "yellow", 3)
        self.ligne_mini_plateau = {l1, l2, l3, l4}

    def supprimerSurligner(self):
        for ligne in self.ligne_mini_plateau:
            jeu.g.supprimer(ligne)


class Case():
    def __init__(self, ligne, colonne, parent):
        self.valeur = None  # Correspond à un objet pokemon
        self.deja_win = None
        self.ligne = ligne  # [0,1,2]
        self.colonne = colonne  # [0,1,2]
        self.parent = parent  # Objet Mini Plateau
        self.contenu = None  # Texte graphique X ou O
        self.texte_poke = None  # Texte graphique nom du pokemon

    def estVide(self):
        if self.valeur == None:
            return True

        return False

    def afficherValeur(self):
        if self.valeur == None:
            valeur = "Vide"
        else:
            valeur = self.valeur.joueur.nom
        print(f"{valeur:^10}", end="|")

    def dessinerSymbole(self, symbole, pokemon):
        x = TAILLE // 4 + self.parent.colonne * taille_mini_plateau + self.colonne * taille_case + taille_case // 2
        y = TAILLE // 4 + self.parent.ligne * taille_mini_plateau + self.ligne * taille_case + taille_case // 2
        if symbole == "X":
            self.contenu = jeu.g.afficherTexte("X", x, y, "red", 40)
        elif symbole == "O":
            self.contenu = jeu.g.afficherTexte("O", x, y, "blue", 40)

        if not self.deja_win:
            self.texte_poke = jeu.g.afficherTexte(pokemon.nom, x, y + 20, "white", 7)

    def effacerSymbole(self):
        jeu.g.supprimer(self.contenu)
        self.contenu = None

    def effacerTexte(self):
        jeu.g.supprimer(self.texte_poke)
        self.texte_poke = None

    def surligner(self):
        # Coordonnées dans le mini morpion
        x1 = self.colonne * taille_case + self.parent.colonne * taille_mini_plateau + TAILLE // 4
        y1 = self.ligne * taille_case + self.parent.ligne * taille_mini_plateau + TAILLE // 4

        x2 = x1 + taille_case
        y2 = y1 + taille_case

        l1 = jeu.g.dessinerLigne(x1, y1, x2, y1, "yellow", 3)
        l2 = jeu.g.dessinerLigne(x1, y2, x2, y2, "yellow", 3)
        l3 = jeu.g.dessinerLigne(x1, y1, x1, y2, "yellow", 3)
        l4 = jeu.g.dessinerLigne(x2, y1, x2, y2, "yellow", 3)
        self.ligne_case = {l1, l2, l3, l4}

    def supprimerSurligner(self):
        for ligne in self.ligne_case:
            jeu.g.supprimer(ligne)


class Partie():
    def __init__(self):
        self.plateau = Plateau()
        self.pokemons = set()
        self.g = ouvrirFenetre(TAILLE, TAILLE)
        self.pokemon_img = {}  # Dictionnaire avec en clé une image et en valeur l'objet pokemon
        self.tour = None
        self.resultat_combat = None

    # Fonction qui a permis d'enlever les pokemons du DataFrame dont Mega faisait parti du nom
    # Pour permettre de récupérer une image pour tous les pokemons
    # N'est plus appelée dans le programme
    def filtrerMegaPokemon(self):
        df = pds.read_csv("pokemon.csv")
        df_filtre = df.loc[df["Name"].apply(lambda x: "Mega" not in str(x))]
        df_filtre.to_csv("pokemon_filtre.csv", index=False)

    def initMenu(self):
        self.fond1 = self.g.afficherImage(0, 0, "./images/Fond_Ultimate.jpg", TAILLE, TAILLE)

        l = TAILLE / 3.5  # largeur des touches rectangles
        h = TAILLE / 15  # hauteur des touches rectangles

        t1 = self.g.dessinerRectangle(TAILLE / 3 - (l / 2), TAILLE / 2 - (h / 2), l, h, "black")
        t2 = self.g.dessinerRectangle(2 * TAILLE / 3 - (l / 2), TAILLE / 2 - (h / 2), l, h, "black")
        t3 = self.g.dessinerRectangle((TAILLE - l) / 2, 3 * TAILLE / 4 - (h / 2), l, h, "black")

        ia = self.g.afficherTexte("Joueur VS IA", 2 * TAILLE / 3, TAILLE / 2, "white", int(3 * TAILLE / 100))
        joueur = self.g.afficherTexte("Joueur VS Joueur", TAILLE / 3, TAILLE / 2, "white", int(3 * TAILLE / 100))
        deuxia = self.g.afficherTexte("IA VS IA", TAILLE / 2, 3 * TAILLE / 4, "white", int(3 * TAILLE / 100))

        self.touche = {t1: 1, t2: 2, t3: 3, joueur: 1, ia: 2, deuxia: 3}

    # Cette fonction efface le menu graphique
    def viderMenu(self):
        self.g.supprimer(self.fond1)
        for obj in self.touche:
            self.g.supprimer(obj)

    # Cette fonction permet de choisir le mode de jeu
    def selectionerModeJeu(self):
        clic = self.g.attendreClic()
        obj = self.g.recupererObjet(clic.x, clic.y)

        while obj not in self.touche:
            clic = self.g.attendreClic()
            obj = self.g.recupererObjet(clic.x, clic.y)

        self.viderMenu()

        if self.touche[obj] == 1:
            self.plateau.joueurs = [Joueur(0, "Joueur 1", "X"), Joueur(1, "Joueur 2", "O")]
        if self.touche[obj] == 2:
            self.plateau.joueurs = [Joueur(0, "Joueur", "O"), IA(1, "IA Aléatoire", "X")]
        if self.touche[obj] == 3:
            self.plateau.joueurs = [IA(0, "IA aléatoire", "X"), IA_minimax(1, "IA avancée", "O")]

    def dessinerGrille(self):
        self.fond2 = self.g.afficherImage(0, 0, "./images/Fond_jeu2.jpg", TAILLE, TAILLE)
        marge = (TAILLE - TAILLE // 2) // 2

        for i in range(0, 10):
            if i % 3 == 0:
                epaisseur = 3
            else:
                epaisseur = 1
            self.g.dessinerLigne(TAILLE // 4, i * taille_case + TAILLE // 4, 3 * TAILLE // 4,
                                 i * taille_case + TAILLE // 4, "black", epaisseur)
            self.g.dessinerLigne(i * taille_case + TAILLE // 4, TAILLE // 4, i * taille_case + TAILLE // 4,
                                 3 * TAILLE // 4, "black", epaisseur)


    def repartirPokemons(self):
        df = pds.read_csv("pokemon_filtre.csv")
        # Copie pour ne pas modifier le data frame original
        df_normalise = df.copy()

        # On homogénéise les caractéristiques en divisant par leur max
        for colonne in ["HP", "Attack", "Defense", "Speed"]:
            valeur_max = df[colonne].max()
            df_normalise[colonne] = df[colonne] / valeur_max

        # Ajout d'une colonne Norme (euclidienne) au data frame
        df_normalise["Norme"] = np.sqrt(
            df_normalise["HP"] ** 2 + df_normalise["Attack"] ** 2 + df_normalise["Defense"] ** 2 + df_normalise[
                "Speed"] ** 2)
        # On trie par ordre décroissant
        df_trie = df_normalise.sort_values(by="Norme", ascending=False)
        print(df_trie[['Name', 'HP', 'Attack', 'Defense', 'Speed', 'Norme']])

        for i in range(NB_POKEMONS * 2):
            pokemon = Pokemon(df_trie.loc[i, "Name"], df.loc[i, "Type 1"], df.loc[i, "HP"], df.loc[i, "Attack"], # Erreur dans la selection des pokemons
                              df.loc[i, "Defense"], df.loc[i, "Speed"])
            # On attribue 1 pokemon sur 2 aux joueurs pour que les caractéristiques soient équilibrées
            if i % 2 == 0:
                self.plateau.joueurs[0].pokemons.add(pokemon)
                pokemon.joueur = self.plateau.joueurs[0]

            if i % 2 == 1:
                self.plateau.joueurs[1].pokemons.add(pokemon)
                pokemon.joueur = self.plateau.joueurs[1]

        # for joueur in self.plateau.joueurs :
        #     joueur.calculerMoyenne()

    def recupererImagePoke(self, pokemon):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.nom.lower().split()[0]}"
        nom_fichier = f"./images/{pokemon.nom}.png"
        print(f"{url} -> {nom_fichier}")
        if not os.path.isfile(nom_fichier):
            try:
                reponse = requests.get(url)
                donnee = reponse.json()
                image_url = donnee['sprites']['front_default']
            except: # A permis de se rendre compte quels pokemons n'avaient pas d'image
                # (d'où le tri du data frame)
                print(f"pas d'image pour {pokemon.nom}")
                return None

            image_reponse = requests.get(image_url)

            with open(nom_fichier, "wb") as fichier:
                fichier.write(image_reponse.content)

        return nom_fichier

    def afficherPokemons(self):
        i = 0
        taille_quart = TAILLE // 4 - 20  # Taille du quart sans les marges
        marge_x = 10  # Marge de 10 pixels
        marge_y = 10

        espace_horizontal = (taille_quart - 2 * marge_x) // 3
        espace_vertical = (taille_quart - 2 * marge_y) // 5
        for joueur in self.plateau.joueurs:
            if i == 0:
                origine_x, origine_y = marge_x, marge_y
            if i == 1:
                origine_x = TAILLE - taille_quart
                origine_y = marge_y
            x = origine_x
            y = origine_y

            for pokemon in joueur.pokemons:
                image = self.recupererImagePoke(pokemon)
                if image != None:
                    obj = self.g.afficherImage(x, y, image, espace_horizontal, espace_vertical)
                    pokemon.objet_image = obj
                    self.pokemon_img[obj] = pokemon  # On ajoute le pokemon et son image dans le dictionnaire
                    x += espace_horizontal

                    # Si on dépasse la largeur du quart on passe à la ligne suivante
                    if x + espace_horizontal > origine_x + taille_quart:
                        x = origine_x
                        y += espace_vertical

            i += 1

        self.g.afficherTexte("Joueur 1", TAILLE // 4, 20, "black")
        self.g.afficherTexte("Joueur 2", 3 * TAILLE // 4, 20, "black")


    def jouer(self):
        joueur = self.plateau.joueurs[0]
        self.tour = self.g.afficherTexte("Au tour de Joueur 1", TAILLE // 2, TAILLE // 4 - 50, "black")
        gagnant = None

        while not gagnant and not self.plateau.verifierPartieTerminee():
            self.plateau.tourDeJeu2(joueur)
            gagnant = self.plateau.estGagne()

            if gagnant:
                self.g.supprimer(self.tour)
                self.g.afficherTexte(f"{gagnant.nom} a gagné !", TAILLE // 2, TAILLE // 4 - 50, "black")
                print(f"{gagnant.nom} a gagné !")
            else:
                # on passe à l'autre joueur
                self.g.supprimer(self.tour)
                if joueur.id == self.plateau.joueurs[0].id:
                    joueur = self.plateau.joueurs[1]
                    self.tour = jeu.g.afficherTexte("Au tour de Joueur 2", TAILLE // 2, TAILLE // 4 - 50, "black")
                else:
                    joueur = self.plateau.joueurs[0]
                    self.tour = jeu.g.afficherTexte("Au tour de Joueur 1", TAILLE // 2, TAILLE // 4 - 50, "black")

            # Si les 2 joueurs sont des IA, on fait une pause
            if self.plateau.joueurs[0].est_ia == True and self.plateau.joueurs[1].est_ia == True:
                self.g.pause(0.5)

            self.g.actualiser()

        if not gagnant:
            gagnant = self.plateau.testerEgalite()
            if gagnant:
                print(f"{gagnant.nom} a gagné en gagnant le plus de morpions !")
        self.terminer()

    def terminer(self):
        self.g.attendreClic()
        self.g.fermerFenetre()


class Pokemon():
    def __init__(self, nom, type, HP, attaque, defense, vitesse):
        self.joueur = None  # Joueur qui le détient
        self.nom = nom
        self.type = type
        self.HP = HP
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.niveau = 1
        self.objet_image = None  # Objet graphique image
        self.objet_texte = None  # Objet graphique texte
        self.info_attaquant = set()
        self.info_defenseur = set()

    def afficherPokemon(self):
        print(f"Je suis le pokemon {self.nom}")

    def sortirBanc(self):
        self.joueur.pokemons.remove(self)
        jeu.g.cacher(self.objet_image)

    def revenirBanc(self):
        self.joueur.pokemons.add(self)
        jeu.g.montrer(self.objet_image)

    def entrerCase(self, case):
        if case.estVide():
            case.valeur = self
            case.dessinerSymbole(self.joueur.symbole, self)

        else:
            self.combattrePokemon(case.valeur, case)

    def calculer_multiplicateur(self, type_attaquant, types_defenseurs, type):

        multiplicateur_total = 1.0  # Multiplicateur initial

        for type_defenseur in types_defenseurs:
            # Récupère le multiplicateur pour le type défenseur
            multiplicateur = type.get(type_attaquant, {}).get(type_defenseur, 1)
            multiplicateur_total *= multiplicateur  # Multiplie par le multiplicateur trouvé

        return multiplicateur_total

    def calculerDegats(self, attaquant, defenseur):
        multiplicateur = self.calculer_multiplicateur(attaquant.type, defenseur.type, type)
        degats = (((((attaquant.niveau * 0.4 + 2) * attaquant.attaque) / defenseur.defense) / 50) + 2) * multiplicateur
        return degats

    def combattrePokemon(self, pokemon2, case):
        print(f"Combat entre {self.nom} et {pokemon2.nom}")
        resultat = 0
        while not self.HP == 0 and not pokemon2.HP == 0:
            degats_attaquant = self.calculerDegats(self, pokemon2)
            degats_defenseur = self.calculerDegats(pokemon2, self)
            self.HP = max(0, (self.HP - degats_defenseur))
            pokemon2.HP = max(0, (pokemon2.HP - degats_attaquant))

        if self.HP == 0 and pokemon2.HP == 0:  # Egalité
            case.valeur = None
            print("Egalité")
            case.effacerSymbole()
            case.effacerTexte()
            self.revenirBanc()
            pokemon2.revenirBanc()
            jeu.resultat_combat = jeu.g.afficherTexte("Egalité", TAILLE // 2, TAILLE - 100, "black")
        if self.HP == 0 and pokemon2.HP > 0:  # Défaite
            case.deja_win = True
            case.effacerTexte()
            self.revenirBanc()
            print(f"Le pokemon {self.nom} a perdu")
            jeu.resultat_combat = jeu.g.afficherTexte(f"Le pokemon {self.nom} a perdu", TAILLE // 2, TAILLE - 100,
                                                      "black")

        if self.HP > 0 and pokemon2.HP == 0:  # Victoire
            case.deja_win = True
            case.valeur = self
            case.effacerSymbole()
            case.effacerTexte()
            case.dessinerSymbole(self.joueur.symbole, self)
            pokemon2.revenirBanc()
            print(f"Le pokemon {self.nom} a gagné")
            jeu.resultat_combat = jeu.g.afficherTexte(f"Le pokemon {self.nom} a gagné", TAILLE // 2, TAILLE - 100,
                                                      "black")
        for info in pokemon2.info_defenseur:
            jeu.g.supprimer(info)
            pokemon2.info_defenseur = set()

        self.niveau += 1
        pokemon2.niveau += 1

    def afficherInfoDefenseur(self):
        if self.joueur.id == jeu.plateau.joueurs[0].id:
            x = TAILLE // 2 - (TAILLE // 2) // 4
        else:
            x = (TAILLE // 2) // 4 + TAILLE // 2
        y = 3 * TAILLE // 4 + 20

        info1 = jeu.g.afficherTexte(f"Défier {self.nom}", x, y, "black", 16)
        info2 = jeu.g.afficherTexte(f"HP : {self.HP}", x, y + 20, "black", 10)
        info3 = jeu.g.afficherTexte(f"Defense : {self.defense}", x, y + 40, "black", 10)
        info4 = jeu.g.afficherTexte(f"Niveau : {self.niveau}", x, y + 60, "black", 10)
        self.info_defenseur.add(info1)
        self.info_defenseur.add(info2)
        self.info_defenseur.add(info3)
        self.info_defenseur.add(info4)

    def afficherInfoAttaquant(self):
        if self.joueur.id == jeu.plateau.joueurs[0].id:
            x = TAILLE // 2 - (TAILLE // 2) // 4
        else:
            x = (TAILLE // 2) // 4 + TAILLE // 2
        y = 3 * TAILLE // 4 + 20

        info1 = jeu.g.afficherTexte(f"Jouer {self.nom}", x, y, "black", 16)
        info2 = jeu.g.afficherTexte(f"HP : {self.HP}", x, y + 20, "black", 10)
        info3 = jeu.g.afficherTexte(f"Attaque : {self.attaque}", x, y + 40, "black", 10)
        info4 = jeu.g.afficherTexte(f"Niveau : {self.niveau}", x, y + 60, "black", 10)
        self.info_attaquant.add(info1)
        self.info_attaquant.add(info2)
        self.info_attaquant.add(info3)
        self.info_attaquant.add(info4)


class Joueur():
    def __init__(self, id, nom, symbole):
        self.nom = nom
        self.pokemons = set()
        self.nombre_mini_win = 0
        self.symbole = symbole
        self.est_ia = False
        self.id = id
        self.tours = 0

    def afficherPokemons(self):
        for pokemon in self.pokemons:
            print(f"Je suis le poke {pokemon.nom} et j'appartiens à {self.nom}")

    def calculerMoyenne(self):
        total = sum(pokemon.vitesse for pokemon in self.pokemons)
        print(total / len(self.pokemons))

    def choisirMorpion(self):
        print("Choisir un morpion")
        morpion_l = random.choice([0, 1, 2])
        morpion_c = random.choice([0, 1, 2])
        print(f"Morpion choisi : ({morpion_l},{morpion_c})")
        return morpion_l, morpion_c

    def choisirCase(self):
        choix = jeu.g.afficherTexte("Choisir Case", TAILLE // 2, 20, "black")
        clic = jeu.g.attendreClic()

        if clic:
            while not TAILLE // 4 <= clic.x <= 3 * TAILLE // 4 or not TAILLE // 4 <= clic.y <= 3 * TAILLE // 4:
                clic = jeu.g.attendreClic()
            jeu.g.supprimer(choix)
            return clic.x, clic.y
        else:
            return -1, -1

    def obtenirCase(self):
        x, y = self.choisirCase()
        #print(f"x = {x}, y = {y}")

        # origine (0,0) dans le coin supérieur gauche du plateau
        x = x - (TAILLE // 4)
        y = y - (TAILLE // 4)

        # Déterminer le mini plateau
        lm = y // taille_mini_plateau
        cm = x // taille_mini_plateau

        # Déterminer la case à l'intérieur du mini plateau
        l = (y % taille_mini_plateau) // taille_case
        c = (x % taille_mini_plateau) // taille_case

        #print(f"lm = {lm}, cm = {cm}, l = {l}, c = {c}")
        return lm, cm, l, c

    def choisirPokemon(self):
        choix = jeu.g.afficherTexte("Choisir Pokemon", TAILLE // 2, 20, "black")
        valider = jeu.g.dessinerRectangle(TAILLE // 2 - (TAILLE // 6 // 2), 100 - (TAILLE // 20 // 2), TAILLE // 6,
                                          TAILLE // 20, "black")
        valider_txt = jeu.g.afficherTexte("Valider", TAILLE // 2, 100, "white")
        bouton_valider = {valider, valider_txt}
        # On garde en mémoire le poke sélectionné
        pokemon_selectionne = None
        objet_selectionne = None
        fini = False

        while True:
            clic = jeu.g.attendreClic()
            obj = jeu.g.recupererObjet(clic.x, clic.y)
            # Si l'utilisateur a choisi un pokemon et que le clic est soit sur un poke soit sur le bouton valider
            # (permet de pouvoir cliquer sur le fond noir sans faire planter le programme)
            if pokemon_selectionne and (obj in jeu.pokemon_img or obj in bouton_valider):
                for info in pokemon_selectionne.info_attaquant:
                    jeu.g.supprimer(info)
                    pokemon_selectionne.info_attaquant = set()

            # Si le clic est sur un pokemon
            if obj in jeu.pokemon_img and jeu.pokemon_img[obj].joueur.id == self.id:
                pokemon = jeu.pokemon_img[obj]
                pokemon.afficherInfoAttaquant()

                # On met à jour la selection
                pokemon_selectionne = pokemon
                #print(pokemon_selectionne.nom)
                objet_selectionne = obj

            # Si on valide et qu'on a choisi un poke
            if obj in bouton_valider and pokemon_selectionne:
                pokemon_selectionne.sortirBanc()
                jeu.g.supprimer(choix)
                return pokemon_selectionne

    def simuler_choisirPokemon(self):
        pokemon = random.choice(list(self.pokemons))
        self.pokemons.remove(pokemon)
        return pokemon


class IA(Joueur):
    def __init__(self, id, nom, symbole):
        super().__init__(id, nom, symbole)
        self.est_ia = True

    def obtenirCase(self):
        lm = random.choice([0, 1, 2])
        cm = random.choice([0, 1, 2])
        l = random.choice([0, 1, 2])
        c = random.choice([0, 1, 2])
        return lm, cm, l, c

    def choisirPokemon(self):
        pokemon = random.choice(list(self.pokemons))
        pokemon.sortirBanc()
        return pokemon


class IA_minimax(IA):
    def __init__(self, id, nom, symbole):
        super().__init__(id, nom, symbole)

    def obtenirCase(self):
        action = self.minimax(jeu.plateau, self.id)
        _, lm, cm, l, c = action[0]
        return lm, cm, l, c

    def obtenirJoueurSuivant(self, plateau):
        if plateau.verifierPartieTerminee():
            return None

        prochain_joueur = 0
        if plateau.joueurs[0].tours > plateau.joueurs[1].tours:
            prochain_joueur = plateau.joueurs[1].id
        else:
            prochain_joueur = plateau.joueurs[0].id

        return prochain_joueur

    def obtenirListesActionsPossibles(self, plateau):
        indice_joueur = self.obtenirJoueurSuivant(plateau)
        if indice_joueur == None:
            return []

        joueur = plateau.joueurs[indice_joueur]
        actions_list = []

        # Idéalement, il faudrait pouvoir combattre un pokemon. Pour simplifier, l'IA_minimax ne peut choisir que des cases vides (Case.valeur == None)
        if plateau.morpion_impose == None or plateau.morpion[plateau.morpion_impose[0]][
            plateau.morpion_impose[1]].verifierMiniPlateauTermine():
            for ligne_morpion in range(3):
                for colonne_morpion in range(3):
                    if not plateau.morpion[ligne_morpion][colonne_morpion].verifierMiniPlateauTermine():
                        for l in range(3):
                            for c in range(3):
                                if plateau.morpion[ligne_morpion][colonne_morpion].morpion[l][c].valeur == None:
                                    actions_list.append((indice_joueur, ligne_morpion, colonne_morpion, l, c))
        else:
            ligne_morpion, colonne_morpion = plateau.morpion_impose
            for l in range(3):
                for c in range(3):
                    if plateau.morpion[ligne_morpion][colonne_morpion].morpion[l][c].valeur == None:
                        actions_list.append((indice_joueur, ligne_morpion, colonne_morpion, l, c))

        return actions_list

    def obtenirPlateauApresAction(self, plateau, action):
        (indice_joueur, ligne_morpion, colonne_morpion, ligne_case, colonne_case) = action
        copie_plateau = copy.deepcopy(plateau)
        pokemon = copie_plateau.joueurs[indice_joueur].simuler_choisirPokemon()
        copie_plateau.morpion[ligne_morpion][colonne_morpion].morpion[ligne_case][colonne_case].valeur = pokemon
        copie_plateau.morpion_impose = (ligne_case, colonne_case);
        copie_plateau.joueurs[indice_joueur].tours += 1

        return copie_plateau

    def obtenirScoreFinal(self, plateau):
        gagnant = plateau.estGagne()
        if gagnant is not None:
            # si la partie a été remportée, on attribue +/-10 selon le vainqueur
            if gagnant.id == 0:
                return 10
            else:
                return -10

        # si la partie est finie sans vainqueur, le score est 0
        if self.obtenirJoueurSuivant(plateau) is None:
            return 0

        # Comme on limite la profondeur de recherche (voir minimax()),
        # la plupart du temps on n'atteint pas la fin de la partie. Pour
        # tout de même départager deux actions différentes, on attribue un point
        # si le premier joueur (joueur id 0) a remporté un mini-plateau.
        # Si c'est l'autre joueur (joueur id 1) qui remporte un mini-plateau,
        # un point est retiré. Dans tous les cas, gagner un ou plusieurs mini-plateau(x)
        # remporte moins de point que de remporter la partie (+/-10 points)
        score = 0
        for ligne_morpion in range(3):
            for colonne_morpion in range(3):
                if plateau.morpion[ligne_morpion][colonne_morpion].verifierMiniPlateauTermine():
                    gagnant_mini_plateau = plateau.morpion[ligne_morpion][colonne_morpion].estGagne()
                    if gagnant_mini_plateau is not None:
                        if gagnant_mini_plateau.id == 0:
                            score += 1
                        else:
                            score -= 1
        if score != 0:
            return score

        return None

    def afficherPlateau(self, plateau):
        os.system("clear")
        for ligne_morpion in range(3):
            print("-" * 15)
            for l in range(3):
                for colonne_morpion in range(3):
                    print("|", end="")
                    for c in range(3):
                        if plateau.morpion[ligne_morpion][colonne_morpion].morpion[l][c].valeur == None:
                            print(" ", end="")
                        else:
                            joueur = plateau.morpion[ligne_morpion][colonne_morpion].morpion[l][c].valeur.joueur
                            print(joueur.symbole, end="")
                    print("|", end="")
                print()

    def minimax(self, plateau, id_joueur, cout=1):
        action_list = self.obtenirListesActionsPossibles(plateau)
        liste_action_score_cout = []
        for action in action_list:
            nouveau_plateau = self.obtenirPlateauApresAction(plateau, action)
            self.afficherPlateau(nouveau_plateau)

            score_final = self.obtenirScoreFinal(nouveau_plateau)
            if score_final is not None:
                return (action, (score_final, cout))

            # on limite la profondeur de recherche (cout)
            if cout > 3:
                return (action, (0, cout))

            joueur_suivant = self.obtenirJoueurSuivant(nouveau_plateau)

            liste_action_score_cout.append((action, self.minimax(nouveau_plateau, joueur_suivant, cout + 1)))

        if len(liste_action_score_cout) == 0:
            return ((0, 0, 0, 0, 0), (0, 0))

        # On trie la liste par score puis par cout
        liste_triee = sorted(liste_action_score_cout,
                             key=lambda l: l[1])  # lambda fonction pour mettre un critère sur le tri
        if id_joueur == 0:
            # On choisit le plus grand score avec le plus petit cout (car les couts sont tries par ordre croissant)
            action_score_cout = max(liste_triee, key=lambda l: l[1][0])
        else:
            # On choisit le plus petit score avec le plus petit cout
            action_score_cout = min(liste_triee, key=lambda l: l[1][0])

        return action_score_cout


jeu = Partie()
jeu.initMenu()
jeu.selectionerModeJeu()
jeu.dessinerGrille()
jeu.repartirPokemons()
jeu.afficherPokemons()
jeu.jouer()

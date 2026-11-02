# Jeu du Pendu

Projet réalisé par **Kevin Ngo, Mathis Portal et Marine Merault**, dans le cadre de la L1 Double Licence Informatique et Sciences de la Vie (LDDBI).

## Présentation du projet

Ce projet consiste à développer un jeu du Pendu en Python, à l'aide de la bibliothèque Tkinter pour créer une interface graphique interactive.

Le joueur doit retrouver un mot choisi aléatoirement en proposant des lettres, tout en disposant d'un nombre limité de tentatives.

## Prérequis

- Python 3 (version récente).
- Bibliothèque Tkinter.
- Bibliothèque Random (incluse dans Python).
- Bibliothèque Unicodedata (incluse dans Python).

## Installation et lancement

1. Télécharger ou cloner le dépôt GitHub.
2. Ouvrir un terminal dans le dossier du projet.
3. Exécuter le fichier `pendu.py` avec la commande :

```bash
python pendu.py
```

Aucune installation supplémentaire de bibliothèque Python n'est nécessaire.

## Comment jouer ?

1. Lancez le programme à l'aide du fichier `pendu.py`.
2. Dans le menu principal, choisissez :
   - **Jouer** : commencer une nouvelle partie.
   - **Règles du jeu** : consulter les règles.
   - **Fermer le jeu** : quitter le programme.
3. Choisissez la longueur du mot souhaitée parmi les longueurs disponibles (de 2 à 19 lettres).
4. Devinez le mot en proposant des lettres. Vous disposez de **7 tentatives** avant de perdre.
5. Si vous avez besoin d'aide, utilisez le bouton **« Besoin d'indice ? »** pour obtenir une lettre aléatoire qui n'a pas encore été découverte. Cette fonctionnalité peut être utilisée plusieurs fois.
6. Le bouton **« Changer de mot »** permet de sélectionner un nouveau mot et de choisir sa longueur.
7. À la fin d'une partie, vous pouvez recommencer ou quitter le jeu.
8. Le nombre de victoires est affiché dans la fenêtre de jeu.

## Fonctionnalités

- Sélection aléatoire des mots en fonction de leur longueur.
- Gestion des accents lors de la saisie des lettres.
- Vérification des lettres proposées et détection des doublons.
- Affichage progressif du dessin du pendu.
- Système d'indices.
- Compteur de victoires.
- Possibilité de recommencer une partie ou de changer de mot.
- Interface graphique avec affichage en plein écran.

## Bibliothèques utilisées

- **Tkinter** : création de l'interface graphique.
- **Random** : sélection aléatoire des mots et des indices.
- **Unicodedata** : gestion des accents.

## Ressources utilisées

- [DelftStack – Création de menus déroulants avec Tkinter](https://www.delftstack.com/fr/howto/python-tkinter/how-to-create-dropdown-menu-in-tkinter/) : ressource utilisée pour la création du menu déroulant.
- **DeepSeek** : aide à la correction de certaines erreurs.

## Licence

Ce projet est distribué sous licence **Apache License 2.0**.

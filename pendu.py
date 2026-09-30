import tkinter as tk
import random
import unicodedata

#VARIABLE GLOBALE

compteur_erreur = 0
scores = 0
lettres_pas_bon = []
mot_inconnu = ""
mot_à_remplir = ""
label_indice = None


def sans_accents(texte):
    """Retire les accents d'un texte (é -> e, ê -> e, ç -> c ...)."""
    return "".join(c for c in unicodedata.normalize("NFD", texte) if unicodedata.category(c) != "Mn")


# Liste de mots (sans classement) : ils sont triés automatiquement par longueur juste en dessous
MOTS = [
    "or", "os", "un", "du",
    "eau", "air", "fer", "sel", "mur", "lac", "vue", "nez", "lit", "pas", "cle", "bus", "ami", "mot", "dos",
    "chat", "bleu", "gris", "rose", "vert", "noir", "lion", "peur", "pneu", "jour", "lune", "miel", "ciel", "pain",
    "chien", "fruit", "table", "porte", "plage", "lampe", "avion", "pizza", "robot", "pomme", "forêt", "livre", "musee", "coeur", "poire",
    "symport", "banane", "bateau", "valise", "tomate", "cinema", "orange", "fusee", "ocean", "raisin", "casque", "garage", "gateau", "souris", "jardin", "palais",
    "animaux", "avocate", "cascade", "clavier", "fenetre", "voiture", "guitare", "docteur", "cheveux", "paysage", "triangle", "montage", "couleur", "sandale", "musique",
    "chocolat", "biologie", "batterie", "internet", "football", "montagne", "histoire", "plomberie", "paysanne", "écureuil", "physique", "espagnol", "dentiste", "ordinateur",
    "infirmier", "programme", "hamburger", "genetique", "croissant", "xylophone", "allegorie", "capitaine", "architecte", "avalanche", "nucléaire", "dirigeant", "injustice", "pediatrie",
    "algorithme", "astronomie", "basketball", "palindrome", "cytoplasme", "geographie", "restaurant", "neurologie", "pharmacien", "professeur", "hebergement", "ventilateur", "psychologie", "teleferique", "composition",
    "ascomycetes", "journaliste", "cardiologue", "immunologie", "chromosomes", "psychologue", "archeologue", "osteoporose", "bibliophile", "interpreter", "volontariat", "pathologie", "sociologue", "radiologue", "hemorragique",
    "bibliotheque", "informatique", "intelligence", "scientifique", "metaphysique", "démocratique", "encyclopedie", "multiplication", "transmission", "complication", "localisation", "reglementaire", "traitement", "considerable", "desoxyribose",
    "cryptographie", "cybersecurite", "microbiologie", "photosynthese", "mathematiques", "neurochirurgie", "administration", "identification", "caracteristique", "collaboration", "architecture", "interpretation", "automatiquement", "bioluminescent", "specialisation",
    "phycoerythrine", "archaeplastida", "virtualisation", "rationalisation", "structuralement", "exceptionnelles", "interprétations", "personnalisation", "recommandations", "internationaliser", "restructurations", "organisationnelle", "representativité", "caracterisations", "incompatibilites",
    "thermodynamique", "desoxyhemoglobine", "bioaccumulations", "instrumentalismes", "neurodeveloppement", "dematerialisation", "pluridisciplinaires", "anticonstitutionnel", "microspectrometrie", "contreproductivite", "bioluminescences", "desapprobations",
]

# CORRECTION : les mots sont rangés selon leur VRAIE longueur et sans accents
# (ainsi "forêt" se joue avec la lettre "e", et chaque longueur contient les bons mots)
mots_par_longueur = {}
for _mot in MOTS:
    _mot = sans_accents(_mot.lower())
    mots_par_longueur.setdefault(len(_mot), [])
    if _mot not in mots_par_longueur[len(_mot)]:
        mots_par_longueur[len(_mot)].append(_mot)


def plein_ecran(fenetre):
    """Met une fenêtre en plein écran. La touche Échap permet d'en sortir."""
    fenetre.attributes('-fullscreen', True)
    fenetre.bind('<Escape>', lambda e: fenetre.attributes('-fullscreen', False))


def Pour_rejouer_gagné():
    global scores
    scores += 1
    rejouerg = tk.Toplevel()
    rejouerg.config(bg="skyblue")
    rejouerg.grid_columnconfigure(0, weight=1)
    rejouerg.grid_rowconfigure(0, weight=1)
    rejouerg.grid_rowconfigure(4, weight=1)
    bravo = tk.Label(rejouerg, text='Bravo tu as gagné !! Tu as sauvé le bonhomme', font=("Comic Sans MS", 40), bg="skyblue")
    button_rejouerg = tk.Button(rejouerg, font=("Comic Sans MS", 15), width=40, height=3, text='Rejouer?', command=lambda: [afficher_menu_longueur(), rejouerg.destroy()])
    button_fermer1 = tk.Button(rejouerg, font=("Comic Sans MS", 15), width=40, height=3, text='Quitter le jeu ', command=lambda: menu.destroy())
    button_fermer1.grid(column=0, row=3, pady=35)
    button_rejouerg.grid(column=0, row=2, pady=35)
    bravo.grid(column=0, row=1)
    plein_ecran(rejouerg)


def Pour_rejouer_perdu():
    global mot_inconnu
    rejouerp = tk.Toplevel()
    for i in range(4):
        rejouerp.grid_columnconfigure(i, weight=1)
        rejouerp.grid_rowconfigure(i, weight=1)
    rejouerp.config(bg="skyblue")

    dommage = tk.Label(rejouerp, text="Dommage, tu as perdu le mot était <" + mot_inconnu + ">", font=("courier", 15, "italic"), bg="skyblue")
    dommage.grid(column=1, row=1, padx=10)
    button_rejouerp = tk.Button(rejouerp, font=("Comic Sans MS", 15), width=15, height=3, text='Rejouer?', command=lambda: [afficher_menu_longueur(), rejouerp.destroy()])
    button_rejouerp.grid(column=1, row=2, pady=20)

    bouton_fermer2 = tk.Button(rejouerp, text="Quitter le jeu", width=15, height=3, command=lambda: menu.destroy(), font=("Comic Sans MS", 15))
    bouton_fermer2.grid(column=1, row=3)

    plein_ecran(rejouerp)

    CANVAS_WIDTH, CANVAS_HEIGHT = 400, 400
    canvas = tk.Canvas(rejouerp, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="light slate blue", highlightthickness=0)
    canvas.grid(row=2, column=2, rowspan=2)

    a0, b0 = 100, CANVAS_HEIGHT - 150
    canvas.create_line(a0, b0, a0 + 100, b0)
    canvas.create_line(a0 + 20, b0, a0 + 20, b0 - 150)
    canvas.create_line(a0 + 20, b0 - 150, a0 + 70, b0 - 150)
    canvas.create_line(a0 + 20, b0 - 120, a0 + 45, b0 - 150)

    canvas.create_line(170, 100, 170, 125, width=2)
    canvas.create_oval(160, 125, 180, 145, width=2)
    canvas.create_line(170, 145, 170, 200, width=2)
    canvas.create_line(170, 170, 145, 150, width=2)
    canvas.create_line(170, 170, 195, 150, width=2)
    canvas.create_line(170, 200, 145, 220, width=2)
    canvas.create_line(170, 200, 195, 220, width=2)


####################################################################################
###################### FONCTIONNMENT JEU ###########################################
####################################################################################

def choisir_mot(longueur):
    if longueur in mots_par_longueur:
        return random.choice(mots_par_longueur[longueur])
    return None

def longueur_est_1(entree):
    return len(entree) <= 1


def lettres_positions(mot):
    dico = {}
    for index, lettre in enumerate(mot):
        if lettre not in dico:
            dico[lettre] = []
        dico[lettre].append(index)
    return dico

def erreurs_pendu(canvas):
    # CORRECTION : cette fonction ne fait que dessiner. La fenêtre "perdu" est
    # ouverte uniquement dans verifier_lettre() (avant, elle s'ouvrait 2 fois).
    if compteur_erreur == 1:
        canvas.create_line(170, 100, 170, 125, width=2)  # corde
    elif compteur_erreur == 2:
        canvas.create_oval(160, 125, 180, 145, width=2)  # tête
    elif compteur_erreur == 3:
        canvas.create_line(170, 145, 170, 200, width=2)  # Corps
    elif compteur_erreur == 4:
        canvas.create_line(170, 170, 145, 150, width=2)  # Bras gauche
    elif compteur_erreur == 5:
        canvas.create_line(170, 170, 195, 150, width=2)  # Bras droit
    elif compteur_erreur == 6:
        canvas.create_line(170, 200, 145, 220, width=2)  # Jambe gauche
    elif compteur_erreur == 7:
        canvas.create_line(170, 200, 195, 220, width=2)  # Jambe droite


def pendu(fenetre_jeu, canvas):
    global compteur_erreur, lettres_pas_bon, mot_inconnu, dico_lettres_positions, mot_à_remplir

    mot_inconnu = choisir_mot(longueur_choisie)
    mot_à_remplir = ['*' for _ in range(len(mot_inconnu))]
    dico_lettres_positions = lettres_positions(mot_inconnu)

    affiche_mot_remplir = tk.Label(fenetre_jeu, text="".join(mot_à_remplir), font=("Comic Sans MS", 55), background='light blue')
    affiche_mot_remplir.grid(row=0, column=1, pady=20)

    affiche_lettres_pas_bon = tk.Label(fenetre_jeu, text="", font=("Comic Sans MS", 20), background='light blue')
    affiche_lettres_pas_bon.grid(row=1, column=1, pady=10)
    #################################################################################################################

    def verifier_lettre():
        global compteur_erreur, lettres_pas_bon
        lettre = sans_accents(entrée.get().lower())
        entrée.delete(0, tk.END)

        # CORRECTION : on ignore une entrée vide ou qui n'est pas une lettre
        if lettre == "" or not (lettre.isascii() and lettre.isalpha()):
            return
        # CORRECTION : une lettre déjà jouée (trouvée ou ratée) ne coûte rien
        if lettre in lettres_pas_bon or lettre in mot_à_remplir:
            return

        if lettre in dico_lettres_positions:
            for index in dico_lettres_positions[lettre]:
                mot_à_remplir[index] = lettre
            affiche_mot_remplir.config(text="".join(mot_à_remplir))

            if "*" not in mot_à_remplir:  # VERIFIE QUE LE MOT A ETE COMPLETEMENT TROUVE
                Pour_rejouer_gagné()
                fenetre_jeu.destroy()
        else:
            lettres_pas_bon.append(lettre)
            affiche_lettres_pas_bon.config(text=", ".join(lettres_pas_bon))

            compteur_erreur += 1
            tentatives_restantes.config(text="Tentatives restantes: " + str(7 - compteur_erreur))
            erreurs_pendu(canvas)

            if compteur_erreur >= 7:
                Pour_rejouer_perdu()
                fenetre_jeu.destroy()

    question = tk.Label(fenetre_jeu, text="Essayez de deviner une lettre :", font=("Comic Sans MS", 15), background='light blue')
    question.grid(row=4, column=1, pady=10)

    verification_longueur_1 = fenetre_jeu.register(longueur_est_1)
    entrée = tk.Entry(fenetre_jeu, validate="key", validatecommand=(verification_longueur_1, '%P'), font=("Comic Sans MS", 20), background='white')
    entrée.grid(row=5, column=1, pady=10)
    entrée.bind('<Return>', lambda e: verifier_lettre())  # Entrée valide aussi la lettre
    entrée.focus_set()

    bouton_valider = tk.Button(fenetre_jeu, text="Valider", command=verifier_lettre, font=("Comic Sans MS", 15))
    bouton_valider.grid(row=6, column=1, pady=10)

###################################################################################
####################### REGLES VIA MENU PRINCIPAL##################################
###################################################################################


def ouvrir_regles():
    regles = tk.Toplevel()
    plein_ecran(regles)
    regles.title("Les règles")
    regles.configure(bg='dark orchid')
    label = tk.Label(regles, text="Un mot est choisi au hasard", background='dark orchid', font=("Comic Sans MS", 17))
    label1 = tk.Label(regles, text="et VOUS devez devinez le mot, lettre par lettre", background='dark orchid', font=("Comic Sans MS", 17))
    label2 = tk.Label(regles, text="vous avez le droit à 7 erreurs", background='dark orchid', font=("Comic Sans MS", 17))
    label3 = tk.Label(regles, text="à la huitième,le bonhomme...", background='dark orchid', font=("Comic Sans MS", 17))
    label4 = tk.Label(regles, text="SE FAIT PENDRE !!!", background='dark orchid', font=("Chiller", 55))
    label.pack(pady=2)
    label1.pack(pady=4)
    label2.pack(pady=6)
    label3.pack(pady=8)
    label4.pack(pady=10)

    # CORRECTION : taille du bouton raisonnable (avant height=20 et pady=210 sortaient de l'écran)
    boutonfermer_règles = tk.Button(regles, text="Retour au menu", font=("Comic Sans MS", 20), command=regles.destroy, width=20, height=2, bg='thistle1', relief='flat')
    boutonfermer_règles.pack(pady=40)
    # CORRECTION : suppression de regles.mainloop() (la boucle principale tourne déjà)


def indice():
    global dico_lettres_positions
    # CORRECTION : on choisit parmi les lettres PAS ENCORE trouvées (avant : UnboundLocalError possible)
    lettres_restantes = [l for l in dico_lettres_positions if l not in mot_à_remplir]
    if not lettres_restantes:
        return
    # CORRECTION : un seul label d'indice, mis à jour (avant : un nouveau label à chaque clic)
    label_indice.config(text=random.choice(lettres_restantes))

###########################################################################################################
######################################## INTERFACE PRIMAIRE #################################################
###########################################################################################################

def ouvrir_jeu():
    global fenetre_jeu, compteur_erreur, lettres_pas_bon, scores, tentatives_restantes, label_indice

    fenetre_jeu = tk.Toplevel()
    fenetre_jeu.title("Jeu du Pendu")
    fenetre_jeu.configure(bg="light blue")
    plein_ecran(fenetre_jeu)

    for i in range(6):
        fenetre_jeu.grid_rowconfigure(i, weight=1)
    for j in range(3):
        fenetre_jeu.grid_columnconfigure(j, weight=1)

    boutonreload = tk.Button(fenetre_jeu, text="Changer de mot", width=15, height=3, font=("Comic Sans MS", 15), command=fctcombine)
    boutonreload.grid(column=0, row=0, padx=10, pady=10)

    boutonfermerjeu = tk.Button(fenetre_jeu, text="Retour au Menu", width=15, height=3, command=fenetre_jeu.destroy, font=("Comic Sans MS", 15))
    boutonfermerjeu.grid(column=0, row=5, padx=10, pady=10)

    scors = tk.Label(fenetre_jeu, text="Nombre de victoires: " + str(scores), font=("Comic Sans MS", 15), bg="light blue")
    scors.grid(column=2, row=0, padx=30)  # LIE AU FONCTIONNEMENT DU JEU SCORES SAUVEGARDE CHAQUE PARTIE

    boutonindice = tk.Button(fenetre_jeu, text="Besoin d'indice?", font=("Comic Sans MS", 15), width=15, height=3, relief="flat", command=indice)
    boutonindice.grid(column=0, row=2, pady=10)

    label_indice = tk.Label(fenetre_jeu, text="", font=("Comic Sans MS", 30), bg="light blue")
    label_indice.grid(row=3, column=0, pady=10)

    tentatives_restantes = tk.Label(fenetre_jeu, text="Tentatives restantes: " + str(7), font=("Comic Sans MS", 15), bg="light blue")
    tentatives_restantes.grid(column=2, row=1, padx=30)  # RENITIALISE A CHAQUE PARTIE

    CANVAS_WIDTH, CANVAS_HEIGHT = 400, 400
    canvas = tk.Canvas(fenetre_jeu, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="light pink", borderwidth=2.5, relief="solid")
    canvas.grid(row=2, column=1, rowspan=2)
    # RENITIALISATION VARIABLES GLOBALES NOUVELLE PARTIE
    compteur_erreur = 0
    lettres_pas_bon = []
    pendu(fenetre_jeu, canvas)
    a0, b0 = 100, CANVAS_HEIGHT - 150
    canvas.create_line(a0, b0, a0 + 100, b0)
    canvas.create_line(a0 + 20, b0, a0 + 20, b0 - 150)
    canvas.create_line(a0 + 20, b0 - 150, a0 + 70, b0 - 150)
    canvas.create_line(a0 + 20, b0 - 120, a0 + 45, b0 - 150)


def fctcombine():  # CALLBACK FONCTION POUR CHANGER DE MOT DONC A NOUVEAU CHOIX LONGUEUR
    fenetre_jeu.destroy()
    afficher_menu_longueur()


def afficher_menu_longueur():
    menulong = tk.Toplevel()
    plein_ecran(menulong)

    menulong.title("Choix de la longueur du mot")
    menulong.config(bg="light blue")

    label = tk.Label(menulong, text="Choisis la longueur du mot :", font=("Comic Sans MS", 18), bg="light blue")
    label.pack(pady=20)

    var_longueur = tk.IntVar()
    var_longueur.set(2)  # valeur par défaut

    longueurs_disponibles = sorted(mots_par_longueur.keys())
    menu_deroulant = tk.OptionMenu(menulong, var_longueur, *longueurs_disponibles)  # Cherché sur internet
    menu_deroulant.config(font=("Comic Sans MS", 14))
    menu_deroulant.pack(pady=10)

    def valider_choix():
        global longueur_choisie
        longueur_choisie = var_longueur.get()  # MAJ Val longueur
        menulong.destroy()

        ouvrir_jeu()

    bouton_valider = tk.Button(menulong, text="Valider", font=("Comic Sans MS", 14), command=valider_choix)
    bouton_valider.pack(pady=20)


# fenêtre principale
menu = tk.Tk()
plein_ecran(menu)
menu.title("Menu du pendu")
menu.configure(bg='skyblue')
labelmenu = tk.Label(menu, text="Bienvenue dans le pendu", font=("Comic Sans MS", 30), bg="skyblue", fg="yellow")
labelmenu.grid(column=0, row=0)

menu.grid_columnconfigure(0, weight=1)
menu.grid_rowconfigure(0, weight=1)
menu.grid_rowconfigure(5, weight=1)


# Boutons centrés
boutonjouer = tk.Button(menu, text="Jouer", font=("Comic Sans MS", 15), width=40, height=3, relief="flat", command=afficher_menu_longueur)
boutonjouer.grid(column=0, row=1, pady=10)

boutonregles = tk.Button(menu, text="Règles du jeu", font=("Comic Sans MS", 15), width=40, height=3, relief="flat", command=ouvrir_regles)
boutonregles.grid(column=0, row=2, pady=10)


boutonfermer = tk.Button(menu, text="Fermer le jeu", font=("Comic Sans MS", 15), width=40, height=3, relief="flat", command=lambda: menu.destroy())
boutonfermer.grid(column=0, row=3, pady=10)

menu.mainloop()

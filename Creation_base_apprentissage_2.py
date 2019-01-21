## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# DESCRIPTION DU CODE - Création de la base d'apprentissage et de teste
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# ENTREES :  - Fichier python à mettre dans le même répertoire que les fichier de log
## %%%%----------------------------------------------------------------------------------%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# SORTIES :  - Fichier .txt comprenant les fichier de différents formats avec comme 
# séparateur le type de format // fichier_test_sopra.txt
## %%%%----------------------------------------------------------------------------------%%%%

## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# PROJET  :   Projet Sopra Steria - ECAM Rennes // Log Mining
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# AUTEURS  : Guillaume HABERT - Louis GABORIAU - Ulysse DANSIN
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# HISTORIQUE :
# +-----------------------------------------------------------------------------------------+
# | Ver. |   Date   |  RA  | Aut.   | Commentaire                                           |
# +-----------------------------------------------------------------------------------------+
# | 1.0.0 |10/01/2019|  --  |  L  | Modif separation() pour séparer toutes les 1000 lignes au lieu de 30ko |
# +-----------------------------------------------------------------------------------------+
# | 1.1.0 |18/01/2019|  --  |  L  | Modif Selection_sequences_par_fichier() et Ajout_reponse() |

##################################################################################################################
#imports
##################################################################################################################
from collections import Counter
import os
import time
import shutil
import sys 
from math import *

#_________________________________________________________________________________________________________________
#Fin des imports
#_________________________________________________________________________________________________________________



##################################################################################################################
#Variables nécessaires
##################################################################################################################
global chemin
global chemin_log
global chemin_log_separer
global poids_dossier_log
global chemin_txts_sequences

chemin = os.path.dirname(os.path.abspath(__file__))
chemin_log = chemin + "/base_de_log"
chemin_log_separer = chemin + "/logs_séparer"
chemin_txts_sequences = chemin +"/txts_sequences"
Nombre_log_separe = 1
#_________________________________________________________________________________________________________________
#Fin des variables nécessaires
#_________________________________________________________________________________________________________________



##################################################################################################################
#Class Barre de progression :
#Entrée : --
#Sortie : 
#         
##################################################################################################################
class ProgressBar:
    """
    This class allows you to make easily a progress bar.
    """

    def __init__(self, steps, maxbar=100, title='Progression'):
        if steps <= 0:
            raise ValueError

        self.steps = steps
        self.title = title

        self.perc = 0
        self._completed_steps = 0

        self.update(False)

    def update(self, increase=True):
        if increase:
            self._completed_steps += 1
        maxbar=50
        
        
        if self._completed_steps > self.steps:
            self._completed_steps = self.steps
        self.perc = floor(self._completed_steps / self.steps * 50)
        steps_bar = floor(self.perc)

        if steps_bar == 0:
            visual_bar = maxbar * ' '
        else:
            visual_bar = (steps_bar - 1) * '=' + '>' + (maxbar - steps_bar) * ' '

        sys.stdout.write('\r' + self.title + ' [' + visual_bar + '] ' + str((self.perc)*2) + '%')
        sys.stdout.flush()
#_________________________________________________________________________________________________________________
#Fin de la Class Barre de progression
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def creation_dossier_log_separer :
#Entrée : --
#Sortie : -Dossier de log séparer créé
##################################################################################################################
def creation_dossier_log_separer():
    os.chdir(chemin)
    if os.path.isdir("logs_séparer"):
        shutil.rmtree("logs_séparer")
        os.mkdir("logs_séparer")
    else:
        os.mkdir("logs_séparer")
#_________________________________________________________________________________________________________________
#Fin de la def creation_dossier_log_separer()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def creation_dossier_log_separer :
#Entrée : --
#Sortie : -Dossier de txts_sequences créé
##################################################################################################################
def creation_dossier_txts_sequences():
    os.chdir(chemin)
    if os.path.isdir("txts_sequences"):
        shutil.rmtree("txts_sequences")
        os.mkdir("txts_sequences")
    else:
        os.mkdir("txts_sequences")
#_________________________________________________________________________________________________________________
#Fin de la def creation_dossier_txts_sequences()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def suppression_dossier_log_separer :
#Entrée : --
#Sortie : -Dossier de log séparer supprimé
##################################################################################################################
def suppression_dossier_log_separer():
    print("Suppression dossier log_separer en cours ...")
    os.chdir(chemin)
    shutil.rmtree("logs_séparer")
    print("Dossier log_separer supprimé")
#_________________________________________________________________________________________________________________
#Fin de la def suppression_dossier_log_separer()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def suppression_dossier_txts_sequences :
#Entrée : --
#Sortie : -Dossier de txts_sequences supprimé
##################################################################################################################
def suppression_dossier_txts_sequences():
    print("Suppression dossier txts_sequences en cours ...")
    os.chdir(chemin)
    shutil.rmtree("txts_sequences")
    print("Dossier txts_sequences supprimé")
#_________________________________________________________________________________________________________________
#Fin de la def suppression_dossier_txts_sequences()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def separation :
#Entrée : Fichier log à séparer
#Sortie : -Fichier séparer en plusieurs fichiers au même endroit que le fichier d'origine
#         -Fichier d'origine supprimé
##################################################################################################################
def separation(log_a_sep,taille_max_lignes):
    os.chdir(chemin)
    try:
        os.path.isdir("logs_séparer")
    except:
        print("dossier logs_séparer n'existe pas")

    os.chdir(chemin_log)
    #print("séparation fichier : ",log_a_sep.name)
        
    #fichier_a_split = open(log_a_sep.name, "r+")
    fs = open(log_a_sep.name, "r")

    nb_ligne = 0
    lignes = []
    for line in fs:
        nb_ligne += 1
        lignes.append(line[29:])
    
    Nombre_de_fichier_a_creer = int((nb_ligne / taille_max_lignes))+1
    #print("nombre de fichier creer",log_a_sep.name,"     ",taille_fichier,"     ",Nombre_de_fichier_a_creer)
    #print("taill",taille_fichier)
    print("nombre de fichier a creer = ",Nombre_de_fichier_a_creer)


    for m in range(0,Nombre_de_fichier_a_creer):
        #print(m)
        contenu_x = ""
        nom = log_a_sep.name
        nom = nom.split(".")
        nb_underscore = nom[0].count("_")
        if ( nb_underscore == 2 or nb_underscore == 3):
            nom = nom[0].split("_")
            try:
                nom = nom[0] + "_" + nom[1] + "_" + nom[2] + "_" + nom[3] + "__part" + str(m)
            except:
                print("Structure du nom du fichier incorrect pour : ",log_a_sep.name)
        else:
            print("Structure du nom du fichier incorrect pour : ",log_a_sep.name)
        os.chdir(chemin_log_separer)
        fichier_creer = open(nom, "w")
        os.chdir(chemin_log)
        if m<Nombre_de_fichier_a_creer-1:
            for l in range((m)*taille_max_lignes,(m+1)*taille_max_lignes):
                contenu_x = contenu_x + lignes[l]

        else:
            for l in range((m)*taille_max_lignes,nb_ligne):
                contenu_x = contenu_x + lignes[l]
        
        fichier_creer.write(contenu_x)
        fichier_creer.close()
#_________________________________________________________________________________________________________________
#Fin de la def separation()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def Deplacement_fichier :
#Entrée : Fichier log
#Sortie : -Fichier texte avec les séquences 
##################################################################################################################
def Deplacement_fichier(taille_max):
    os.chdir(chemin_log)
    Folder_origine = os.listdir(chemin_log)

    taille_dossier = len(Folder_origine) 
    print("taille du dossier :",taille_dossier," fichier(s)")
    bar2 = ProgressBar(taille_dossier)
    for i in range(0, taille_dossier): 
        #print(os.path.getsize(Folder_origine[i]))
        if os.path.getsize(Folder_origine[i]) > taille_max:
            fichier_split = open(Folder_origine[i], "r")
            separation(fichier_split,taille_max)
            fichier_split.close()
        else:
            fichier_a_deplacer = open(Folder_origine[i], "r+")
            nom_fich_a_dep = fichier_a_deplacer.name
            nom_fich_a_dep = nom_fich_a_dep.split(".")
            nb_underscore = nom_fich_a_dep[0].count("_")
            if ( nb_underscore == 2 or nb_underscore == 3):
                nom_fich_a_dep = nom_fich_a_dep[0].split("_")
                try:
                    nom_fich_a_dep = nom_fich_a_dep[0] + "_" + nom_fich_a_dep[1] + "_" + nom_fich_a_dep[2] + "_" + nom_fich_a_dep[3]
                except:
                    print("Structure du nom du fichier incorrect pour : ",fichier_a_deplacer.name)
            else:
                print("Structure du nom du fichier incorrect pour : ",fichier_a_deplacer.name)
            contenu_a_deplacer = fichier_a_deplacer.read()
            os.chdir(chemin_log_separer)
            fichier_deplacer = open(nom_fich_a_dep, "w")
            fichier_deplacer.write(contenu_a_deplacer)
            fichier_a_deplacer.close()
            fichier_deplacer.close()
            os.chdir(chemin_log)
        bar2.update()
#_________________________________________________________________________________________________________________
#Fin de la def Deplacement_fichier()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def Selection_sequences_par_fichier :
#Entrée : Fichier log
#Sortie : -Fichier texte avec les séquences 
##################################################################################################################
def Selection_mot_par_fichier(log_selection,Nb_caractere_sortie):
    
    os.chdir(chemin)
    try:
        os.path.isdir("txts_sequences")
    except:
        print("dossier txts_sequences n'existe pas")


    os.chdir(chemin_log_separer)
    fichier_source = open(log_selection, "r+")
    
    #poids_dossier_log.append(os.path.getsize(log_selection))
    contenu = fichier_source.read().replace("(","").replace(")","").replace("{","").replace("}","").replace("[","").replace("]","").replace("<","").replace(">","").replace("	"," ")

    fichier_source.close()
    
    global Nombre_log_separe
    nb = Nombre_log_separe
    os.chdir(chemin_txts_sequences)
    nom_texte_sequence = "log" + str(nb) + ".txt"
    Nombre_log_separe = Nombre_log_separe + 1
    fichier_destination = open(nom_texte_sequence,"w+")
        
    fichier_destination.write(contenu)
    
    fichier_destination.close()
#_________________________________________________________________________________________________________________
#Fin de la def Selection_sequences_par_fichier()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def Selection_sequences_par_fichier :
#Entrée : Fichier log
#Sortie : -Fichier texte avec les séquences 
##################################################################################################################
def Selection_sequences_par_fichier_runer(log_selection,Nb_caractere_sortie,Nombre_de_sequence,chemin_donnee):
    print("________________________________________")
    print("Lecture de ",log_selection," en cours...")
    os.chdir(chemin_log_separer)
    fichier_source = open(log_selection, "r+")
    
    #poids_dossier_log.append(os.path.getsize(log_selection))
    contenu = fichier_source.read().replace("(","").replace(")","").replace("{","").replace("}","").replace("[","").replace("]","").replace("<","").replace(">","").replace("	"," ")

    fichier_source.close()
    
    return contenu

#_________________________________________________________________________________________________________________
#Fin de la def Selection_sequences_par_fichier()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def Ajout_reponse() :
#Entrée : Fichier txt avec sequences les plus courantes
#Sortie : -Fichier texte avec les séquences et les réponses
##################################################################################################################
def Ajout_reponse():
    os.chdir(chemin_txts_sequences)
    liste_txt_sequ = os.listdir(chemin_txts_sequences)
    Nombre_log_sep = len(liste_txt_sequ) 
    for i in range(0,Nombre_log_sep):
        os.chdir(chemin_txts_sequences)
        fichier_ouvert = open(liste_txt_sequ[i],"r")
        nb_ligne = 0
        lignes = []
        contenu_i = ""
        for line in fichier_ouvert:
            nb_ligne += 1
            lignes.append(line)
        for y in range(0,nb_ligne):
            ligne = lignes[y].split(" ")
            reponse = " --important--"
            for z in range(0,len(ligne)-1):
                if (ligne[z]=="info"):
                    reponse = " --pas important--"
                contenu_i = contenu_i + ligne[z] + " "
            contenu_i = contenu_i + reponse + "\n"
        fichier_ouvert.close()
        fichier_ouvert = open(liste_txt_sequ[i],"w")
        fichier_ouvert.write(contenu_i)
        fichier_ouvert.close()
#_________________________________________________________________________________________________________________
#Fin de la def Ajout_reponse()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def Creation_fichier_apprentissage() :
#Entrée : Fichier txt avec sequences les plus courantes
#Sortie : -Fichier texte avec les séquences et les réponses
##################################################################################################################
def Creation_fichier_apprentissage():
    print("Creation du fichier texte base d'apprentissage...")
    try:
        os.chdir(chemin)
        if (os.path.isdir("base_apprentissage_sequences.txt")):
            os.remove("base_apprentissage_sequences.txt")
        os.chdir(chemin_txts_sequences)
        liste_fichier_txt = os.listdir()
        Nombre_de_fichier_txt = len(liste_fichier_txt)
        base_apprentissage = ""
        for i in range(0,Nombre_de_fichier_txt):
            if (i<Nombre_de_fichier_txt-2):
                fichier_en_cours = open(liste_fichier_txt[i],"r+")
                contenu = fichier_en_cours.read()
                base_apprentissage = base_apprentissage + contenu
                fichier_en_cours.close()
            else:
                fichier_en_cours = open(liste_fichier_txt[i],"r+")
                contenu = fichier_en_cours.read()
                base_apprentissage = base_apprentissage + contenu
                fichier_en_cours.close()
        os.chdir(chemin)
        fichier_apprentissage = open("base_apprentissage_sequences.txt","w+")
        fichier_apprentissage.write(base_apprentissage)
        fichier_apprentissage.close()

        print("Base d'apprentissage crée avec succès")
    except:
        print("Erreur de création de la base d'apprentissage")
#_________________________________________________________________________________________________________________
#Fin de la def Creation_fichier_apprentissage()
#_________________________________________________________________________________________________________________



##################################################################################################################
#MAIN
################################################################################################################## 
def Main_base_apprentissage(Nb_seq,taille_max):
    print("#########################################################")
    print("Début du programme de création de la base d'apprentissage")
    print("#########################################################")
    
    ##################################################################################################################
    #variables globales
    ##################################################################################################################

    #heure de début du programme
    temps_calcul0 = time.clock()

    print("heure de début",temps_calcul0)

    os.chdir(chemin)
    creation_dossier_log_separer()
    creation_dossier_txts_sequences()

    try:
        print("------------------------------------")
        print("Déplacement des fichiers en cours...")
        print("------------------------------------")
        Deplacement_fichier(taille_max)
        print()
        print("*****************************")
        print("Fichiers déplacés avec succès")
        print("*****************************")
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Problème lors du déplacement des fichiers")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    try:
        print("--------------------------------")
        print("Lecture des fichiers en cours...")
        print("--------------------------------")
        os.chdir(chemin_log_separer)
        liste_log_sep = os.listdir(chemin_log_separer)
        Nombre_log = len(liste_log_sep)
        bar = ProgressBar(Nombre_log)
        for i in range(0,Nombre_log):
            Selection_mot_par_fichier(liste_log_sep[i],3)
            bar.update()
        print()
        print("***************************")
        print("Fin de lecture des fichiers")
        print("***************************")
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Problème lors de la lecture des fichiers")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    try:
        print("------------------------------")
        print("Ajout des réponses en cours...")
        print("------------------------------")
        Ajout_reponse()
        print("*****************************")
        print("Réponses ajoutées avec succès")
        print("*****************************")
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Problème lors de l'ajout des réponses")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    try:
        Creation_fichier_apprentissage()
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Problème lors de la création de la base d'apprentissage")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    #suppression_dossier_log_separer()
    #suppression_dossier_txts_sequences()

    #heure de fin du programme
    temps_calcul1 = time.clock()


    print("temps d'execution = ",temps_calcul1-temps_calcul0,)
    print("#######################################################")
    print("Fin du programme de création de la base d'apprentissage")
    print("#######################################################")


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
# | 1.0.0 |11/10/2018|  --  |  LGU  |  Création de l'algo pour lecture des différents types |
# +-----------------------------------------------------------------------------------------+
# | 1.0.1 |12/10/2018|  --  |  U  |  Selection des x premiers élements du log               |
# +--------------------------------------------------------------------------------------------------+
# | 2.0.0 |29/10/2018|  --  |  LU  |  Prendre les parties de 3 caractères de mots les plus fréquente  |
# +--------------------------------------------------------------------------------------------------+
# | 2.0.1 |07/11/2018|  --  |  G  |  Adaptation du nombre de caractère par sequence                  |
# +--------------------------------------------------------------------------------------------------+
# | 2.0.2 |12/11/2018|  --  |  G  |  Temps d'execution du programme en fonction du volume des fichiers
# +--------------------------------------------------------------------------------------------------+
# | 2.1.0 |15/11/2018|  --  |  G  |  remise en forme du code
# +--------------------------------------------------------------------------------------------------+
# | 2.1.1 |15/11/2018|  --  |  G  |  creation dossier pour séparation des logs
# +--------------------------------------------------------------------------------------------------+
# | 2.2.0 |16/11/2018|  --  |  LU  |  Ajout de la barre de progression et correction de bugs
# +--------------------------------------------------------------------------------------------------+
# | 2.2.1 |30/11/2018|  --  |  G  |  Correction bugs majeurs
# +--------------------------------------------------------------------------------------------------+

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
global chemin_txts_sequences_format
global chemin_txts_sequences_source

chemin = os.getcwd()
chemin_log = chemin + "/base_de_log"
chemin_log_separer = chemin + "/logs_séparer"
chemin_txts_sequences_format = chemin +"/txts_sequences_format"
chemin_txts_sequences_source = chemin +"/txts_sequences_source"
Nombre_log_separe = 0
Nombre_log_separe2 = 0
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
#Sortie : -Dossier de txts_sequences_format créé
##################################################################################################################
def creation_dossier_txts_sequences_format():
    os.chdir(chemin)
    if os.path.isdir("txts_sequences_format"):
        shutil.rmtree("txts_sequences_format")
        os.mkdir("txts_sequences_format")
    else:
        os.mkdir("txts_sequences_format")
#_________________________________________________________________________________________________________________
#Fin de la def creation_dossier_txts_sequences_format()
#_________________________________________________________________________________________________________________


##################################################################################################################
#Def creation_dossier_log_separer :
#Entrée : --
#Sortie : -Dossier de txts_sequences_source créé
##################################################################################################################
def creation_dossier_txts_sequences_source():
    os.chdir(chemin)
    if os.path.isdir("txts_sequences_source"):
        shutil.rmtree("txts_sequences_source")
        os.mkdir("txts_sequences_source")
    else:
        os.mkdir("txts_sequences_source")
#_________________________________________________________________________________________________________________
#Fin de la def creation_dossier_txts_sequences_source()
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
#Def suppression_dossier_txts_sequences_format :
#Entrée : --
#Sortie : -Dossier de txts_sequences_format supprimé
##################################################################################################################
def suppression_dossier_txts_sequences_format():
    print("Suppression dossier txts_sequences_format en cours ...")
    os.chdir(chemin)
    shutil.rmtree("txts_sequences_format")
    print("Dossier txts_sequences_format supprimé")
#_________________________________________________________________________________________________________________
#Fin de la def suppression_dossier_txts_sequences_format()
#_________________________________________________________________________________________________________________

##################################################################################################################
#Def suppression_dossier_txts_sequences_format :
#Entrée : --
#Sortie : -Dossier de txts_sequences_format supprimé
##################################################################################################################
def suppression_dossier_txts_sequences_source():
    print("Suppression dossier txts_sequences_source en cours ...")
    os.chdir(chemin)
    shutil.rmtree("txts_sequences_source")
    print("Dossier txts_sequences_source supprimé")
#_________________________________________________________________________________________________________________
#Fin de la def suppression_dossier_txts_sequences_source()
#_________________________________________________________________________________________________________________




##################################################################################################################
#Def separation :
#Entrée : Fichier log à séparer
#Sortie : -Fichier séparer en plusieurs fichiers au même endroit que le fichier d'origine
#         -Fichier d'origine supprimé
##################################################################################################################
def separation(log_a_sep,taille_max):
    os.chdir(chemin)
    try:
        os.path.isdir("logs_séparer")
    except:
        print("dossier logs_séparer n'existe pas")

    os.chdir(chemin_log)
    #print("séparation fichier : ",log_a_sep.name)
        
    fichier_a_split = open(log_a_sep.name, "r+")
    contenu_a_split = fichier_a_split.read()
    taille_fichier = len(contenu_a_split)
    Nombre_de_fichier_a_creer = int((taille_fichier / taille_max))+1
    #print("nombre de fichier creer",log_a_sep.name,"     ",taille_fichier,"     ",Nombre_de_fichier_a_creer)
    #print("taill",taille_fichier)
    print("nombre de fichier a creer = ",Nombre_de_fichier_a_creer)
    for m in range(0,Nombre_de_fichier_a_creer):
        #print(m)
        nom = log_a_sep.name
        nom = nom.split(".")
        nb_underscore = nom[0].count("_")
        if ( nb_underscore == 2 or nb_underscore == 3):
            nom = nom[0].split("_")
            try:
                nom = nom[0] + "_" + nom[1] + "_" + nom[2] + ".part" + str(m)
            except:
                print("Structure du nom du fichier incorrect pour : ",log_a_sep.name)
        else:
            print("Structure du nom du fichier incorrect pour : ",log_a_sep.name)
        os.chdir(chemin_log_separer)
        fichier_creer = open(nom, "w")
        os.chdir(chemin_log)
        if m<Nombre_de_fichier_a_creer-1:
            contenu_x = contenu_a_split[m*taille_max:((m+1)*taille_max)-1]

        else:
            contenu_x = contenu_a_split[m*taille_max:((m+1)*taille_max)-1] + contenu_a_split[(m+1)*taille_max:]
        
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
            nom_fich = fichier_split.name
            fichier_split.close()
        else:
            fichier_a_deplacer = open(Folder_origine[i], "r+")
            nom_fich_a_dep = fichier_a_deplacer.name
            nom_fich_a_dep = nom_fich_a_dep.split(".")
            nb_underscore = nom_fich_a_dep[0].count("_")
            if nb_underscore == 2 or nb_underscore==3:
                nom_fich_a_dep = nom_fich_a_dep[0].split("_")
                try:
                    nom_fich_a_dep = nom_fich_a_dep[0] + "_" + nom_fich_a_dep[1] + "_" + nom_fich_a_dep[2] 
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
#Fin de la def Selection_sequences_par_fichier()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def Selection_sequences_par_fichier :
#Entrée : Fichier log
#Sortie : -Fichier texte avec les séquences 
##################################################################################################################
def Selection_sequences_par_fichier(log_selection,Nb_caractere_sortie,Nombre_de_sequence):
    
    os.chdir(chemin)
    try:
        os.path.isdir("txts_sequences_format")
    except:
        print("dossier txts_sequences_format n'existe pas")


    os.chdir(chemin_log_separer)
    fichier_source = open(log_selection, "r+")
    
    #poids_dossier_log.append(os.path.getsize(log_selection))
    contenu = fichier_source.read().replace(" ",",").replace("\n",",").replace("	",",").replace(",,",",").replace(",,",",").replace(",,",",").replace(",,",",")
    new_contenu = ""
    mots = contenu.split(",")
    fichier_source.close()

    for m in range(0,len(mots)-2):
        mot=mots[m]
        if len(mot)<Nb_caractere_sortie:
            new_contenu = new_contenu + mot + ","
        else:
            partie_mot = len(mot)- Nb_caractere_sortie + 1
            for y in range(0,partie_mot):
                new_contenu = new_contenu + mot[y:y+Nb_caractere_sortie] + ","

    new_contenu = new_contenu.split(",")                
    dictionary = Counter(new_contenu)
    most_common = dictionary.most_common(Nombre_de_sequence)
    global Nombre_log_separe
    nb = Nombre_log_separe
    os.chdir(chemin_txts_sequences_format)
    nom_texte_sequence = "log" + str(nb) + ".txt"
    Nombre_log_separe = Nombre_log_separe + 1
    fichier_destination = open(nom_texte_sequence,"w+")
    
    for j in range (0,Nombre_de_sequence):
        new_contenu = most_common[j][0]
        new_contenu = new_contenu + ','
        fichier_destination.write(new_contenu)
    
    fichier_destination.close()
#_________________________________________________________________________________________________________________
#Fin de la def Selection_sequences_par_fichier()
#_________________________________________________________________________________________________________________


##################################################################################################################
#Def Selection_sequences_par_fichier :
#Entrée : Fichier log
#Sortie : -Fichier texte avec les séquences 
##################################################################################################################
def Selection_sequences_par_fichier_source(log_selection,Nb_caractere_sortie,Nombre_de_sequence):
    
    os.chdir(chemin)
    try:
        os.path.isdir("txts_sequences_source")
    except:
        print("dossier txts_sequences_source n'existe pas")


    os.chdir(chemin_log_separer)
    fichier_source = open(log_selection, "r+")
    
    #poids_dossier_log.append(os.path.getsize(log_selection))
    contenu = fichier_source.read().replace(" ",",").replace("\n",",").replace("	",",").replace(",,",",").replace(",,",",").replace(",,",",").replace(",,",",")
    new_contenu = ""
    mots = contenu.split(",")
    fichier_source.close()

    for m in range(0,len(mots)-2):
        mot=mots[m]
        if len(mot)<Nb_caractere_sortie:
            new_contenu = new_contenu + mot + ","
        else:
            partie_mot = len(mot)- Nb_caractere_sortie + 1
            for y in range(0,partie_mot):
                new_contenu = new_contenu + mot[y:y+Nb_caractere_sortie] + ","

    new_contenu = new_contenu.split(",")                
    dictionary = Counter(new_contenu)
    most_common = dictionary.most_common(Nombre_de_sequence)
    global Nombre_log_separe2
    nb2 = Nombre_log_separe2
    os.chdir(chemin_txts_sequences_source)
    nom_texte_sequence = "log" + str(nb2) + ".txt"
    Nombre_log_separe2 = Nombre_log_separe2 + 1
    fichier_destination = open(nom_texte_sequence,"w+")
    
    for j in range (0,Nombre_de_sequence):
        new_contenu = most_common[j][0]
        new_contenu = new_contenu + ','
        fichier_destination.write(new_contenu)
    
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
    os.chdir(chemin_donnee)
    fichier_source = open(log_selection, "r+")
    
    #poids_dossier_log.append(os.path.getsize(log_selection))
    contenu = fichier_source.read().replace(" ",",").replace("\n",",").replace("	",",").replace(",,",",").replace(",,",",").replace(",,",",").replace(",,",",")
    new_contenu = ""
    mots = contenu.split(",")
    fichier_source.close()
    bar3 = ProgressBar(len(mots)-2)
    for m in range(0,len(mots)-2):
        mot=mots[m]
        if len(mot)<Nb_caractere_sortie:
            new_contenu = new_contenu + mot + ","
        else:
            partie_mot = len(mot)- Nb_caractere_sortie + 1
            for y in range(0,partie_mot):
                new_contenu = new_contenu + mot[y:y+Nb_caractere_sortie] + ","
        bar3.update()

    new_contenu = new_contenu.split(",")                
    dictionary = Counter(new_contenu)
    most_common = dictionary.most_common(Nombre_de_sequence)
    sequences_ = ""
    for j in range (0,Nombre_de_sequence):
        if j < Nombre_de_sequence-1:
            new_contenu = most_common[j][0] + ','
        else:
            new_contenu = most_common[j][0]
        sequences_ = sequences_ + new_contenu
    os.remove(log_selection)
    return sequences_

#_________________________________________________________________________________________________________________
#Fin de la def Selection_sequences_par_fichier()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def Ajout_reponse_format() :
#Entrée : Fichier txt avec sequences les plus courantes
#Sortie : -Fichier texte avec les séquences et les réponses
##################################################################################################################
def Ajout_reponse_format():
    
    os.chdir(chemin_log_separer)
    liste_sep = os.listdir(chemin_log_separer)
    os.chdir(chemin_txts_sequences_format)
    liste_txt_sequ = os.listdir(chemin_txts_sequences_format)
    Nombre_log_sep = len(liste_txt_sequ) 
    for i in range(0,Nombre_log_sep):

        os.chdir(chemin_log_separer)
        fichier_ouvert = open(liste_sep[i],"r+")
        nom = fichier_ouvert.name
        nom = nom.split(".")
        nom = nom[0].split("_")
        reponse = nom[2].upper()
        fichier_ouvert.close()
        os.chdir(chemin_txts_sequences_format)
        fichier_ouvert = open(liste_txt_sequ[i],"r+")
        contenu_sequence = fichier_ouvert.read()
        fichier_ouvert.close()
        fichier_ouvert = open(liste_txt_sequ[i],"w+")
        contenu_avec_reponse = contenu_sequence + "--" + reponse + "--"
        fichier_ouvert.write(contenu_avec_reponse)
        fichier_ouvert.close()
#_________________________________________________________________________________________________________________
#Fin de la def Ajout_reponse_format()
#_________________________________________________________________________________________________________________

##################################################################################################################
#Def Ajout_reponse_format() :
#Entrée : Fichier txt avec sequences les plus courantes
#Sortie : -Fichier texte avec les séquences et les réponses
##################################################################################################################
def Ajout_reponse_source():
    
    os.chdir(chemin_log_separer)
    liste_sep = os.listdir(chemin_log_separer)
    os.chdir(chemin_txts_sequences_source)
    liste_txt_sequ = os.listdir(chemin_txts_sequences_source)
    Nombre_log_sep = len(liste_txt_sequ) 
    for i in range(0,Nombre_log_sep):

        os.chdir(chemin_log_separer)
        fichier_ouvert = open(liste_sep[i],"r+")
        nom = fichier_ouvert.name
        nom = nom.split(".")
        nom = nom[0].split("_")
        reponse = nom[1].upper()
        fichier_ouvert.close()
        os.chdir(chemin_txts_sequences_source)
        fichier_ouvert = open(liste_txt_sequ[i],"r+")
        contenu_sequence = fichier_ouvert.read()
        fichier_ouvert.close()
        fichier_ouvert = open(liste_txt_sequ[i],"w+")
        contenu_avec_reponse = contenu_sequence + "--" + reponse + "--"
        fichier_ouvert.write(contenu_avec_reponse)
        fichier_ouvert.close()
#_________________________________________________________________________________________________________________
#Fin de la def Ajout_reponse_source()
#_________________________________________________________________________________________________________________


##################################################################################################################
#Def Creation_fichier_apprentissage_format() :
#Entrée : Fichier txt avec sequences les plus courantes
#Sortie : -Fichier texte avec les séquences et les réponses
##################################################################################################################
def Creation_fichier_apprentissage_format():
    print("Creation du fichier texte base d'apprentissage...")
    try:
        os.chdir(chemin)
        if (os.path.isdir("base_apprentissage_sequences_format.txt")):
            os.remove("base_apprentissage_sequences_format.txt")
        os.chdir(chemin_txts_sequences_format)
        liste_fichier_txt = os.listdir()
        Nombre_de_fichier_txt = len(liste_fichier_txt)
        base_apprentissage = ""
        for i in range(0,Nombre_de_fichier_txt):
            if (i<Nombre_de_fichier_txt-1):
                fichier_en_cours = open(liste_fichier_txt[i],"r+")
                contenu = fichier_en_cours.read()
                base_apprentissage = base_apprentissage + contenu + "\n"
            else:
                fichier_en_cours = open(liste_fichier_txt[i],"r+")
                contenu = fichier_en_cours.read()
                base_apprentissage = base_apprentissage + contenu
            fichier_en_cours.close()

        os.chdir(chemin)
        fichier_apprentissage = open("base_apprentissage_sequences_format.txt","w+")
        fichier_apprentissage.write(base_apprentissage)
        fichier_apprentissage.close()
        print("Base d'apprentissage FORMAT crée avec succès")
    except:
        print("Erreur de création de la base d'apprentissage")
#_________________________________________________________________________________________________________________
#Fin de la def Creation_fichier_apprentissage()
#_________________________________________________________________________________________________________________

##################################################################################################################
#Def Creation_fichier_apprentissage_source() :
#Entrée : Fichier txt avec sequences les plus courantes
#Sortie : -Fichier texte avec les séquences et les réponses
##################################################################################################################
def Creation_fichier_apprentissage_source():
    print("Creation du fichier texte base d'apprentissage...")
    try:
        os.chdir(chemin)
        if (os.path.isdir("base_apprentissage_sequences_source.txt")):
            os.remove("base_apprentissage_sequences_source.txt")
        os.chdir(chemin_txts_sequences_source)
        liste_fichier_txt = os.listdir()
        Nombre_de_fichier_txt = len(liste_fichier_txt)
        base_apprentissage = ""
        for i in range(0,Nombre_de_fichier_txt):
            if (i<Nombre_de_fichier_txt-1):
                fichier_en_cours = open(liste_fichier_txt[i],"r+")
                contenu = fichier_en_cours.read()
                base_apprentissage = base_apprentissage + contenu + "\n"
            else:
                fichier_en_cours = open(liste_fichier_txt[i],"r+")
                contenu = fichier_en_cours.read()
                base_apprentissage = base_apprentissage + contenu
            fichier_en_cours.close()

        os.chdir(chemin)
        fichier_apprentissage = open("base_apprentissage_sequences_source.txt","w+")
        fichier_apprentissage.write(base_apprentissage)
        fichier_apprentissage.close()
        print("Base d'apprentissage SOURCE crée avec succès")
    except:
        print("Erreur de création de la base d'apprentissage")
#_________________________________________________________________________________________________________________
#Fin de la def Creation_fichier_apprentissage_source()
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
    creation_dossier_txts_sequences_format()
    creation_dossier_txts_sequences_source()

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
        print("Lecture des fichiers FORMAT en cours...")
        print("--------------------------------")
        os.chdir(chemin_log_separer)
        liste_log_sep = os.listdir(chemin_log_separer)
        Nombre_log = len(liste_log_sep)
        bar = ProgressBar(Nombre_log)
        for i in range(0,Nombre_log):
            Selection_sequences_par_fichier(liste_log_sep[i],3,Nb_seq)
            bar.update()
        print()
        print("***************************")
        print("Fin de lecture des fichiers FORMAT")
        print("***************************")
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Problème lors de la lecture des fichiers FORMAT")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    try:
        print("--------------------------------")
        print("Lecture des fichiers SOURCE en cours...")
        print("--------------------------------")
        os.chdir(chemin_log_separer)
        liste_log_sep = os.listdir(chemin_log_separer)
        Nombre_log = len(liste_log_sep)
        bar = ProgressBar(Nombre_log)
        for i in range(0,Nombre_log):
            Selection_sequences_par_fichier_source(liste_log_sep[i],3,Nb_seq)
            bar.update()
        print()
        print("***************************")
        print("Fin de lecture des fichiers SOURCE")
        print("***************************")
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Problème lors de la lecture des fichiers SOURCE")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    try:
        print("------------------------------")
        print("Ajout des réponses en cours...")
        print("------------------------------")
        Ajout_reponse_format()
        Ajout_reponse_source()
        print("*****************************")
        print("Réponses ajoutées avec succès")
        print("*****************************")
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Problème lors de l'ajout des réponses")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    try:
        Creation_fichier_apprentissage_format()
        Creation_fichier_apprentissage_source()
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Problème lors de la création de la base d'apprentissage")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    faire = input("Faire la suppression des fichiers -> yes or no\n")
    if (faire == "y" or faire == "yes"):
        suppression_dossier_log_separer()
        suppression_dossier_txts_sequences_format()
        suppression_dossier_txts_sequences_source()

    #heure de fin du programme
    temps_calcul1 = time.clock()


    print("temps d'execution = ",temps_calcul1-temps_calcul0,)
    print("#######################################################")
    print("Fin du programme de création de la base d'apprentissage")
    print("#######################################################")


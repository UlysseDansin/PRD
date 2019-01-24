
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# DESCRIPTION DU CODE - Applicatif machine learning (predictions)
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# ENTREES :  - 2 programmes:
#                   *Creation_base_apprentissage_2.py
#                   *ML_formats.py
#           -Fichier model.h5 (contient les poids du modèle sauvegarder)
## %%%%----------------------------------------------------------------------------------%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# SORTIES :  - Prédiction du format
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
# | 1.0.0 |30/11/2018|  --  |  G  |  Import et début
# +-----------------------------------------------------------------------------------------+
# | 1.1.0 |05/12/2018|  --  |  L  |  ajout de loaded_model_json en provenance ML_format
# +-----------------------------------------------------------------------------------------+
# | 1.2.0 |21/01/2019|  --  |  G  |  independance par rapport aux autres scripts et tri des logs inconnus


##################################################################################################################
#Import
##################################################################################################################
import os
import numpy
import pandas
import keras
import time
import sys 
from math import *
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn import model_selection
from keras.models import Sequential
from keras.layers import Dense
from keras.models import *
from keras import *
import matplotlib.pyplot as plt
from keras.models import model_from_json


Nb_cara_par_seq = 3
Nb_seq = 50

chemin = os.path.dirname(os.path.abspath(__file__))
chemin_log = chemin + "/base_de_log"
chemin_log_separer = chemin + "/logs_séparer"
chemin_txts_sequences = chemin +"/txts_sequences"
chemin_log_inconnu = chemin +"/Logs_inconnus"
chemin_donnee_entree = chemin + "/Donnee_entree"
os.chdir(chemin_donnee_entree)
liste_log_entree = os.listdir()




def def_vocab_to_int():
        chemin2 = chemin + '/base_de_log'
        
        # Filter : Select only c file
        Folder_origine = os.listdir(chemin2)                          
        all_file_name = numpy.array([f for f in Folder_origine])

        content = ""
        for name in all_file_name:
                with open(os.path.join(chemin2, name), "r") as f:
                        content += f.read() + "\n"

        # Convert the string into a list of interger
        vocab = set(content)
        vocab_to_int_ = {c: i for i, c in enumerate(vocab,1)}
        int_to_vocab = dict(enumerate(vocab))
        return vocab_to_int_


def codage_runer(seq,nb_seq):     
        
        data_no = seq
        data = data_no.split("\n")
        nombre_de_ligne = len(data)
        vocab_to_int = def_vocab_to_int()

        
        #encoded = np.array([vocab_to_int[c] for c in content], dtype=np.int32)
        def encodage(def_data):
                encoded = numpy.array([vocab_to_int[c] for c in def_data], dtype=numpy.long)
                return(encoded)

        #print("dictionnaire = ",vocab_to_int)



        ##################################################################################################################
        #Definition du mini_encoded taille des lignes pour Data_matrix
        ##################################################################################################################
        liste_e = []
        for x in range(0,nombre_de_ligne):
                nb = len(data[x])
                liste_e.append(nb)
        #print("liste_encoded =",liste_e)
        mini_encoded = min(liste_e)
        #print("data = ",data)
        #print("mini_encoded = ",mini_encoded)
        #*****************************************************************************************************************

        ##################################################################################################################
        #Creation de la matrice Data_matrix_mot_int
        ##################################################################################################################
        Data_matrix_mot_int = numpy.zeros((nombre_de_ligne,nb_seq), dtype =numpy.long)
        #*****************************************************************************************************************

        ##################################################################################################################
        #Creation de Data_matrix_int (matrice de caractères encodés en int) et Creation de la matrice Data_matrix_mot_int (multiplication des int d'encodage de chaque caractère d'un mot)
        ##################################################################################################################
        Data_matrix_int = numpy.zeros((nombre_de_ligne,mini_encoded), dtype=numpy.int)
        val_aide = 1000
        for x in range(0,nombre_de_ligne):

                ligne = data[x].split(",")
                
                liste_mot = []
                for y in range(0,nb_seq):
                        liste_mot.append(encodage(ligne[y]))
                
                #print(liste_mot)
                i=0
                i_liste=0
                while i_liste<(nb_seq) and (i+len(liste_mot[i_liste]))<mini_encoded: 
                        mot_int = 1
                        for g in range(0, len(liste_mot[i_liste])):
                                Data_matrix_int[x][i+g]=liste_mot[i_liste][g]
                                mot_int = mot_int * liste_mot[i_liste][g]
                                if (mot_int < 0):
                                        mot_int = mot_int + val_aide
                                else:
                                        mot_int = mot_int - val_aide

                        i=i+len(liste_mot[i_liste])
                        Data_matrix_mot_int[x][i_liste] = mot_int
                        i_liste=i_liste+1
                
                
                        
        #print(Data_matrix_int, "= Data_matrix_int")
        #print(Data_matrix_mot_int, "= Data_matrix_mot_int")
        #*****************************************************************************************************************

        ##################################################################################################################
        #Creation de la liste de résultat d'affichage
        ##################################################################################################################
        liste_affi = numpy.chararray(nombre_de_ligne, itemsize=9)
        for x in range(0,nombre_de_ligne):
                ligne = data[x].split(",")
                liste_affi[x] = ligne[len(ligne)-2]
        ##################################################################################################################
        #Creation de la matrice de résultat z
        ##################################################################################################################

        Dm = Data_matrix_int.shape
        n = Dm[0]
        #print(Dm)

        #print(z)
        #*****************************************************************************************************************

        ##################################################################################################################
        # répétition du nombre de boucle d'apprentissage et de test
        ##################################################################################################################


        ##################################################################################################################
        # Séparation base d'apprentissage/base de test
        ##################################################################################################################
        X=Data_matrix_mot_int
        #print(Data_matrix_int,"Data_matrix_int")
        #print(Data_matrix_mot_int,"Data_matrix_mot_int")
        return X








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
    return sequences_

#_________________________________________________________________________________________________________________
#Fin de la def Selection_sequences_par_fichier()
#_________________________________________________________________________________________________________________



##################################################################################################################
#Def creation_dossier_log_separer :
#Entrée : --
#Sortie : -Dossier de log séparer créé
##################################################################################################################
def deplacement_log_inconnu(new_log):
    os.chdir(chemin + "/Donnee_entree")
    file_new_log = open(new_log,"r+")
    contenu_new_log = file_new_log.read()
    file_new_log.close()
    os.remove(new_log)
    os.chdir(chemin_log_inconnu)
    nombre_log_inconnu = len(os.listdir(chemin_log_inconnu)) + 1
    nom_inconnu = "--INCONNU_" + str(nombre_log_inconnu) + "--.txt"
    file_new_log_destination = open(nom_inconnu,"w+")
    file_new_log_destination.write(contenu_new_log)
    file_new_log_destination.close()

        
#_________________________________________________________________________________________________________________
#Fin de la def creation_dossier_log_separer()
#_________________________________________________________________________________________________________________






try:
    os.chdir(chemin)
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)

    model.load_weights("model.h5")
    print("poids et modèle importé avec succès")

except:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("l'importation des poids ou du modèle a échoué : fichier introuvable")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")





compteur = 0

while True:


    os.chdir(chemin_donnee_entree)
    liste_ = os.listdir(chemin_donnee_entree)

    if len(liste_)!=0:
        
    
        try:
            sequences = Selection_sequences_par_fichier_runer(liste_[0],Nb_cara_par_seq,Nb_seq,chemin_donnee_entree)
            print()
            print("Séléction des séquences effectuée avec succès")
        except: 
            print()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Problème lors de la séléction des séquences")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            
        try:
            cod = codage_runer(sequences,Nb_seq)
            print("codage des séquences effectué avec succès")
        except: 
            print()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Problème lors du codage des séquences")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            #prediction = model.predict_classes(cod)
            prediction_format = Model.predict(model,cod)
            print("Prédiction effectuée avec succès")
            print("Prédiction : ",prediction_format)
            """
            if (prediction[0]==0):
                print("Prediction: [APACHE_LOG]")
            elif (prediction[0]==1):
                print("Prediction: [APACHE_XML]")
            else:
                print("Prediction: [APACHE_JSON]")
            """
        except:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Problème lors de la prédiction du format")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        liste_prediction = []
        for i in range(0,len(prediction_format[0])):
            liste_prediction.append(prediction_format[0][i])
        if liste_prediction.index(max(liste_prediction)) == 11 and liste_prediction[11]>65:
            #ajout d'un neurone

            try: 
                
                deplacement_log_inconnu(liste_[0])
                print("Déplacement du log inconnu : ",""," effectué avec succès vers le dossier ",os.getcwd())
            except:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Problème lors du déplacement du log inconnu")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        else:
            #sortir le plus haut
            prediction_max = max(liste_prediction)
            source = liste_prediction.index(prediction_max)
            print("prediction_max = ",prediction_max)
            print("source = ",source)
    else:
        if compteur % 5 == 0:
            print("Dossier vide.")
        elif compteur % 5 == 1:
            print("Dossier vide..")
        elif compteur % 5 == 2:
            print("Dossier vide...")
        elif compteur % 5 == 3:
            print("Dossier vide....")
        elif compteur % 5 == 4:
            print("Dossier vide.....")
        compteur += 1
        if compteur == 100:
            compteur = 0
    time.sleep(3)

print("################")
print("Fin du programme")
print("################")
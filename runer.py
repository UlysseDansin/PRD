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
# | 1.1.0 |05/12/2018|  --  |  L  |  Ajout de loaded_model_json en provenance ML_format     |
# +-----------------------------------------------------------------------------------------+
# | 1.2.0 |21/12/2018| -- | U | Ajout de ML source  avec adaptation du code                 |
# +-----------------------------------------------------------------------------------------+


##################################################################################################################
#Import
##################################################################################################################
import os
import numpy
import pandas
import keras
import time
from sklearn.preprocessing import StandardScaler
from sklearn import model_selection
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.models import model_from_json
import Creation_base_apprentissage_2 as crea
import ML_formats as ml





Nb_cara_par_seq = 3
Nb_seq = 50
chemin_racine = os.getcwd()
chemin_donnee_entree = chemin_racine + "/donnee_entree"
os.chdir(chemin_donnee_entree)
liste_log_entree = os.listdir()

"""
model = Sequential()
        # architecture
        # premiere couche
model.add(Dense(units=2000,input_dim=Nb_seq,activation="relu"))
model.add(Dense(units=1000,input_dim=2000,activation="relu"))
model.add(Dense(units=500,input_dim=1000,activation="relu"))
#keras.layers.Dropout(0.1)
model.add(Dense(units=3,input_dim=500,activation="softmax"))
"""
try:
    os.chdir(chemin_racine)
    json_file = open('model_format.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model_format = model_from_json(loaded_model_json)

    model_format.load_weights("model_format.h5")
    print("poids et modèle importé avec succès")
except:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("l'importation des poids ou du modèle FORMAT a échoué : fichier introuvable")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

try:
    os.chdir(chemin_racine)
    json_file = open('model_source.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model_source = model_from_json(loaded_model_json)

    model_source.load_weights("model_source.h5")
    print("poids et modèle importé avec succès")
except:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("l'importation des poids ou du modèle SOURCE a échoué : fichier introuvable")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


compteur = 0
while True:
    os.chdir(chemin_donnee_entree)
    liste_ = os.listdir(chemin_donnee_entree)
    if len(liste_)!=0:
        for i in range(len(liste_)):
            try:
                sequences = crea.Selection_sequences_par_fichier_runer(liste_[i],Nb_cara_par_seq,Nb_seq,chemin_donnee_entree)
                print()
                print("Séléction des séquences effectuée avec succès")
            except: 
                print()
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Problème lors de la séléction des séquences")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            try:
                cod,z = ml.codage(sequences,Nb_seq)
                print()
                print("codage des séquences effectué avec succès")
            except: 
                print()
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Problème lors de le codage des séquences FORMAT")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                
            try:
                prediction_format = model_format.predict_classes(cod)
                print("Prédiction effectuée avec succès")
                print("Prédiction FORMAT : ",prediction_format)
                if (prediction_format[0]==0):
                    print("Prediction: [XML]")
                elif (prediction_format[0]==1):
                    print("Prediction: [LOG]")
                else:
                    print("Prediction: [JSON]")

            except:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Problème lors de la prédiction du format")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            try:
                prediction_source = model_source.predict_classes(cod)
                print("Prédiction effectuée avec succès")
                print("Prédiction SOURCE : ",prediction_source)
                if (prediction_source[0]==0):
                    print("Prediction: [APACHE]")
                elif (prediction_source[0]==1):
                    print("Prediction: [IIS]")
                else:
                    print("Prediction: [WINDOWS]")
            except:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Problème lors de la prédiction du format")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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
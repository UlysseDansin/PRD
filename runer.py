
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
from keras.models import *
from keras import *
import matplotlib.pyplot as plt
from keras.models import model_from_json
import Creation_base_apprentissage_2 as crea
from ML_formats import Ajout_neurone
from ML_formats import codage
from ML_formats import Main_machine_learning
from ML_formats import liste_neurone

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
import_model_runer = True
compteur = 0
while True:


    os.chdir(chemin_donnee_entree)
    liste_ = os.listdir(chemin_donnee_entree)

    if import_model_runer: 
            try:
                os.chdir(chemin_racine)
                json_file = open('model.json', 'r')
                loaded_model_json = json_file.read()
                json_file.close()
                model = model_from_json(loaded_model_json)

                model.load_weights("model.h5")
                print("poids et modèle importé avec succès")
                import_model_runer = False
            except:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("l'importation des poids ou du modèle a échoué : fichier introuvable")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        pass
    if len(liste_)!=0:
        
    
        try:
            sequences = crea.Selection_sequences_par_fichier_runer(liste_[0],Nb_cara_par_seq,Nb_seq,chemin_donnee_entree)
            print()
            print("Séléction des séquences effectuée avec succès")
        except: 
            print()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Problème lors de la séléction des séquences")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            
        try:
            cod,z = codage(sequences,Nb_seq)
            print()
            print("codage des séquences effectué avec succès")
        except: 
            print()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Problème lors de le codage des séquences")
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
        if max(liste_prediction)<50:
            #ajout d'un neurone
            rep = input("yes or no")
            if (rep == "yes"):
                Ajout_neurone()
                print("ajout d'un nouveau neurone")
                Main_machine_learning(Nb_seq)
                import_model_runer = True
            else:
                print("non non non")
        else:
            #sortir le plus haut
            prediction_max = max(liste_prediction)
            source = liste_prediction.index(prediction_max)
            print("prediction_max = ",prediction_max)
            print("source = ",source)
        print("liste neurone = ",liste_neurone)
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
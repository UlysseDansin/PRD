## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# DESCRIPTION DU CODE - Utilisation de l'étiquetage et mise en forme des données
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# ENTREES : 
## %%%%----------------------------------------------------------------------------------%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# SORTIES :  - A voir
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
# | 1.0.0 |18/01/2019|  --  |  L  |  Adaptation au ML2                                      |
# +-----------------------------------------------------------------------------------------+
# | 1.0.0 |22/01/2019|  --  |  L  |  Data_matrix_mot_int avec padding "maison" et new z     |

# -*- coding: utf-8 -*

# importation des donnees

import os
import numpy
import pandas
import keras
from sklearn.preprocessing import StandardScaler
from sklearn import model_selection
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
import matplotlib.pyplot as plt
numpy.random.seed(7)
chemin_racine = os.getcwd()


liste_neurone = ["--WINDOWS_XML--","--CENTOS_SYSLOG--","--WINDOWS_APACHE_LOG4J--","--LINUX_APACHE_LOG4J--","--WINDOWS_IIS_CSV--","--WINDOWS_SHAREPOINT--","--WINDOWS_SCCM--","--WINDOWS_EXCHANGE--","--CENTOS_POSTFIX_SYSLOG--","--CENTOS_OPENLDAP_SYSLOG--","--ALFRESCO_LOG4J--","--Neurone_Inconnu--"]
Numero_inconnu = 0
nombre_neurone_sortie = len(liste_neurone)



def def_vocab_to_int():
        chemin2 = chemin_racine + '/base_de_log'
        
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


def codage(seq,Nb_mot_max):     
        
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
        #Creation de la matrice Data_matrix_mot_int
        ##################################################################################################################
        Data_matrix_mot_int = numpy.zeros((nombre_de_ligne-1,Nb_mot_max), dtype =numpy.long)
        #*****************************************************************************************************************

        ##################################################################################################################
        #Creation de Data_matrix_int (matrice de caractères encodés en int) et Creation de la matrice Data_matrix_mot_int (multiplication des int d'encodage de chaque caractère d'un mot)
        ##################################################################################################################
        #Data_matrix_int = numpy.zeros((nombre_de_ligne,mini_encoded), dtype=numpy.int)
        val_aide = 10000
        for x in range(0,nombre_de_ligne-1):
                ligne = data[x].split(" ")
                liste_mot = []
                for y in range(0,len(ligne)-1):
                        liste_mot.append(encodage(ligne[y]))
                        mot_int = 1
                        for g in range(0, len(liste_mot[y])):
                                mot_int = mot_int * liste_mot[y][g]
                                if (mot_int < 0):
                                        mot_int = mot_int + val_aide
                                else:
                                        mot_int = mot_int - val_aide
                        if (y<Nb_mot_max):
                                Data_matrix_mot_int[x][y] = mot_int


   
        #print(Data_matrix_int, "= Data_matrix_int")
        print(Data_matrix_mot_int, "= Data_matrix_mot_int")
        #*****************************************************************************************************************

        ##################################################################################################################
        #Creation de la liste de résultat d'affichage
        ##################################################################################################################
        liste_affi = numpy.chararray(nombre_de_ligne, itemsize=9)
        for x in range(0,nombre_de_ligne):
                ligne = data[x].split(" ")
                liste_affi[x] = ligne[len(ligne)-1]
        ##################################################################################################################
        #Creation de la matrice de résultat z
        ##################################################################################################################


        z=numpy.zeros((nombre_de_ligne-1,2))
        
        
        for i in range(0,nombre_de_ligne-1):
                ligne = data[i].split(" ")
                if  ligne[len(ligne)-1] == "--important--":
                        z[i,0]=1
                        z[i,1]=0
                else:
                        z[i,0]=0
                        z[i,1]=1

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
        return X,z

def Main_machine_learning(Nb_mot_max):
        print("#########################################################")
        print("Début du programme d'apprentissage")
        print("#########################################################")
        ##################################################################################################################
        # lecture et preparation des donnees
        ##################################################################################################################
        chemin1 = os.path.dirname(os.path.abspath(__file__)) + '/base_apprentissage_sequences.txt'
        chemin3 = os.path.dirname(os.path.abspath(__file__))
        raw_data = open(chemin1, 'rt')
        dat = raw_data.read()
  
        #print(t)
        X,z = codage(dat,Nb_mot_max)

        XTrain = X
        zTrain = z
        

        XTrain,XTest,zTrain,zTest = model_selection.train_test_split(X,z, test_size=1)
        #*****************************************************************************************************************

        
        # centrage-reduction des variables
        cr = StandardScaler(with_mean=True,with_std=True)
        #calcul des parametres + centrage reduction du train set
        
        XTrainStd = cr.fit_transform(XTrain)
        
        #print("comparaison des moyennes")
        #comparaison des moyennes, avant ...
        #print(numpy.mean(XTrain,axis=0))
        #... et apres CR (centrage-reduction)
        #print(numpy.mean(XTrainStd,axis=0))


        ##################################################################################################################
        # definition de l'architecture neuronale avec keras
        ##################################################################################################################
        # instanciation du modele

        # architecture
        # premiere couche
        model = Sequential()
        
        # architecture
        # premiere couche
        model.add(Dense(units=1000,input_dim=Nb_mot_max,activation="sigmoid"))
        model.add(Dense(units=500,input_dim=1000,activation="sigmoid"))
        model.add(Dense(units=250,input_dim=500,activation="sigmoid"))
        keras.layers.Dropout(0.1)
        model.add(Dense(units=2,input_dim=250,activation="sigmoid"))
        #*****************************************************************************************************************




        # compilation - algorithme d'apprentissage
        model.compile(loss="binary_crossentropy",optimizer="adam",metrics=["accuracy"])
        
        #model.compile(loss='mean_squared_error', optimizer="adam",metrics=["accuracy"])



        ##################################################################################################################
        # Apprentissage
        ##################################################################################################################
        # centrage-reduction des variables de l'echantillon test
        # avec (!) les parametres de l'echantillon d'apprentissage
        XTestStd = cr.transform(XTest)
        #vd = (XTestStd, yTest)
        
        history = model.fit(XTrainStd,zTrain,epochs=5,batch_size=20)#,validation_split=0.33)

        # poids synaptiques
        #print(model.get_weights())

        # list all data in history
        #print(history.history.keys())
        """
        # summarize history for accuracy
        # courbe de precision lors de l apprentissage
        plt.plot(history.history['acc'])
        # courbe de precision sur la base de test
        #plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        #plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        # summarize history for loss
        # courbe de cout lors de l apprentissage
        plt.plot(history.history['loss'])
        # courbe de cout sur la base de test
        #plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        #plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        """
        #*****************************************************************************************************************
        ##################################################################################################################
        # Sauvegarde du modele
        ##################################################################################################################
        try:
                os.chdir(chemin3)
                model_json = model.to_json()
                with open("model.json", "w") as json_file:
                        json_file.write(model_json)
                        
                model.save_weights("model.h5")
                print("poids et modèle de réseau de neurone enregistré avec succès!")
        except:
                print("Problème lors de la sauvegarde du modèle")
        
        #*****************************************************************************************************************

        

        ##################################################################################################################
        # Evaluation du modèle avec la base test
        ##################################################################################################################
        print("\n score sur la base de test (loss, accuracy)")
        
        score = model.evaluate(XTestStd,zTest)
        
        
        print(score[1])
        
        #*****************************************************************************************************************


        #print("dictionnaire", vocab_to_int)
        #print(Data_matrix_int, "= Data_matrix_int")
        #print("Matrice de mot en int = ",Data_matrix_mot_int) 
        print("\n")


        print("#########################################################")
        print("Fin du programme d'apprentissage")
        print("#########################################################")


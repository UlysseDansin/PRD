## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# DESCRIPTION DU CODE - Utilisation de l'étiquetage et mise en forme des données
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# ENTREES :  - Fichier en sortie de Spider nommé "ichier_test_sopra.txt" situé dans le même dossier que ce programme
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
# | 1.0.0 |11/10/2018|  --  |  U  | Création du code en copie de MLformat.py et avec quelques arrangements |
# +-----------------------------------------------------------------------------------------+

# -*- coding: utf-8 -*

# importation des donnees
import os
import numpy
import pandas
import keras
from sklearn.preprocessing import StandardScaler
from sklearn import model_selection
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
numpy.random.seed(7)
chemin_racine = os.getcwd()

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


def codage(seq,nb_seq):

        
        
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
        print(Data_matrix_mot_int, "= Data_matrix_mot_int")
        
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

        z=numpy.zeros((n,5))

        for i in range(0,nombre_de_ligne):
                ligne = data[i].split(",")
                print(ligne[len(ligne)-1])
                if  ligne[len(ligne)-1] == "--EVENT--": #windows
                        z[i,0]=1
                        z[i,1]=0
                        z[i,2]=0
                        z[i,3]=0
                        z[i,4]=0

                elif ligne[len(ligne)-1] == "--EVENEMENT--": #centos
                        z[i,0]=0
                        z[i,1]=2
                        z[i,2]=0
                        z[i,3]=0
                        z[i,4]=0

                elif ligne[len(ligne)-1] == "--APACHE24--":
                        z[i,0]=0
                        z[i,1]=0
                        z[i,2]=3
                        z[i,3]=0
                        z[i,4]=0


                elif ligne[len(ligne)-1] == "--AUDITD--":
                        z[i,0]=0
                        z[i,1]=0
                        z[i,2]=0
                        z[i,3]=4
                        z[i,4]=0

                elif ligne[len(ligne)-1] == "--SSHD--":
                        z[i,0]=0
                        z[i,1]=0
                        z[i,2]=0
                        z[i,3]=0
                        z[i,4]=5


        print(z)
        print("shape",numpy.shape(z))
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

def Main_machine_learning(Nb_de_most_common_word):
        print("#########################################################")
        print("Début du programme d'apprentissage SOURCE")
        print("#########################################################")
        ##################################################################################################################
        # lecture et preparation des donnees
        ##################################################################################################################
        chemin1 = os.getcwd() + '/base_apprentissage_sequences_source.txt'
        
        chemin3 = os.getcwd()
        raw_data = open(chemin1, 'rt')
        dat = raw_data.read()
  
        #print(t)
        X,z = codage(dat,Nb_de_most_common_word)

        XTrain = X
        zTrain = z
        #XTrain,XTest,zTrain,zTest = model_selection.train_test_split(X,z, test_size=1)
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
        model.add(Dense(units=1000,input_dim=Nb_de_most_common_word,activation="relu"))
        model.add(Dense(units=500,input_dim=1000,activation="relu"))
        model.add(Dense(units=250,input_dim=500,activation="relu"))
        keras.layers.Dropout(0.1)
        model.add(Dense(units=5,input_dim=250,activation="softmax"))
        #*****************************************************************************************************************




        # compilation - algorithme d'apprentissage
        model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
        
        #model.compile(loss='mean_squared_error', optimizer="adam",metrics=["accuracy"])



        ##################################################################################################################
        # Apprentissage
        ##################################################################################################################
        # centrage-reduction des variables de l'echantillon test
        # avec (!) les parametres de l'echantillon d'apprentissage
        #XTestStd = cr.transform(XTest)
        #vd = (XTestStd, yTest)
        
        history = model.fit(XTrainStd,zTrain,epochs=200,batch_size=10)#,validation_split=0.33)

        # poids synaptiques
        #print(model.get_weights())

        # list all data in history
        #print(history.history.keys())
        
        # summarize history for accuracy
        # courbe de precision lors de l apprentissage
        plt.plot(history.history['acc'])
        # courbe de precision sur la base de test
        

        #plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        # summarize history for loss
        # courbe de cout lors de l apprentissage
        plt.plot(history.history['loss'])
        # courbe de cout sur la base de test
        #plt.plot(history.history['val_loss'])

        #plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        
        #*****************************************************************************************************************
        ##################################################################################################################
        # Sauvegarde du modele
        ##################################################################################################################
        try:
                os.chdir(chemin3)
                model_source_json = model.to_json()
                with open("model_source.json", "w") as json_file:
                        json_file.write(model_source_json)
                        
                model.save_weights("model_source.h5")
                print("poids et modèle de réseau de neurone enregistré avec succès!")
        except:
                print("Problème lors de la sauvegarde du modèle")
        
        #*****************************************************************************************************************

        

        ##################################################################################################################
        # Evaluation du modèle avec la base test
        ##################################################################################################################
        print("\n score sur la base de test (loss, accuracy)")
        
        #score = model.evaluate(XTestStd,zTest)
        
        #*****************************************************************************************************************


        #print("dictionnaire", vocab_to_int)
        #print(Data_matrix_int, "= Data_matrix_int")
        #print("Matrice de mot en int = ",Data_matrix_mot_int) 
        print("\n")


        print("#########################################################")
        print("Fin du programme d'apprentissage SOURCE")
        print("#########################################################")
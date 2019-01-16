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
# | 1.0.0 |16/01/2019|  --  |  L  |  Début Mettre en avant les mots importants par "->"     |
# +-----------------------------------------------------------------------------------------+


##################################################################################################################
#imports
##################################################################################################################
import os
import sys 
from math import *
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
#_________________________________________________________________________________________________________________

##################################################################################################################
#Récupération logs
##################################################################################################################
os.chdir(chemin_log)
log_a_souligner = os.listdir(chemin_log)
liste_fichier = open("002_window_apache_log.log", "r+")
contenu = liste_fichier.read().replace(","," ").replace(",,"," ").replace(":"," ").replace("<"," ").replace(">"," ").replace("{"," ").replace("}"," ").replace("["," ").replace("]"," ").replace("	"," ")
liste_fichier.close()


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


log_test = contenu
log_split = log_test.split(" ")
log_final = ""
for i in range(0,len(log_split)):
    if (log_split[i] == "error"):
        log_final = log_final + "->" + log_split[i] + "<-" + " "
        #log_final = log_final + color.UNDERLINE + log_split[i] + color.END + " "
    else:
        log_final = log_final + log_split[i] + " "
    

os.chdir(chemin_txts_sequences)
fichier_destination = open("fichier_test.txt", "w+")

fichier_destination.write(log_final)
    
fichier_destination.close()
#print(len(log_test))
#print(len(log_split))
#print(len(log_final))


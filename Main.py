## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# DESCRIPTION DU CODE - Programme Main d'apprentissage (composition du modèle neuronal)
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# ENTREES :  - 2 programmes:
#                   *Creation_base_apprentissage_2.py
#                   *ML_formats.py
## %%%%----------------------------------------------------------------------------------%%%%

## %%%%----------------------------------------------------------------------------------%%%%
# SORTIES :  - Execution de l'ensemble
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
# | 1.0.0 |29/11/2018|  --  |  G  |  Import et applicatif


import os
import time
import shutil

import Creation_base_apprentissage_2 as crea
import ML_formats as ML_f
import ML_source as ML_s

Nb_seq = 10
taille_max_des_fichiers = 30000
crea.Main_base_apprentissage(Nb_seq,taille_max_des_fichiers)
ML_f.Main_machine_learning(Nb_seq)
ML_s.Main_machine_learning(Nb_seq)






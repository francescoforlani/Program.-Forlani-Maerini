# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 18:55:09 2022

@author: Franc
"""

from main_taxi import file_list_features

#  INTERFACCIA UTENTE


# ANALISI DEL PREZZO PER MIGLIO E DEL PREZZO PER MIGLIO PONDERATO DALLA DURATA DELLA CORSA
# DEI TAXI DI NYC PER BOROUGH


# INSERIRE IN my_data_path IL PERCORSO SU CUI SONO SALVATI I DATI
my_data_path = r'C:\Users\Franc\Desktop\progetto_programmazione\data'

#INSERIRE IN my_results_path IL PERCORSO SU CUI SI VOGLIONO SALVATI I RISULTATI
my_results_path = r'C:\Users\Franc\Desktop\progetto_programmazione\results'

# INSERIRE NELLA SEGUENTE LISTA I FILE DA ANALIZZARE, DEVONO ESSERE IN FORMATO .csv
dati = file_list_features(['yellow_tripdata_2020-04.csv'],
                           my_data_path, my_results_path)



# SE SI DESIDERA EFFETTUARE L'ANALISI SOLO SU SPECIFICI BOROUGH, 
# INSERIRE IL NOME DI QUET'ULTIMI NELLA SEGUENTE LISTA
# (NOMI CONSENTITI :Manhattan, Queens, Bronx, Brooklyn, Staten Island, EWR, Unknown)
# INOLTRE, SELEZIONARE SE SI VUOLE EFFETTUARE L'ANALISI CONSIDERANDO IL BOROUGH DI PARTENZA 
# DELLA CORSA (PU) O IL BOROUGH DI ARRIVO (DO)

dati = dati.list_features([], 'PU')



# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:23:18 2022

@author: Franc
"""


import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

# classe che viene istanziata dal main nel momento in cui si vuole effettuare
# il conteggio del prezzo al miglio e del prezzo al miglio ponderato dal tempo del viaggio 
# relativi alle corse dei taxi di NY 
# come input riceve la lista di file inserita dall'utente nell'interfaccia

class file_list_features:
    data_path = ''
    results_path = ''
    
    def __init__(self,list_of_file, data_path, results_path):
        self.list_of_file = list_of_file
        file_list_features.data_path = data_path
        file_list_features.results_path = results_path
         
    
    def list_features(self,Borough = [], PUorDO = str):
        col_list = ['LocationID','Borough']
        Borough_df = pd.read_csv (self.data_path + r'\taxi+_zone_lookup.csv',
                              usecols=col_list, delimiter=',')
        elenco_corse_df = pd.DataFrame()
        
        for filename in self.list_of_file:
            temp_df = Reader.get_lista_corse(filename)
            elenco_corse_df = pd.concat([elenco_corse_df,temp_df])
        
        #Amplio il database iniziale, aggiungendo il borough di partenza o di arrivo 
        #utilizzando rispettivamente il PULocationID o il DOLocationID, in base alla richiesta 
        #dell'utente
        if PUorDO == 'PU':
            Borough_df = Borough_df.rename(columns={'LocationID':'PULocationID'})
            input_data_df = pd.merge(elenco_corse_df, Borough_df, on='PULocationID', how="left")
            
        elif PUorDO == 'DO':
            Borough_df = Borough_df.rename(columns={'LocationID':'DOLocationID'})
            input_data_df = pd.merge(elenco_corse_df, Borough_df, on='DOLocationID', how="left")
            
        else:
            raise ValueError('String not recognized. Insert PU or DO.')
        
        # istanziato un oggetto della classe Standardizer relativo al Dataframe
        # in input
        std = Standardizer(input_data_df)
        input_data_df = std.elimina_righe_inutili()
        
        
        input_data_df["PM"] = np.nan
        input_data_df["PMT"] = np.nan
        input_data_df["trip_duration"] = np.nan
        
        # se non è stata inserita in ingresso una lista di Borough desiderati
        # di default il programma analizza tutte le corse su tutti i borough
        # calcolando PM e PMT per ogni corsa
        if Borough == []:
            Borough = input_data_df['Borough'].unique()              
            
            df_out= pd.DataFrame(columns=['Borough','mean_PM','std_PM', 'mean_PMT', 'std_PMT'])
            df_out['Borough'] = Borough
            
            #calcolo PM, trip_duration, PMT per ogni corsa e aggiungo le relative colonne al dataset
            input_data_df = std.aggiungo_PM_e_PMT(input_data_df)
            
            #Calcolo medie e deviazioni standard di PM e PMT per ogni borough
            df_out = std.calcolo_mean_e_std(Borough, input_data_df, df_out)

        else:
        # se è stata inerita una lista di Borough si riduce il Dataframe
        # in input eliminando tutti i borough non richiesti e si calcolano 
        # PM e PMT per ogni corsa di ogni borough rimasto
            input_data_df = std.elimina_Borough(Borough)
            df_out= pd.DataFrame(columns=['Borough','mean_PM','std_PM', 'mean_PMT', 'std_PMT'])
            df_out['Borough'] = Borough
            
            #calcolo PM, trip_duration, PMT per ogni corsa e aggiungo le relative colonne al dataset
            input_data_df = std.aggiungo_PM_e_PMT(input_data_df)
            
            #Calcolo medie e deviazioni standard di PM e PMT per ogni borough
            df_out = std.calcolo_mean_e_std(Borough, input_data_df, df_out)

        df_out.to_excel(self.results_path + r'/mean_std_of_PM_PMT.xls')
        plot_PM, plot_PMT = std.plotta(input_data_df)
        
        return df_out
  
    # ---------------------------------------------------------------------
    # lettura dei file in input

class Reader():
    
    def get_lista_corse(filename):
        data = pd.read_csv((file_list_features.data_path + r'/' + filename), delimiter=';')   
        return data

     # -------------------------------------------------------------------

# classe chiamata per pulire il dataset in input dalle righe non utili, per 
# aggiungere colonne utili ai fini del task e per fare i boxplot
class Standardizer():

    def __init__(self,df):
        self.df = df
           
    def elimina_righe_inutili(self):
            #Rimozione dalle righe con: 
            #RatecodeID != 1 (tariffe non standard che non ci interessano) 
            #trip_distance = 0 (non hanno senso)
            self.df = self.df.drop(self.df[self.df.RatecodeID != 1].index)
            self.df = self.df.drop(self.df[self.df.trip_distance == 0].index)
            #Rimozione di tutte le righe con valori Nan nelle colonne distanza e tariffa
            self.df = self.df.dropna(subset=['trip_distance','fare_amount'])
            return self.df
        
    def elimina_Borough(self,Borough):
        #Rimozione dal dataset dei borough non richiesti dall'utente
        self.df = self.df.set_index('Borough')
        self.df = self.df.loc[Borough]
        self.df = self.df.reset_index()
        return self.df
    
    def calcola_durata(self, start_datetime, end_datetime):
        #Calcolo della durata della corsa a partire dal pick up time e drop off time
        date_time_obj_start = datetime.datetime.strptime(start_datetime, '%d/%m/%Y %H:%M')
        date_time_obj_end = datetime.datetime.strptime(end_datetime, '%d/%m/%Y %H:%M')
        timedelta_obj = (date_time_obj_end - date_time_obj_start)
        minutes = timedelta_obj.seconds/60
        return minutes
    
    def calcola_PM(self, prezzo, distanza):
        #Calcolo del prezzo per miglio
        PM = prezzo/distanza
        return PM
    
    def calcola_PMT(self, PM, durata_corsa):
        #Calcolo del prezzo per miglio ponderato dalla durata della corsa
        PMT = PM/durata_corsa
        return PMT
    
    def aggiungo_PM_e_PMT(self, df):
        trip_duration = [None]*len(df)
        df_durations = pd.DataFrame(trip_duration)
        frames = [df, df_durations]
        df = pd.concat(frames, axis=1, join='inner')
        for index, row in df.iterrows():
            prezzo = df['fare_amount'][index]
            distanza = df['trip_distance'][index]
            df['PM'][index] = self.calcola_PM(prezzo,distanza)
            start = df['tpep_pickup_datetime'][index]
            end = df['tpep_dropoff_datetime'][index]
            df['trip_duration'][index] = self.calcola_durata(start,end)
            PM = df['PM'][index]
            durata_corsa = df['trip_duration'][index]
            df['PMT'][index] = self.calcola_PMT(PM,durata_corsa)
        return df
        
    def calcolo_mean_e_std(self, Borough, df_in, df_out_):
        for n in Borough:
            globals()["df_"+str(n)] = df_in.loc[df_in['Borough'] == n]
            arr_PM = globals()["df_"+str(n)]['PM']
            arr_PMT = globals()["df_"+str(n)]['PMT']
            globals()["mean_PM_"+str(n)] = np.mean(arr_PM[np.isfinite(arr_PM)])
            globals()["std_PM_"+str(n)] = np.std(arr_PM[np.isfinite(arr_PM)])
            globals()["mean_PMT_"+str(n)] = np.mean(arr_PMT[np.isfinite(arr_PMT)])
            globals()["std_PMT_"+str(n)] = np.std(arr_PMT[np.isfinite(arr_PMT)])
            df_out_['mean_PM'].loc[df_out_['Borough'] == n] = globals()["mean_PM_"+str(n)]
            df_out_['std_PM'].loc[df_out_['Borough'] == n] = globals()["std_PM_"+str(n)]
            df_out_['mean_PMT'].loc[df_out_['Borough'] == n] = globals()["mean_PMT_"+str(n)]
            df_out_['std_PMT'].loc[df_out_['Borough'] == n] = globals()["std_PMT_"+str(n)]
        return df_out_
        
    
    def plotta(self, dataframe):
        #Esecuzione boxplot delle distribuzioni di PM e PMT per ogni borough
        #elimino gli outliers con il metodo IQR (Inter Quartile Range)
        
        #PM:
        dataframe_PM = dataframe.copy()
        Q1 = np.percentile(dataframe_PM['PM'], 25,
                           interpolation = 'midpoint')
         
        Q3 = np.percentile(dataframe_PM['PM'], 75,
                           interpolation = 'midpoint')
        IQR = Q3 - Q1

        max = Q3+(1.5*IQR)
        min = Q1-(1.5*IQR)
 
        dataframe_PM.loc[dataframe_PM['PM'] < min, 'PM'] = np.nan
        dataframe_PM.loc[dataframe_PM['PM'] > max, 'PM'] = np.nan

        plot_PM = dataframe_PM.boxplot(by = 'Borough', column = ['PM'], grid = False)
        plt.savefig(file_list_features.results_path + r'/boxplot_PM.png')
        plt.show()
        
        #PMT:
        dataframe_PMT = dataframe.copy()
        Q1 = np.nanpercentile(dataframe_PMT['PMT'], 25,
                           interpolation = 'midpoint')
         
        Q3 = np.nanpercentile(dataframe_PMT['PMT'], 75,
                           interpolation = 'midpoint')
        IQR = Q3 - Q1

        max = Q3+(1.5*IQR)
        min = Q1-(1.5*IQR)
        
        dataframe_PMT.loc[dataframe_PMT['PMT'] < min, 'PMT'] = np.nan
        dataframe_PMT.loc[dataframe_PMT['PMT'] > max, 'PMT'] = np.nan

        dataframe_PMT = dataframe_PMT[(dataframe_PMT['PMT']>0)]

        plot_PMT = dataframe_PMT.boxplot(by = 'Borough', column = ['PMT'], grid = False)
        plt.savefig(file_list_features.results_path + r'/boxplot_PMT.png')
        plt.show() 
        
        return plot_PM, plot_PMT
    
    

REPOSITORY ESERCIZIO TAXI

Software sviluppato per rispondere alla Research Question 5 del Prof. Guarrasi. La specifica è la seguente: 

"La tariffa al miglio cambia attraverso i borough di New York? Vogliamo scoprire se le spese di un utente che usufruisce dei taxi in una zona sono diverse da quelle di chi li usa in un'altra. Considerando il fare_amount:
	
	-Calcolare il Prezzo al miglio (PM) per ogni corsa.
	
	-Calcolare la media e la deviazione standard della nuova variabile per ogni borough. Poi tracciate la distribuzione con un boxplot.

Il prezzo per miglio potrebbe dipendere dal traffico che il Taxi trova lunga la strada. Quindi, cerchiamo di mitigare questo effetto. È probabile che la durata del viaggio dica qualcosa sulla congestione della città, soprattutto se combinata con le distanze percorse. Potrebbe essere una buona idea ponderare il prezzo per miglio utilizzando il tempo necessario per completare il viaggio (T). Così, invece di PM, si può usare PMT=PM/T. Svolgere le stesse analisi fatte su PM ma su PMT e confrontare i risultati."

Una volta effettuato il clone della repository, è necessario eseguire il file “interfaccia.py”, il quale, servendosi dell’altro script nella repository (“main_taxi.py”) restituirà i risultati attesi.

All’interno del file “interfaccia.py” sono presenti:
	
	-un filtro per effettuare l’analisi solo su determinati borough invece che su tutto il dataset;
	
	-un filtro per selezionare se si vuole effettuare l’analisi sul borough di partenza della corsa del taxi o quello di arrivo;
	
	-una lista in cui inserire i file csv dei mesi di cui si vuole avere l’analisi;
	
	-una variabile in cui inserire il path dove sono salvati i file csv contenenti i dati delle corse;
	
	-una variabile in cui inserire il path dove voglio vengano salvati i risultati dell’analisi.

Nella repository, nella cartella “results_example”, è presente il file csv delle corse del mese di aprile (l’unico che rispettasse le dimensioni massime consentite da github per un file) e sono portati come esempio i risultati dell’analisi di questo file svolta su tutti i borough, considerando il borough di partenza. In essa vi è anche il file csv “taxi+_zone_lookup.csv” che associa ogni LocationID delle corse ad uno specifico borough, che è necessario per svolgere l’analisi.

Moduli utilizzati:
	
	-Pandas;
	
	-Datetime;
	
	-Numpy;
	
	-Matplotlib.pyplot

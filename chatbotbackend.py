from flask import Flask, request
import json
import csv
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/webhook",methods=['POST'])
def responseCreator():
    req = request.get_json(silent=True, force=True)
    #Print se koristi samo za pregled u Heroku konzoli
    print(req)

    #Varijable queryResults i intent sadrže informacije koje su potrebne za određivanje odgovora
    queryResults = req['queryResult']
    intent = queryResults['intent']['displayName']

    response = intentRecognizer(queryResults,intent)

    return {
            "fulfillmentMessages": [
                {
                "text": {
                    "text": [
                    f"{response}"
                    ]
                }
                }
            ]
            }

def intentRecognizer(queryResults,intent):
    if intent == "Smjerovi_Studija" :
        return Smjerovi_Studija(queryResults)
    elif intent == "Obavezni_kolegiji_na_studiju":        
        return Obavezni_kolegiji_na_studiju(queryResults)
    elif intent == "Izborni_kolegiji_na_studiju":        
        return Izborni_kolegiji_na_studiju(queryResults)
    elif intent == "Godina_kolegija":        
        return Godina_kolegija(queryResults)
    elif intent == "Semestar_kolegija":        
        return Semestar_kolegija(queryResults)           
                           
def Smjerovi_Studija(queryResults):
     vrstaStudija = queryResults['parameters']['vrsta_studija']
     smjerovi = pronadiSmjerove(vrstaStudija)
     return smjerovi

def Obavezni_kolegiji_na_studiju(queryResults):
     nazivStudija = queryResults['parameters']['naziv_studija']
     godinaStudija = queryResults['parameters']['godina_studija']
     obavezni = pronadiObavezneKolegije(nazivStudija,godinaStudija)
     return obavezni

def Izborni_kolegiji_na_studiju(queryResults):
     nazivStudija = queryResults['parameters']['naziv_studija']
     godinaStudija = queryResults['parameters']['godina_studija']
     obavezni = pronadiIzborneKolegije(nazivStudija,godinaStudija)
     return obavezni 

def Godina_kolegija(queryResults):
     nazivKolegija = queryResults['parameters']['naziv_kolegija']
     obavezni = pronadiGodinuKolegija(nazivKolegija)
     return obavezni  

def Semestar_kolegija(queryResults):
     nazivKolegija = queryResults['parameters']['naziv_kolegija']
     obavezni = pronadiSemestarKolegija(nazivKolegija)
     return obavezni

def pronadiSmjerove(vrstaStudija):
     pronadeniSmjerovi = []
     odgovor = ""
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['Vrsta_studija'].lower() == vrstaStudija.lower():
                 if zapis['Studij'] not in pronadeniSmjerovi:
                     pronadeniSmjerovi.append(zapis['Studij'])
                     odgovor += zapis['Studij']+", "

     if len(odgovor) == 0:
         odgovor = "I'm sorry but I don't have that study in my database. Check your spelling please"
     else:
         odgovor = f"{vrstaStudija} courses are {odgovor[:-2]}" 

     return odgovor  

def pronadiObavezneKolegije(nazivStudija,godinaStudija):
     odgovor = ""
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['Studij'].lower() == nazivStudija.lower() and zapis['Godina_studija'] == str(int(godinaStudija)):
                 if zapis['Obavezan'] == "DA":
                     odgovor += zapis['Naziv']+", "

     if len(odgovor) == 0:
         odgovor = "I'm sorry but I don't have that course and year in my database. Check your spelling please"
     else:
         odgovor = f"{nazivStudija} mandatory subjects are {odgovor[:-2]}" 

     return odgovor   

def pronadiIzborneKolegije(nazivStudija,godinaStudija):
     odgovor = ""
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['Studij'].lower() == nazivStudija.lower() and zapis['Godina_studija'] == str(int(godinaStudija)):
                 if zapis['Obavezan'] == "NE":
                     odgovor += zapis['Naziv']+", "

     if len(odgovor) == 0:
         odgovor = "I'm sorry but I don't have that course and year in my database. Check your spelling please"
     else:
         odgovor = f"{nazivStudija} optional subjects are {odgovor[:-2]}" 

     return odgovor

def pronadiGodinuKolegija(nazivKolegija):
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['Naziv'].lower() == nazivKolegija.lower():
                     return f"{zapis['Naziv']} is performed in {zapis['Godina_studija']} year {zapis['Semestar']} semester"
     return  "I'm sorry but I don't have that course in my database. Check your spelling please"                           

def pronadiSemestarKolegija(nazivKolegija):
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['Naziv'].lower() == nazivKolegija.lower():
                     return f"{zapis['Naziv']} is performed in {zapis['Semestar']} semester"
     return  "I'm sorry but I don't have that course in my database. Check your spelling please" 

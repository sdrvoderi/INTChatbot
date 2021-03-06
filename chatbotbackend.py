from flask import Flask, request
import json
import csv
import feedparser
import random
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
    elif intent == "ISVU_sifra":        
        return ISVU_sifra(queryResults)
    elif intent == "Broj_ECTS-a":        
        return Broj_ECTS(queryResults)
    elif intent == "Nastavnici_na_kolegiju":        
        return Nastavnici_na_kolegiju(queryResults)
    elif intent == "Sadrzaj_predavanja":        
        return Sadrzaj_predavanja(queryResults)
    elif intent == "Sadrzaj_vjezbi":        
        return Sadrzaj_vjezbi(queryResults)
    elif intent == "Ishodi_ucenja_predmeta":        
        return Ishodi_ucenja_predmeta(queryResults)
    elif intent == "Preduvjeti_za_predmet":        
        return Preduvjeti_za_predmet(queryResults)
    elif intent == "Novosti":        
        return Novosti()                                             
                           
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

def ISVU_sifra(queryResults):
     isvuSifra = queryResults['parameters']['isvu_number']
     obavezni = pronadiKolegijIsvu(isvuSifra)
     return obavezni

def Broj_ECTS(queryResults):
     nazivKolegija = queryResults['parameters']['naziv_kolegija']
     obavezni = pronadiKolegijECTS(nazivKolegija)
     return obavezni

def Nastavnici_na_kolegiju(queryResults):
     nazivKolegija = queryResults['parameters']['naziv_kolegija']
     obavezni = pronadiNastavnike(nazivKolegija)
     return obavezni    

def Sadrzaj_predavanja(queryResults):
     nazivKolegija = queryResults['parameters']['naziv_kolegija']
     obavezni = pronadiSadrzajPredavanja(nazivKolegija)
     return obavezni

def Sadrzaj_vjezbi(queryResults):
     nazivKolegija = queryResults['parameters']['naziv_kolegija']
     obavezni = pronadiSadrzajVjezbi(nazivKolegija)
     return obavezni 

def Ishodi_ucenja_predmeta(queryResults):
     nazivKolegija = queryResults['parameters']['naziv_kolegija']
     obavezni = pronadiIshodeUcenja(nazivKolegija)
     return obavezni

def Preduvjeti_za_predmet(queryResults):
     nazivKolegija = queryResults['parameters']['naziv_kolegija']
     obavezni = pronadiPreduvjete(nazivKolegija)
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

def pronadiKolegijIsvu(isvuSifra):
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['ISVU_sifra'] == str(int(isvuSifra)):
                     return f"{zapis['Naziv']} is the course behind the code {int(isvuSifra)}"
     return  "I'm sorry but I don't have that isvu code in my database. Check your spelling please"

def pronadiKolegijECTS(nazivKolegija):
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['Naziv'].lower() == nazivKolegija.lower():
                     return f"{zapis['Naziv']} is worth {zapis['ECTS']} ECTS points!"
     return  "I'm sorry but I don't have that subject in my database. Check your spelling please"

def pronadiNastavnike(nazivKolegija):
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['Naziv'].lower() == nazivKolegija.lower():
                     return f"{zapis['Naziv']} is being lectured by {zapis['Nastavnici']}"
     return  "I'm sorry but I don't have that subject in my database. Check your spelling please" 

def pronadiSadrzajPredavanja(nazivKolegija):
     odgovor = ""
     with open('data/moreData.json',newline='') as json_file:
         reader = json.load(json_file)
         for key, value in reader.items():
             if value['nazivKolegija'].lower() == nazivKolegija.lower():
                 for key2, value2 in value['sadrzajPredavanja'].items():
                     odgovor += value2['naziv']+", "
                 break        

     if len(odgovor) == 0:
         odgovor = "I'm sorry but I don't have that subject in my database or the subject does not have lectures. Check your spelling please"
     else:
         odgovor = f"{nazivKolegija}  lecture contents are {odgovor[:-2]}" 

     return odgovor

def pronadiSadrzajVjezbi(nazivKolegija):
     odgovor = ""
     with open('data/moreData.json',newline='') as json_file:
         reader = json.load(json_file)
         for key, value in reader.items():
             if value['nazivKolegija'].lower() == nazivKolegija.lower():
                 for key2, value2 in value['sadrzajVjezbi'].items():
                     odgovor += value2['opis']+", "
                 break        

     if len(odgovor) == 0:
         odgovor = "I'm sorry but I don't have that subject in my database or the subject does not have excercises. Check your spelling please"
     else:
         odgovor = f"{nazivKolegija} excecises contents are {odgovor[:-2]}" 

     return odgovor

def pronadiIshodeUcenja(nazivKolegija):
     odgovor = ""
     with open('data/moreData.json',newline='') as json_file:
         reader = json.load(json_file)
         for key, value in reader.items():
             if value['nazivKolegija'].lower() == nazivKolegija.lower():
                 for key2, value2 in value['ishodiUcenjaPredmeta'].items():
                     odgovor += value2['opis']+", "
                 break        

     if len(odgovor) == 0:
         odgovor = "I'm sorry but I don't have that subject in my database or the subject does not have any learning outcomes. Check your spelling please"
     else:
         odgovor = f"{nazivKolegija} learning outcomes are {odgovor[:-2]}" 

     return odgovor     

def pronadiPreduvjete(nazivKolegija):
     odgovor = ""
     pronadeniKolegij = False
     with open('data/moreData.json',newline='') as json_file:
         reader = json.load(json_file)
         for key, value in reader.items():
             if value['nazivKolegija'].lower() == nazivKolegija.lower():
                 pronadeniKolegij = True
                 for key2, value2 in value['preduvjeti'].items():
                     odgovor += value2['predmet']+", "
                 break        

     if len(odgovor) == 0:
         if pronadeniKolegij is True:
             odgovor = "The subject does not have any prerequisites."
         else:    
             odgovor = "I'm sorry but I don't have that subject in my database.  Check your spelling please"
     else:
         odgovor = f"{nazivKolegija} prerequisites are {odgovor[:-2]}" 

     return odgovor 

def Novosti():
     feed = feedparser.parse('https://www.foi.unizg.hr/hr/novosti/rss')
     entries = feed.entries
     if len(entries) > 0:
         novost = random.choice(entries)
         odgovor = f"I found this news! (you can ask me multiple tiems if you want more news) \nTime: {novost.published} \nNews headline: {novost.title}\nLink: {novost.link}"
     else:
         odgovor = "There is no news at this time!"   
     return odgovor      
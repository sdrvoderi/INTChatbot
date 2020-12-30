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
                           
def Smjerovi_Studija(queryResults):
     vrstaStudija = queryResults['parameters']['vrsta_studija']
     smjerovi = pronadiSmjerove(vrstaStudija)
     return f"{vrstaStudija} courses are {smjerovi}"  

def pronadiSmjerove(vrstaStudija):
     pronadeniSmjerovi = []
     odgovor = ""
     with open('data/elementaryData.csv',newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for zapis in reader:
             if zapis['Vrsta_studija'] == vrstaStudija.lower():
                 if zapis['Studij'] not in pronadeniSmjerovi:
                     pronadeniSmjerovi.append(zapis['Studij'])
                     odgovor += zapis['Studij']+", "
     if len(odgovor) == 0:
         odgovor = "I'm sorry but I don't have that study in my database. Check your spelling please"                
     return odgovor[:-1]                
                     


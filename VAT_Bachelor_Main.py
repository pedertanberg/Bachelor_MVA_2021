import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import flask
from flask import Flask, jsonify, request, make_response
import json
import requests
from functools import wraps
import jwt
import datetime


# definer scopet for å hente Google Sheets Data
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# Legge til google drive credentials
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/Bruger Power/Desktop/hello/.vscode/Sheets-8c9794c21198.json', scope)

# authorize google sheets for brukeren
client = gspread.authorize(creds)


# hente det spesifikke sheetet
sheet = client.open('Frontend Template')

# hente ark nummer 1
sheet_instance = sheet.get_worksheet(0)


# hente all data fra arket
records_data = sheet_instance.get_all_records()

# se dataen
records_data

# get all the records of the data
records_data = sheet_instance.get_all_records()

# view the data
records_data
#print(records_data)

# konverterer json til et Dataframe
records_df = pd.DataFrame.from_dict(records_data)


#Instansierer flask (til API hosting)
app = flask.Flask(__name__)
app.config["DEBUG"] = True
#Flask, når dataen skal hostes, skal den sorteres slik som dataen er i listen
app.config['JSON_SORT_KEYS'] = False

finalOutput=[]
apiOutPut=[]
objectList=[]
#Itererer gjennom dataframen, for å definere all dataen i hver celle. 
for index,row in records_df.iterrows():
    country_from = row['Selger']
    country_to = row['Mottaker']
    vat_nr = row['VAT NR']
    good_type1 = row['Momstype']
    good_type = str(good_type1.lower())
    sales_amount1 = str(row['Salgsbeløp'])
    temp_sales = sales_amount1.replace(',','.')
    sales_amount = float(temp_sales)
    #Konverterer dato til riktig format for å hente kurs på API
    date = row['Dato']
    day = date[0:2]
    month = date[3:5]
    year = date[6:10]
    datetime1 = year+"-"+month+"-"+day
    #Dataformattering for å se om land f.eks er "Denmark", så skal det gjøres om til "DE"
    length_of_country_to = len(country_to)
    length_of_country_from = len(country_from)

##if statement for å sjekke country_to og dens lengde
    if length_of_country_to > 2:
        #Konvertere alt til små bokstaver
        country_to.lower()
        if country_to.lower()=="austria":
            country_to="AT"
        elif country_to.lower()=="sweden":
            country_to="SE"
        elif country_to.lower()=="czech republic":
            country_to="CZ"
        elif country_to.lower()=="denmark":
            country_to="DK"
        elif country_to.lower()=="bulgaria":
            country_to="BG"
        elif country_to.lower()=="croatia":
            country_to="HR"
        elif country_to.lower()=="hungary":
            country_to="HU"
        elif country_to.lower()=="poland":
            country_to="PL"
        elif country_to.lower()=="romania":
            country_to="RO"
        elif country_to.lower()=="belgium":
            country_to="BE"
        elif country_to.lower()=="cyprus":
            country_to="CY"
        elif country_to.lower()=="estonia":
            country_to="EE"
        elif country_to.lower()=="finland":
            country_to="FI"
        elif country_to.lower()=="france":
            country_to="FR"
        elif country_to.lower()=="germany":
            country_to="DE"
        elif country_to.lower()=="greece":
            country_to="GR"
        elif country_to.lower()=="ireland":
            country_to="IR"
        elif country_to.lower()=="italy":
            country_to="IT"
        elif country_to.lower()=="latvia":
            country_to="LV"
        elif country_to.lower()=="lithuania":
            country_to="LT"
        elif country_to.lower()=="luxembourg":
            country_to="LU"
        elif country_to.lower()=="malta":
            country_to="MT"
        elif country_to.lower()=="netherlands":
            country_to="NL"
        elif country_to.lower()=="portugal":
            country_to="PT"
        elif country_to.lower()=="slovenia":
            country_to="SL"
        elif country_to.lower()=="slovakia":
            country_to="SK"
        elif country_to.lower()=="spain":
            country_to="ES"
    else:
        #Hvis ingen av de er sanne, så ser country samme som data fra Sheets   
        country_to=country_to


    # samme if statement, bare for country from
    if length_of_country_from > 2:
        country_from.lower()
        if country_from.lower()=="austria":
            country_from="AU"
        elif country_from.lower()=="sweden":
            country_from="SE"
        elif country_from.lower()=="czech republic":
            country_from="CZ"
        elif country_from.lower()=="denmark":
            country_from="DK"
        elif country_from.lower()=="bulgaria":
            country_from="BG"
        elif country_from.lower()=="croatia":
            country_from="HR"
        elif country_from.lower()=="hungary":
            country_from="HU"
        elif country_from.lower()=="poland":
            country_from="PL"
        elif country_from.lower()=="romania":
            country_from="RO"
        elif country_from.lower()=="belgium":
            country_from="BE"
        elif country_from.lower()=="cyprus":
            country_from="CY"
        elif country_from.lower()=="estonia":
            country_from="EE"
        elif country_from.lower()=="finland":
            country_from="FI"
        elif country_from.lower()=="france":
            country_from="FR"
        elif country_from.lower()=="germany":
            country_from="DE"
        elif country_from.lower()=="greece":
            country_from="GR"
        elif country_from.lower()=="ireland":
            country_from="IR"
        elif country_from.lower()=="italy":
            country_from="IT"
        elif country_from.lower()=="latvia":
            country_from="LV"
        elif country_from.lower()=="lithuania":
            country_from="LT"
        elif country_from.lower()=="luxembourg":
            country_from="LU"
        elif country_from.lower()=="malta":
            country_from="MT"
        elif country_from.lower()=="netherlands":
            country_from="NL"
        elif country_from.lower()=="portugal":
            country_from="PT"
        elif country_from.lower()=="slovenia":
            country_from="SL"
        elif country_from.lower()=="slovakia":
            country_from="SK"
        elif country_from.lower()=="spain":
            country_from="ES"
       
    else:
        country_from=country_to

    #Antakelse for MVP'en at basen alltid vil være danske kroner, da Skat.dk krever oppggjørelse i DKK
    currencyBase="DKK"
    currencysymbol =""
    #Sjekker om country_to er blant landene som har euro. Hvis ikke setter den lokal valuta i country_to
    if country_to not in ["SE","FI","CZ", "DK","BG", "HR", "HU","PL","RO"]:
        currencysymbol="EUR"
        
    elif country_to=="SE":
        currencysymbol="SEK"
    elif country_to=="CZ":
        currencysymbol="CZK"
    elif country_to=="DK":
        currencysymbol="DKK"
    elif country_to=="BG":
        currencysymbol="BGN"
    elif country_to=="HR":
        currencysymbol="HRK"
    elif country_to=="HU":
        currencysymbol="HUF"
    elif country_to=="PL":
        currencysymbol="PLN"
    elif country_to=="RO":
        currencysymbol="RON"

    #Henter valutakursdata
    urlFX = ("https://api.ratesapi.io/"+datetime1+"?base="+currencysymbol+"&symbols=DKK")
    Fx_Respnse = requests.get(urlFX)
    FX_Data = Fx_Respnse.json()
    #Velger raten i JSON formatet
    fx_rate = FX_Data['rates']['DKK']
            

    #Henter MVA data fra API. 
    urlVAT = ("http://www.apilayer.net/api/rate?access_key=baebd10f0fedb104d52e251b2753f473&country_code="+country_to)
    r = requests.get(urlVAT)
    VAT_Data = r.json()

    #sjekker om brukerinput fra sheets er standard_rate
    if good_type == "standard_rate":
        #Hvis sann så henter den JSON data fra API som er er standard rate
        VAT_rate = VAT_Data['standard_rate']
        good_type="standard"
    elif good_type != "standard_rate":
        #Hvis ikke sann så henter den JSON data fra API som er er reduced rate for good type
        VAT_rate= VAT_Data['reduced_rates'][good_type]
        good_type="nedsatt"

    #finner salgssum i DKK basert på valutakurs
    Sales_amount_in_DKK = sales_amount*fx_rate
    #finner momsbeløp basert på MVA rate og momspliktig beløp
    VAT_payable = Sales_amount_in_DKK*VAT_rate/100
    #legger nå til alle parametere i formatet skat.dk krever, i en midlertidig list ved hver iterasjon
    templist1={"linjekode":"003","landekode_from":country_from, "VAT_number":vat_nr,"Landekode_to":country_to,"Momssatstype": good_type,"Momssatsprocent":VAT_rate, 'Mompliktig_beløp':Sales_amount_in_DKK, 'Momsbeløp': VAT_payable}
    #Legger deretter denne midlertidige listen i en list som skal inneholde alle transaksjoner
    finalOutput.append(templist1)

for i in finalOutput:
    objectList.append(i)

#Sender finalOutput listen til google sheets
spreadsheetList = finalOutput
runs = pd.DataFrame(spreadsheetList)
sheet_transactions=sheet.get_worksheet(2)
sheet_transactions.insert_rows(runs.values.tolist())


#Verifiserer nå google sheets igjen, for å hente dataen som nå ble insertet til databasen
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/Bruger Power/Desktop/hello/.vscode/Sheets-8c9794c21198.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Frontend Template')
#Databasen finnes på ark 3
sheet_instance = sheet.get_worksheet(2)
records_data = sheet_instance.get_all_records()
records_data
records_data = sheet_instance.get_all_records()
records_df = pd.DataFrame.from_dict(records_data)

jsonAPIList=[]
#Iterasjoner gjennom dataen fra databasen
for index,row in records_df.iterrows():
    print(row)
    linje_kode = row[0]
    country_from = row[1]
    vat_nr = row[2]
    country_to = row[3]
    good_type = row[4]
    VAT_rate = row[5]
    Sales_amount_in_DKK = row[6]
    VAT_payable = row[7]

    #legger dataen til i en midlertidig liste i formatted krevd fra skat.Dk
    templist1={"linjekode":linje_kode,"landekode_from":country_from, "VAT_number":vat_nr,"Landekode_to":country_to,"Momssatstype": good_type,"Momssatsprocent":VAT_rate, 'Mompliktig_beløp':Sales_amount_in_DKK, 'Momsbeløp': VAT_payable}
    #Legger midlertidig listen i en listen som skal sendes til API
    jsonAPIList.append(templist1)

#Definerer JWT elementer som en nøkkel, algoritme og levetid for token key. 
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20
templist1={"linjekode":"003","landekode_from":"NO", "VAT_number":"1934829","Landekode_to":"DK","Momssatstype": "Food Stuff","Momssatsprocent":"22", 'Mompliktig_beløp':"200", 'Momsbeløp': "44"}

# Token Decorator
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')

		if not token:
			return jsonify({'message' : 'Token is missing'}), 403

		try:
			data = jwt.decode(token,JWT_SECRET, algorithms=[JWT_ALGORITHM])
		except:
			return jsonify({'message' : 'Token is invalid!'}), 403

		return f(*args, **kwargs)

	return decorated

# En unprotected route og funksjon som returnerer en melding
@app.route('/unprotected')
def unprotected():
	return jsonify({'message' : 'Anyone can view this.'})

# En protected route og funksjon som returnerer JSON listen etter verfifisert login
@app.route('/protected')
#kaller på token_required
@token_required
def protected():
    #Bruker JSONIFY funksjonen fra flask til å konverter listen til JSON format
	return jsonify(finalOutput)

# Login Route og funksjon
@app.route('/login')
def login():
	auth = request.authorization

    #Hvis brukernavn og passord er BachelorBoys, så generer og returner en token
	if auth and auth.password == 'BachelorBoys':
		token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50)},JWT_SECRET, JWT_ALGORITHM)
		return jsonify({'token' : token})
        #Bruker JSONIFY funksjonen fra flask til å konverter token til JSON format


	return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm:"Login Required"'})

@app.route('/api/v1/resources/transactions', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    #Ser om en ID var gitt som parameter i URL. Hvis den er, så assign den til en variabel. Hvis ikke display error.
        if 'VAT_number' in request.args:
            id = int(request.args['VAT_number'])
        else:
            return "Error: No id field provided. Please specify an id."

        # Create an empty list for our results
        #Oppretter et tomt array for resultatene
        results = []

        #Looper gjennom dataen og finner matchene resultater med vat_number
        for transaction in objectList:
            if transaction['VAT_number'] == id:
                results.append(transaction)

        #Bruker JSONIFY funksjonen fra flask til å konverter listen til JSON format
        return jsonify(results)


app.run()
   
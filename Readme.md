# Bachelor_MVA_Final

Steps to reproduce
1. Gå til: https://docs.google.com/spreadsheets/d/1e1BGOR7E5GRndh5L-N-xyxQGcI9lbTqceUYtLjG09a8/edit#gid=0
2. I Ark 1, inntast data i feltene, og velg Momstype fra Dropdown
3. Sørg for å installere: gspread, pandas, oauth2client.service_account, flask, jwt gjennom kommando "pip instal ..."
4. Hent nøklene til Sheets-8c9794c21198.json i Bilag XXX i bachelorrapporten
5. Kjør scriptet. 
6. Når scriptet har kjørt gå til http://127.0.0.1:5000/login
7. Inntast brukernavn: BachelorBoys og passord: BachelorBoys
8. Kopier den opprettede token. 
9. Gå til http://127.0.0.1:5000/protected?token=<DIN TOKEN HER>
10. Du vil nå se alle transaksjoner i JSON Api format. 
11. Du vil også se alle transaksjonene lagret i Databasen på Ark 3. 

![image](https://github.com/pedertanberg/Bachelor_MVA_Final/blob/main/hello/image.jpg)

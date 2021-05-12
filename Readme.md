Steps to reproduce
1. Gå til: https://docs.google.com/spreadsheets/d/1e1BGOR7E5GRndh5L-N-xyxQGcI9lbTqceUYtLjG09a8/edit#gid=0
2. I Ark 1, inntast data i feltene, og velg Momstype fra Dropdown
3. Sørg for å installere: gspread, pandas, oauth2client.service_account, flask, jwt gjennom kommando "pip instal ..."
4. Kjør scriptet. 
5. Når scriptet har kjørt gå til http://127.0.0.1:5000/login
6. Inntast brukernavn: BachelorBoys og passord: BachelorBoys
7. Kopier den opprettede token. 
8. Gå til http://127.0.0.1:5000/protected?token=<DIN TOKEN HER>
9. Du vil nå se alle transaksjoner i JSON Api format. 
10. Gå til https://www.sheet2site.com/api/v3/index.php?key=1e1BGOR7E5GRndh5L-N-xyxQGcI9lbTqceUYtLjG09a8
11. Her vil du se alle transaksjonene lagret i Databasen(Ark 3) på en frontend. 

![image](https://github.com/pedertanberg/Bachelor_MVA_2021/blob/main/image.jpg)

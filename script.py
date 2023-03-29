import json
import re
from datetime import datetime

#Regex para la detección de fechas formato dd/mm/yy y para la detección de importes
regex_dmy =r"((0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/(19|20)?\d{2})"
regex_importe = r"(-?\d+[.,]\d{2}) ?€?"
#regex_mdy =r"((0*[1-9]|1[0-2])[- /.](0*[1-9]|[1-2][0-9]|3[01])[- /.](19|20)*\d{2})"

#Se ha modificado los datos originales para tener formato json
f = open('data.txt', encoding="utf8")

data = json.loads(f.read())

fechas = []
importes = []
totales = []
importes_neg = []
#Extracción de las fechas e importes de las cadenas de texto
for doc in data:
    fechas_temp = re.findall(regex_dmy,doc["Cadena"])
    importes_temp = re.findall(regex_importe,doc["Cadena"])
    importes_temp = set([float(t.replace(",",".")) for t in importes_temp])
    #fechas_temp = fechas_temp if fechas_temp else re.findall(regex_mdy,doc["Cadena"])
    fechas_clean = []
    for tupla in fechas_temp:
        #formateando a datetime para dd/mm/yyyy o dd/mm/yy
        try:
            fechas_clean.append(datetime.strptime(tupla[0],"%d/%m/%Y"))
        except:
            fechas_clean.append(datetime.strptime(tupla[0],"%d/%m/%y"))

    fechas.append(fechas_clean)
    importes_neg.append([n for n in importes_temp if n<0])
    #De base se obtiene el importe máximo
    totales.append(max(importes_temp))
    importes.append(importes_temp)

#Detección de números negativos para no tomar el valor máximo como importe
for i in range(0,len(totales)):
    if importes_neg[i]:
        #En caso de que haya números negativos se comprueba si la resta de los mismos al valor 
        #más alto existe en el documento
        nuevo_total = totales[i] + sum(importes_neg[i])
        if list(importes[i]).count(nuevo_total):
            totales[i]=nuevo_total
#Se añade los importes totales y fechas para cada documento
for i,doc in enumerate(data):
    doc["Total"]=totales[i]
    #A falta de un sistema más complejo se obtiene la última fecha del documento
    doc["Fecha"]=fechas[i][-1].strftime("%d/%m/%Y")

#Se devuelve (imprime en este caso) el json con los datos añadidos
print(data)
print("fin")
from datetime import datetime, timedelta


fecha1 = datetime.strptime("13/05/2022", "%d/%m/%Y")
fecha2 = datetime.strptime("15/05/2022", "%d/%m/%Y")

dif = (fecha2 - fecha1).days

print(dif)

dic1 = {
    "nombre": "Emerson Cabrera",
    "anio_nacimiento": 1982,
    "celular": "311 420 9440",
}
dic2 = dic1
print(dic1)
print(dic2)

dic2["anio_nacimiento"] = 1980
dic1["nombre"] = "Emerson"
print("-------------------------")
print(dic1)
print(dic2)

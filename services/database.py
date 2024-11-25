import pyodbc

server= "LAPTOP-H123T9I7\SQLEXPRESS"
database= "Lafepe03"
username= "mateus"
password= "mateus30"
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

print("Conexão Bem Sucedida")



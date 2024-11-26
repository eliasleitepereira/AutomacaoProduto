import mysql.connector

#Função de conexao
def connect_sql():
    return mysql.connector.connect(host='127.0.0.1', user='admin', password='123456',port='3306', database='delfia')

# import re
# import math

# QTD_Produto_Pesquisado = 50
# numero_pag = 0

# a = "Elias 89"
# b = int(re.search(r"\d+", a).group())

# print(b)


# for i in range(1,QTD_Produto_Pesquisado+1,12):
#     numero_pag +=1 
#     if i > b:
#         break

#     for j in range(1,13):
#         print(f"numero do produto da pagina: {j}")
#         print(f"numero total do produto: {i}")
#         i+=1
        
#         if i > 50:
#             break
    
#     print(f"numero da pagina: {numero_pag}")
        


# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import pyautogui
# import time
# import re

# Qtd_pesq = 50
# Marca_Pesquisada = "Apple"
# Numero_pagina = 1

# #region Navegar até os produtos
# driver = webdriver.Chrome()
# wait = WebDriverWait(driver,10)
# driver.get('https://store.vivo.com.br/celulares/c?query=:pricePriority-desc:allCategories:celulares:brand:Apple')
# # Maximizando a janela
# driver.maximize_window()

# for i in range (1,15):
#     time.sleep(5)
#     driver.get(f'https://store.vivo.com.br/celulares/c?query=:pricePriority-desc:allCategories:celulares:brand:Apple&currentPage={Numero_pagina}')
#     Numero_pagina += 1
#     pyautogui.alert(text=f"{Numero_pagina}")
import ConexaoBd as cn
from funcoes import * 


produto = "Apple iPhone 16 256GB Verde Acinzentado 5G Tela 6,1 Câm. Traseira 48 MP + 12 MP Frontal 12 MP"
preco = "R$ 8.299,00"
capacidade, modelo, tela, cor = detalhes_produto(produto)
Ultima_peca = 1

preco = int(preco.replace("R$ ", "").replace(".", "").replace(",00", ""))
parcela = round(preco/12 ,2)


try:
    print("oi")
except:
    print("oi")
#preco = re.sub(",", ".", preco)

#query para inserção 
adicionandoDB = f"""INSERT INTO tb_celulares (Modelo, `Capacidade (GB)`, `Tamanho da Tela`, `Preco total`, `Valor da parcela`, Cor, `Ultimas pecas`)
VALUES ('{modelo[:50]}', '{capacidade[:10]}', '{tela[:10]}', '{preco}', '{parcela}', '{cor[:10]}', {Ultima_peca});"""
#Inserindo no BD
#cn.inserir_sql(adicionandoDB)

inserir_sql(adicionandoDB)





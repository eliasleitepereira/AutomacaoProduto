from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
from funcoes import * 
import easygui
Qtd_pesq = 50 #Qtd de Itens a pesquisar
Marca_Pesquisada = "Apple" #Marca a pesquisar
Numero_pagina = 1
Item_Comprado = False
cep = "08235360"
#region Navegar até os produtos
driver = webdriver.Chrome()
wait = WebDriverWait(driver,10)


driver.get('https://store.vivo.com.br/celulares/c')



# Maximizando a janela
driver.maximize_window()

#Clicando no campo de selecao
time.sleep(2)
driver.find_element('xpath','/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[1]/div/div[3]/div/vsp-select/section/button/div[2]/div').click()


#Clicando em "preço(maior primeiro)"
time.sleep(2)
driver.find_element('xpath','/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[1]/div/div[3]/div/vsp-select/section/ul/li[5]/span').click()

#Aplicando filtro de marca pesquisada
driver.get(f'https://store.vivo.com.br/celulares/c?query=:pricePriority-desc:allCategories:celulares:brand:{Marca_Pesquisada}')


easygui.msgbox("Após o Filtro")
#region Obter a quantidade de resultado
time.sleep(5)
    #Mensagem informando a quatidade encontrada
Mensagem_Resultado = driver.find_element('xpath','/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[1]/div/div[1]/div[1]/div/div/span').text

    #Pegando o numero de resultado
Numero_Resultado = int(re.search(R"\d+", Mensagem_Resultado).group())
#endregion

#endregion

#Loop para quantidade de item a pesquisar
    #O 12 é a quantidade maxima de produto por pagina
for numero_produto in range(1,Qtd_pesq+1,12):

    #Verificando se ultrapassou a qtd de pesquisa
    if numero_produto > Numero_Resultado:
        break
    
    time.sleep(5)
    #Loop para quantidade de produtos na pagina
    for card_produto in range(1,13):
        
        #Descricao do produto
        Desc_Prod = driver.find_element('xpath',f'/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[2]/div/product-card[{card_produto}]/a/div[2]/h3').text
        print(Desc_Prod)
        #Verificando se o produto contem preço ou não
        try:
            #Pegando preço
            preco = driver.find_element('xpath',f'/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[2]/div/product-card[{card_produto}]/a/div[3]/div/div[2]/div/p/span').text
            
            #region Validando se o produto com preco contem "ultimas pecas" ou nao
            try:
                #Caso a tag de "ulima peça" esteja do lado de "lancamento"
                Ultimas_pecas_tag = driver.find_element('xpath',f'/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[2]/div/product-card[{card_produto}]/a/product-tags/div/div[2]/span[2]').text
                
                #Verificar se a tag é a de ultimas pecas
                if Ultimas_pecas_tag == 'Últimas Peças':

                    Ultimas_pecas = 1
                else:
                    Ultimas_pecas = 0
                
               
            except:
                
                try:
                    #Caso a tag de "ulima peça" seja unico
                    Ultimas_pecas_tag = driver.find_element('xpath',f'/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[2]/div/product-card[{card_produto}]/a/product-tags/div/div/span[2]').text
                    
                    #Verificar se a tag é a de ultimas pecas
                    if Ultimas_pecas_tag == 'Últimas Peças':

                        Ultimas_pecas = 1
                    else:
                        Ultimas_pecas = 0
                
                except:
                    #Caso nao tenha nenhuma tag
                    Ultimas_pecas = 0
            #endregion

            #Validacao para o primeiro item com preço
            if Item_Comprado == False:
                Item_Comprado = True
                cep_entrega= consultar_cep(cep)
                pedido = gerarPdf(cep=cep,rua=cep_entrega['logradouro'],bairro = cep_entrega['bairro'],produto = Desc_Prod,preco = preco,nome_arquivo="Detalhes_pedido.pdf")
                easygui.msgbox("Olhar PDF")

            #Função para encontra as caracteristicas do produto
            capacidade, modelo, tela, cor = detalhes_produto(Desc_Prod)
            
            #Removendo R$ e ,00
            preco = int(preco.replace("R$ ", "").replace(".", "").replace(",00", ""))

            #Valor da parcela
            parcela = round(preco/12 ,2)
            
            #Query de inserção
            adicionandoDB = f"""INSERT INTO tb_celulares (Modelo, `Capacidade (GB)`, `Tamanho da Tela`, `Preco total`, `Valor da parcela`, Cor, `Ultimas pecas`)
                                VALUES ('{modelo[:50]}', '{capacidade[:10]}', '{tela[:10]}', '{preco}', '{parcela}', '{cor[:10]}', {Ultimas_pecas});"""
            #Função Inserir no banco
            inserir_sql(adicionandoDB)


            print(f""" Modelo: {modelo},
                       Capacidade: {capacidade},
                        Tela: {tela},
                        Preco: {preco},
                        valor parcela: {parcela},
                        cor: {cor[:10]},
                        Ultimas Pecas: {Ultimas_pecas}
                        """)
        except:
            #Caso nao tenha preco
            preco = driver.find_element('xpath',f'/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[2]/div/product-card[{card_produto}]/a/div[3]/p').text

        numero_produto +=1
        #Verifica caso já tenha ultrapassado o numero de pesquisa de produto
        if numero_produto > Qtd_pesq:
            break

    #Mudando para proxima pagina
    driver.get(f'https://store.vivo.com.br/celulares/c?query=:pricePriority-desc:allCategories:celulares:brand:{Marca_Pesquisada}&currentPage={Numero_pagina}')
    Numero_pagina +=1
    time.sleep(4)


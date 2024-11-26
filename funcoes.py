import requests
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from ConexaoBd import *
import re

# Função para consultar CEP usando a API ViaCEP
def consultar_cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    
    # Fazendo a requisição GET
    response = requests.get(url)
    
    # Verificando se a requisição foi bem-sucedida (status code 200)
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        dados = response.json()
        
        # Verificando se o CEP é válido
        if "erro" not in dados:
            return dados
        else:
            return "CEP inválido!"
    else:
        return f"Erro na consulta do CEP. Status Code: {response.status_code}"

#Função para gerar PDF
def gerarPdf(nome_arquivo,rua, bairro, cep,produto, preco):
   
    data_entrega = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
    pdf = SimpleDocTemplate(nome_arquivo,pagesize=letter)

    # Dados da Tabela
    dados = [
        ['Produto', 'Valor', 'Entrega prevista'],
        [produto,preco,data_entrega]
    ]

    # Criar a tabela
    tabela = Table(dados)

    # Definir o estilo da tabela
    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),  # Fundo cinza para o cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto branco no cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centralizar o conteúdo
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte do cabeçalho em negrito
        ('FONTSIZE', (0, 0), (-1, -1), 9),  # Tamanho da fonte
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Espaçamento inferior do cabeçalho
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Fundo bege para o conteúdo
        ('GRID', (0, 0), (-1, -1), 1, colors.purple)  # Linhas da tabela com cor preta
    ])

     # Aplicar o estilo à tabela
    tabela.setStyle(estilo_tabela)

    # Criar o estilo para o texto abaixo da tabela
    estilo = getSampleStyleSheet()
    estilo_normal = estilo['Normal']

    # Texto que será adicionado abaixo da tabela
    texto = f"""
    A entrega será feita no endereço: {rua} no bairro: {bairro}, CEP:{cep} até a data prevista.\n
    Para mais informações, entre em contato com nossa central de atendimento.
    """

    # Criar o parágrafo com o texto e o estilo definido
    paragrafo = Paragraph(texto, estilo_normal)

    # Adicionar um espaço entre a tabela e o texto
    espaco = Spacer(1, 12)

    # Definir o conteúdo do PDF (tabela seguida do parágrafo)
    elementos = [tabela, espaco, paragrafo]

    # Criar o PDF
    pdf.build(elementos)

#Função de inserção no banco
def inserir_sql(query):
    cnxn = connect_sql()
    cursor = cnxn.cursor(dictionary=True)
    cursor.execute(query)
    cnxn.commit()
    cursor.close()
    cnxn.close()
    #cn.inserir_sql(adicionandoDB)

#Função obter detalhes do produto pela descrição
def detalhes_produto(produto):
    #produto = "Apple iPhone 16 256GB Verde Acinzentado 5G Tela 6,1 Câm. Traseira 48 MP + 12 MP Frontal 12 MP"
    #Regex da capacidade de memoria
    capacidade = re.findall("\d+\S{2}|\d{3}\S{2}", produto)


    #Regex do modelo
    modelo= re.split("\d+\S{2}|\d{3}\S{2}", produto)
    

    #Regex do Tamanho da tela
    tela = re.findall("\d,\d", produto)
    
    #Regex da cor
    cor = re.findall(f"{capacidade[0]}(.*?)5G", produto)

    #Retornando todas as caracteristicas encontrada
    return capacidade[0], modelo[0], tela[0], cor[0]
    
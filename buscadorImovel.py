
from email.policy import strict
import imp
from platform import java_ver
from pydoc import source_synopsis
import re
import pandas as pd
import numpy as np
import requests 
from bs4 import BeautifulSoup
import json
from difflib import SequenceMatcher
from selenium import webdriver
import time 
from datetime import date 
# regex para pegar o ano da STRING 
import regex

listaJason = []

def buscadorDadosOlx(pages = 2, bairro = "AT"):
    # https://se.olx.com.br/sergipe/aracaju/jabotiana/imoveis/venda
    # https://se.olx.com.br/sergipe/aracaju/jabotiana/imoveis/venda
    bairroBuscar = {"AT": "atalaia", "JB": "jabotiana"}

    for x in range(0, pages):
        print(" LOOP NUMERO: " + str(x))
        url = "https://se.olx.com.br/sergipe/aracaju/" + bairroBuscar[bairro] + "/imoveis/venda"

        if x == 0: 
            print("somente a primeira linha")
        else: 
            url = "https://se.olx.com.br/sergipe/aracaju/" + bairroBuscar[bairro] + "/imoveis/venda?o=" +str(x)

        PARAMS = {
                    "authority": "se.olx.com.br",
                    "method": "GET",
                    "path": "/aracaju/atalaia/imoveis/venda",
                    "scheme": "https",
                    "referer": "https://se.olx.com.br/sergipe/aracaju/atalaia/imoveis/venda",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        }

        page = requests.get(url=url, headers=PARAMS)
        soup = BeautifulSoup(page.content, "lxml")
        itens = soup.find_all("li", {"class": "sc-1fcmfeb-2 fvbmlV"})
        print(len(itens))

        for a in itens: 
            try:
                anuncio = a.findAll("h2")[0].contents[0]
                precoImovel = a.findAll("span", class_="m7nrfa-0 eJCbzj sc-fzsDOv kHeyHD")[0].contents[0]
                precoImovel = precoImovel.split("R$")[1]
                precoImovel = float(precoImovel.replace(".", ""))
                diaHoraPostagem = a.findAll("span", class_="sc-11h4wdr-0 javKJU sc-fzsDOv dTHJIA")[0].contents[0]
                diaPostagem = diaHoraPostagem.split(",")[0]
                horaPostagem = diaHoraPostagem.split(",")[1]
                urlPostagem = a.find("a")["href"]
                quartosPostagem = a.findAll("span", "sc-1ftm7qz-0 itsfPe sc-bdVaJa bxVNCd")[0].contents[0]
                quartosPostagem = quartosPostagem.split(" ")[0]
                metrosQuadrados = a.findAll("span", "sc-1ftm7qz-0 itsfPe sc-bdVaJa bxVNCd")[1].contents[0]
                metrosQuadrados = metrosQuadrados.split("m")[0]
                condominioPostagem = a.findAll("span", "sc-1ftm7qz-0 itsfPe sc-bdVaJa bxVNCd")[2].contents[0]
                condominioPostagem = float(condominioPostagem.split("R$")[1])
                #print(precoImovel)
                
            except: 
                print("error")

            print("Preco do Imovel: " + str(precoImovel))
            print("Descricao: " + anuncio)
            print("Dia da Postagem: " + diaPostagem)
            print("Hora da Postagem: " + horaPostagem)
            print("URL: " + urlPostagem)
            print("Quartos: " + quartosPostagem)
            print("m2: " + metrosQuadrados)
            print("Condominio: " + str(condominioPostagem))
            print("=============")

            json = {
                "postagem": anuncio, 
                "preco_postagem": precoImovel, 
                "quartos_postagem": quartosPostagem, 
                "metros_postagem": metrosQuadrados, 
                "condominio_postagem": condominioPostagem,
                "dia_postagem": diaPostagem, 
                "hora_postagem": horaPostagem, 
                "url_postagem": urlPostagem,
            }

            listaJason.append(json)

buscadorDadosOlx(pages = 2)
df = pd.DataFrame(listaJason)
df.to_excel("imoveis.xlsx")
print(listaJason)
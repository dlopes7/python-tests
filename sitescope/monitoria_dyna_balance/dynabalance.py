import sys
import requests
import time
import json
import smtplib
import imaplib

import icontrol as viprion

rodar = False


#Primeiro parametro, URL
url = 'www.casasbahia.com.br'

#Mapeamento de URLs para Pools (Viprion)
url_pool_viprion = {
            'www.pontofrio.com.br':'/Common/AJAX_HTTP',
            'carrinho.pontofrio.com.br': '/Common/AJAXCARRINHO_HTTP',
            'imagens.pontofrio.com.br': '/Common/ROMA_HTTP',
            'busca.pontofrio.com.br': '/Common/AJAXBUSCA_HTTP',
            
            'www.casasbahia.com.br': '/Common/DALLAS_HTTP',
            'carrinho.casasbahia.com.br': '/Common/DALLASCARRINHO_HTTP',
            'imagem.casasbahia.com.br': '/Common/PARMA_HTTP',
            'busca.casasbahia.com.br': '/Common/DALLASBUSCA_HTTP',
            
            'www.extra.com.br': '/Common/CHELSEA_HTTP',
            'carrinho.extra.com.br': '/Common/CHELSEACARRINHO_HTTP',
            'imagens.extra.com.br': '/Common/LAZIO_HTTP',
            'busca.extra.com.br': '/Common/CHELSEABUSCA_HTTP',
            
            'www.cdiscount.com.br':'/Common/MILAN_HTTP',
            'carrinho.cdiscount.com.br': '/Common/MILANCARRINHO_HTTP',
            'imagens.cdiscount.com.br': '/Common/CELTIC_HTTP',
            'busca.cdiscount.com.br': '/Common/MILANBUSCA_HTTP',
            
            'www.aoc.com.br': '/Common/GALAXY_HTTP',
            'www.lojahp.com.br': '/Common/GALAXY_HTTP',
            'www.lojafuji.com.br': '/Common/GALAXY_HTTP',
            'www.barateiro.com.br': '/Common/GALAXY_HTTP',
            
            'imagens.lojahp.com.br': '/Common/NAPOLI_HTTP',
            'imagens.aocloja.com.br': '/Common/NAPOLI_HTTP',
            'imagens.lojafuji.com.br': '/Common/NAPOLI_HTTP',
            'imagens.barateiro.com.br': '/Common/NAPOLI_HTTP',

            'www.b2bnaweb.com.br': '/Common/GENOA_HTTP',
            'imagens.b2bnaweb.com.br': '/Common/UDINESE_HTTP',

            'www.nike.com.br': '/Common/SANTOS_HTTP',
            'shop.nike.com.br': '/Common/SANTOSCARRINHO_HTTP',
            'www.lojadanike.com.br': '/Common/CORITIBA_HTTP',

            'imagens.pontofrioatacado.com.br': '/Common/TOTTENHAM_HTTP',
            'servicos.gpa.net.br': '/Common/ARSENAL_HTTP',
            }

#Mapeamento de URLs para Pools (BigIP)
url_pool_big_ip = {}




#*********** USUARIO E SENHA ***********#
usuario = '<usuario>'               #
senha = '<senha>'                      #
#***************************************#


with open(r'D:\SiteScope\logs\python\agentes_dynatrace.txt', 'r') as arquivo:
    agentes = json.loads(str(arquivo.read()))

agentes_fora_balance = []

for site, hosts in agentes.iteritems():
    hosts = [host.upper() for host in hosts]
    try:
        pool = url_pool_viprion[site]
        ip = '10.128.7.253' 
    except KeyError, e:
        try:
            pool = url_pool_big_ip[site]
            ip = '10.128.7.8'
        except KeyError, e:
            continue
        
    servidores =  viprion.get_pool_members(pool, ip, usuario, senha)
    #print site
    for host in hosts:
        status = servidores[host]['status']
        description = servidores[host]['description']

        if (status == 'ENABLED_STATUS_ENABLED' and description != 'Pool member is available') or (status != 'ENABLED_STATUS_ENABLED'):
            agentes_fora_balance.append(str(host) + ' - ' + str(site) + ' - ' + str(servidores[host]))

  
texto = ''
for agente in agentes_fora_balance:
    texto += '<li>' + agente + '</li>'

print('RESULTADO_' + texto+ '_FIM')


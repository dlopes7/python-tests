import sys
import requests
import time

import icontrol as viprion


'''
Script para monitorar as paginas da CNOVA
Se baseia nas maquinas que estao no balance do Viprion e do BIG IP

Se a maquina estiver fora do balance, nao e testada
Parametros
<url> (Url a ser testada)
<tipo_monitoria> (compression, monitoria.aspx ou balance)
'''


monitoria_aspx, compression, balance, imagens = False, False, False, False
rodar = True

#Palavra a ser testada no caso de monitoria.aspx
palavra = 'Sucesso'

#Primeiro parametro, URL
url = str(sys.argv[1])

#Segundo parametro, tipo de monitoria
if len(sys.argv) == 3:
    if str(sys.argv[2]) == 'monitoria.aspx':
        uri = str(sys.argv[2])
        monitoria_aspx = True
    elif str(sys.argv[2]) == 'compression':
        uri = ''
        compression = True
    elif str(sys.argv[2]) == 'balance':
        uri = ''
        balance = True
    elif str(sys.argv[2]) == 'imagens':
        uri = 'Js/TagManager/loader.js'
        #Js/utilsP.js
        imagens = True
        palavra = 'function'
    else:
        print('RESULTADO_Falha! segundo argumento deve ser "monitoria", "compression" ou "balance"_FIM')
        rodar = False
else:
    print 'RESULTADO_Erro, parametros devem ser "<url> <balance|compression|monitoria.aspx>"_FIM'
    rodar = False



#Mapeamento de URLs para Pools (Viprion)
url_pool_viprion = {
            'www.pontofrio.com.br':'/Common/AJAX_HTTP',
            'carrinho.pontofrio.com.br': '/Common/AJAXCARRINHO_HTTP',
            'imagens.pontofrio.com.br': '/Common/ROMA_HTTP',
            'busca.pontofrio.com.br': '/Common/AJAXBUSCA_HTTP',
            'rec.pontofrio.com.br': '/Common/AJAXRECOMENDACAO_HTTP',
            
            'www.casasbahia.com.br': '/Common/DALLAS_HTTP',
            'carrinho.casasbahia.com.br': '/Common/DALLASCARRINHO_HTTP',
            'imagem.casasbahia.com.br': '/Common/PARMA_HTTP',
            'busca.casasbahia.com.br': '/Common/DALLASBUSCA_HTTP',
            'rec.casasbahia.com.br': '/Common/DALLASRECOMENDACAO_HTTP',
            
            'www.extra.com.br': '/Common/CHELSEA_HTTP',
            'carrinho.extra.com.br': '/Common/CHELSEACARRINHO_HTTP',
            'imagens.extra.com.br': '/Common/LAZIO_HTTP',
            'busca.extra.com.br': '/Common/CHELSEABUSCA_HTTP',
            'rec.extra.com.br': '/Common/CHELSEARECOMENDACAO_HTTP',
            
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
            'servicos.nike.com.br': '/Common/CORITIBA_HTTP',

            'imagens.pontofrioatacado.com.br': '/Common/TOTTENHAM_HTTP',
            'servicos.gpa.net.br': '/Common/ARSENAL_HTTP',
            }

#Mapeamento de URLs para Pools (BigIP)
url_pool_big_ip = {}




#*********** USUARIO E SENHA ***********#
usuario = '<usuario>'               #
senha = '<senha>'                      #
#***************************************#

#Define se vamos buscar dados no Viprion ou no BigIP
try:
    pool = url_pool_viprion[url]
    ip = '10.128.7.253' 
except KeyError, e:
    pool = url_pool_big_ip[url]
    ip = '10.128.7.8' 

#Se for pra realizar a monitoria    
if rodar:
    
    #Metodo que traz a lista de PoolMembers de um pool do Viprion/BIG IP
    #Recebe o nome do pool, IP do BigIP, usuario e senha
    #{'DALLAS004': {
    #   'ip':'10.128.43.27'
    #   'nome': }
    servidores =  viprion.get_pool_members(pool, ip, usuario, senha)

    #Header necessario para simular o "arquivo hosts"
    headers = {"Host": url }

    #Cor das metricas no HTML do email
    cor = 'black'

    
    print 'RESULTADO_<br>',
    for nome, detalhes in servidores.items():
      
        #Monitoria ASPX para as que nao tem monitoria.aspx
        #Paginas como busca.cdiscount.com.br, testamos a pagina em si
        if url == 'busca.cdiscount.com.br':
            palavra = 'roupa'
            uri = '?strBusca=roupa'
        if url == 'www.nike.com.br':
            palavra = 'nike'
            uri = ''
            

        if monitoria_aspx:
            #Se a maquina estiver habilitada no BigIP/Viprion
            if detalhes['status'] == 'ENABLED_STATUS_ENABLED' and detalhes['description'] == 'Pool member is available':
                try:
                    r = requests.get('http://{ip}/{uri}'.format(ip=detalhes['ip'], uri=uri), headers=headers, timeout=60)
                    teste = palavra in r.text
                    if teste:
                        resultado = 'OK! (' + str(r.status_code) + ')'
                        cor = 'black'
                    else:
                        resultado = 'Falha! (' + str(r.status_code) + ') - Palavra ' + palavra + ' nao encontrada'
                        cor = 'red'

                except Exception, e:
                    resultado = 'Falha! - ' + str(e)
                    cor = 'red'
                print '<font color="'+ cor +'">',nome, detalhes['ip'], resultado, '</font>'

        if imagens:
            #Se a maquina estiver habilitada no BigIP/Viprion
            if detalhes['status'] == 'ENABLED_STATUS_ENABLED' and detalhes['description'] == 'Pool member is available':
                try:
                    t0 = time.time()
                    r = requests.get('http://{ip}/{uri}'.format(ip=detalhes['ip'], uri=uri), headers=headers, timeout=60)
                    tempo_resposta = time.time() - t0
                    teste = palavra in r.text
                    if teste:
                        resultado = 'OK! (' + str(r.status_code) + ') ' + '{0:.2f}'.format(tempo_resposta) + 's'
                        cor = 'black'
                    else:
                        resultado = 'Falha! (' + str(r.status_code) + ') - Palavra ' + palavra + ' nao encontrada'
                        cor = 'red'
                except Exception, e:
                    resultado = 'Falha! - ' + str(e)
                    cor = 'red'
                    
                if not tempo_resposta:
                    tempo_resposta = time.time() - t0
                    resultado += ' '+ '{0:.2f}'.format(tempo_resposta)
                    
                print '<font color="'+ cor +'">',nome, detalhes['ip'], resultado, '</font>'

        if compression:
            if detalhes['status'] == 'ENABLED_STATUS_ENABLED' and detalhes['description'] == 'Pool member is available':
                try:
                    r = requests.get('http://{ip}/{uri}'.format(ip=detalhes['ip'], uri=uri), headers=headers, timeout=60)
                    compressao = r.headers['Content-Encoding']
                    if compressao:
                        resultado = 'OK! (' + str(r.status_code) + ')' + ' - ' + 'Content-Encoding: ' + str(compressao) 
                        cor = 'black'
                    else:
                        resultado = 'Falha! (' + str(r.status_code) + ')'
                        cor = 'red'
                except Exception, e:
                    resultado = 'Falha! - ' + str(e) + ' - Header nao encontrado'
                    cor = 'red'
                print '<font color="'+ cor +'">',nome, detalhes['ip'], resultado, '</font>'

        if balance:
            if (detalhes['status'] == 'ENABLED_STATUS_ENABLED' and detalhes['description'] == 'Pool member is available') or detalhes['description'] == 'Pool member does not have service checking enabled':
                resultado = 'OK! Maquina no balance'
                cor = 'black'
            elif detalhes['status'] != 'ENABLED_STATUS_ENABLED':
                resultado = 'OK! Maquina fora do balance'
                cor = 'gray'
            elif detalhes['status'] == 'ENABLED_STATUS_ENABLED' and detalhes['description'] != 'Pool member is available' and detalhes['description'] != 'Pool member does not have service checking enabled':
                resultado = 'Falha! Maquina fora do balance ' + str(detalhes['description']) 
                cor = 'red'
            print '<font color="'+ cor +'">',nome, detalhes['ip'], resultado, '</font>'
                
    print '_FIM',

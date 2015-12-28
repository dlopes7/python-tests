import re
import requests
import os
import sys

from bs4 import BeautifulSoup
from PIL import Image


def get_lista_imagens(url):
    """
    Metodo que captura todas as imagens de uma pagina html
    Retorna a lista de imagens unicas sorteada em ordem alfabetica
    """

    endereco = url['url']
    parametros = url['parameters']

    imagens = []
    try:
        page = BeautifulSoup(requests.get('{url}'.format(url=endereco), params=parametros).text, 'html.parser' )
    except:
        return
    #Para cada tag <img> obter o src, data-src ou data-lazy dependendo da disponibilidade de cada atributo
    for imagem in page.findAll('img'):
        if imagem.get('src', ''):
            imagens.append(imagem.get('src', ''))
        elif imagem.get('data-src', ''):
            imagens.append(imagem.get('data-src', ''))
        elif imagem.get('data-lazy', ''):
            imagens.append(imagem.get('data-lazy', ''))

    #ordena e elimina duplicados da lista de imagens
    #alem disso elimina arquivos que nao terminem com formatos conhecidos de imagens (caso ArquivoExibir.aspx)
    for imagem in sorted(list(set(imagens))):
        if('imagens.com.br' in imagem and (imagem.endswith('.jpg') or imagem.endswith('.gif') or imagem.endswith('.png') or imagem.endswith('.bmp'))):
            yield imagem.replace('\\', '/')

def get_lista_arquivos(lista):
    """
    Metodo monta um dicionario de imagens de certa bandeira
    Server para ser usado depois para encontrar as imagens no fs-front
    """    
    dicionario = {}

    #obtem a bandeira de cada imagem e adiciona a imagem na lista da bandeira X no dicionario
    for link in lista:
        bandeira = re.match('.*?www.(.*?)-imagens', link)
        caminho = re.match('.*?com.br(.*)', link)
        if bandeira and caminho:
            bandeira = bandeira.group(1)
            caminho = caminho.group(1)
        else:
            pass
        try:
            dicionario[bandeira].append(caminho)
        except KeyError:
            dicionario[bandeira] = [caminho, ]
    return dicionario

def get_tamanho_dimensao(dicionario):
    """
    Metodo que obtem o tamanho e a dimensao de um dicionario de imagens de uma certa bandeira
    retorna um dicionario de imagens com seu tamanho e dimensoes
    """ 
    resultado_arquivos = {}
    path_front = {'extra': '//fsfront.dc.nova/SITES/SITE-EXTRA',
                  'casasbahia': '//fsfront.dc.nova/SITES/SITE-CASASBAHIA',
                  'pontofrio': '//fsfront.dc.nova/SITES/SITE-PONTOFRIO',}
    

    for bandeira, arquivos in dicionario.iteritems():
        caminho_front = path_front[bandeira]
        for arquivo in arquivos:
            caminho_arquivo = caminho_front + arquivo

            #tamanho do arquivo em bytes
            tamanho = os.path.getsize(caminho_arquivo)
            #dimensao do arquivo no formato (pixels_x, pixels_y)   
            dimensoes = Image.open(caminho_arquivo).size
            
            resultado_arquivos[arquivo] = {'tamanho': tamanho, 'dimensoes': dimensoes}
            #print caminho_arquivo, resultado_arquivos[arquivo]
    return resultado_arquivos

def valida_thresholds(bandeira, arquivos):
    """
    Metodo que checa se as imagens de um dicionario seguem os limites pre definidos
    retorna um dicionario das imagens com a informacao de Erro ou Ok
    """ 
    maximo = 10**7

    #Regras passadas por thiago.chichorro@cnova.com do Marketing 
    regras = {'casasbahia': {'banner-tv-dept': {'formato': (1920, 380), 'peso': 200000},
                             'banner-tv': {'formato': (1920, 380), 'peso': 200000},
                             'banner-retangulo': {'formato': (300, 250), 'peso': 100000},
                             'banner-superbanner': {'formato': (728, 90), 'peso': 100000},
                             'super-banner': {'formato': (728, 90), 'peso': 100000},
                             'superbanner': {'formato': (728, 90), 'peso': 100000},
                             'banner-lateral': {'formato': (maximo, maximo), 'peso': maximo},
                             'other': {'formato': (1920, 447), 'peso': 200000},
                             'img/thumb': {'formato': (45, 45), 'peso': 30000},
                             '/banner/mobile/': {'formato': (maximo, maximo), 'peso': maximo},
                             '/mobile/': {'formato': (maximo, maximo), 'peso': maximo},
                             },
              'extra':      {'banner-tv-dept': {'formato': (1920, 380), 'peso': 200000},
                             'banner-tv': {'formato': (1920, 447), 'peso': 200000},
                             'banner-retangulo': {'formato': (300, 250), 'peso': 100000},
                             'banner-superbanner': {'formato': (728, 90), 'peso': 100000},
                             'super-banner': {'formato': (728, 90), 'peso': 100000},
                             'superbanner': {'formato': (728, 90), 'peso': 100000},
                             'banner-lateral': {'formato': (maximo, maximo), 'peso': maximo},
                             'other': {'formato': (1920, 447), 'peso': 200000},
                             'img/thumb': {'formato': (45, 45), 'peso': 30000},
                             '/banner/mobile/': {'formato': (maximo, maximo), 'peso': maximo},
                             '/mobile/': {'formato': (maximo, maximo), 'peso': maximo},
                             },
              'pontofrio':  {'banner-tv-dept': {'formato': (1920, 380), 'peso': 200000},
                             'banner-tv': {'formato': (1920, 400), 'peso': 200000},
                             'banner-retangulo': {'formato': (300, 250), 'peso': 100000},
                             'banner-superbanner': {'formato': (728, 90), 'peso': 100000},
                             'super-banner': {'formato': (728, 90), 'peso': 100000},
                             'superbanner': {'formato': (728, 90), 'peso': 100000},
                             'banner-lateral': {'formato': (maximo, maximo), 'peso': maximo},
                             'other': {'formato': (1920, 447), 'peso': 200000},
                             'img/thumb': {'formato': (45, 45), 'peso': 30000},
                             '/banner/mobile/': {'formato': (maximo, maximo), 'peso': maximo},
                             '/mobile/': {'formato': (maximo, maximo), 'peso': maximo},
                             },
              }
    
    regra = regras[bandeira]
    t_tamanho, t_x, t_y = None, None, None
    
    for arquivo, detalhes in arquivos.iteritems():
        regra_encontrada = False
        for chave in regra.keys():
            if chave in arquivo.lower():
                t_tamanho = regra[chave]['peso']
                t_x = regra[chave]['formato'][0]
                t_y = regra[chave]['formato'][1]
                regra_encontrada = True
                break
        if regra_encontrada == False:
             t_tamanho, t_x, t_y = None, None, None

        if(t_tamanho and t_x and t_y):
            if(detalhes['tamanho'] > (t_tamanho * 1.3)):
                detalhes['status'] = 'Erro! Tamanho do arquivo ({tamanho} bytes) maior que {t_tamanho} bytes'.format(tamanho=detalhes['tamanho'], t_tamanho=t_tamanho)
            elif (detalhes['dimensoes'][0] > (t_x * 1.3) or detalhes['dimensoes'][1] > (t_y * 1.3)):
                detalhes['status'] = 'Erro! Dimensao do arquivo {dimensoes} maior que {t_dimensoes}'.format(dimensoes=detalhes['dimensoes'], t_dimensoes = (t_x, t_y))
            else:
                detalhes['status'] = 'Ok'
        else:
            detalhes['status'] = 'Ok'        
    return arquivos

def imprime_erros(arquivos):
    """
    Metodo que imprime a informacao dos arquivos que estiverem fora dos limites
    imprime no formato esperado pelo sitescope /RESULTADO_(.*?)_FIM/s
    """ 
    
    erros = ''
    for arquivo, detalhes in arquivos.iteritems():
        if detalhes['status'] != 'Ok':
            erros += '<br>{arquivo}: {status}'.format(arquivo=arquivo, status=detalhes['status'])

    print ('RESULTADO_{erros}_FIM'.format(erros = erros))
            

    

def get_bandeira_from_url(url):
    """
    Metodo que tenta advinhar a bandeira com base em uma URL
    www.bandeira.com.br
    m.bandeira.com.br
    """ 
    bandeira = re.match('.*?www.(.*?).com.br', url)
    if bandeira:
        return bandeira.group(1) 
    else:
        bandeira = re.match('.*?m.(.*?).com.br', url)
        if bandeira:
            return bandeira.group(1) 
        else:
            return None

def get_lista_departamentos(bandeira):
    departamentos = {'extra':  [{'url': 'http://www.extra.com.br/ArVentilacao/', 'parameters': {'Filtro': 'C2809', 'nid': '200663'}},
                                {'url': 'http://www.extra.com.br/BelezaSaude/', 'parameters': {'Filtro': 'C102', 'nid': '200669'}},
                                {'url': 'http://www.extra.com.br/CineFoto/', 'parameters': {'Filtro': 'C29', 'nid': '200675'}},
                                {'url': 'http://www.extra.com.br/EletrodomesticosLinhaIndustrial/', 'parameters': {'Filtro': 'C1017', 'nid': '200686'}},
                                {'url': 'http://www.extra.com.br/Eletronicos/', 'parameters': {'Filtro': 'C1', 'nid': '200700'}},
                                {'url': 'http://www.extra.com.br/Eletroportateis/', 'parameters': {'Filtro': 'C73', 'nid': '200678'}},
                                {'url': 'http://www.extra.com.br/EsporteLazer/', 'parameters': {'Filtro': 'C418', 'nid': '200679'}},
                                {'url': 'http://www.extra.com.br/EsporteLazer/SuplementosAlimentares/', 'parameters': {'Filtro': 'C418_C2667', 'nid': '200697'}},
                                {'url': 'http://www.extra.com.br/Ferramentas/', 'parameters': {'Filtro': 'C827', 'nid': '200680'}},
                                {'url': 'http://www.extra.com.br/Flores/', 'parameters': {'Filtro': 'C1900', 'nid': '200681'}},
                                {'url': 'http://www.extra.com.br/Games/', 'parameters': {'Filtro': 'C336', 'nid': '200682'}},
##                                {'url': 'http://www.extra.com.br/Informatica/', 'parameters': {'Filtro': 'C56', 'nid': '200683'}},
##                                {'url': 'http://www.extra.com.br/Moveis/', 'parameters': {'Filtro': 'C93', 'nid': '200690'}},
##                                {'url': 'http://www.extra.com.br/Perfumaria/', 'parameters': {'Filtro': 'C1886', 'nid': '200693'}},
##                                {'url': 'http://www.extra.com.br/ProdutosdeLimpeza/', 'parameters': {'Filtro': 'C2285', 'nid': '200695'}},
##                                {'url': 'http://www.extra.com.br/Relogios/', 'parameters': {'Filtro': 'C1733', 'nid': '200696'}},
##                                {'url': 'http://www.extra.com.br/TelefoneseCelulares/', 'parameters': {'Filtro': 'C38', 'nid': '200699'}},
##                                {'url': 'http://www.extra.com.br/UtilidadesDomesticas/', 'parameters': {'Filtro': 'C371', 'nid': '200701'}},
##                                {'url': 'http://www.extra.com.br/artesanato/', 'parameters': {'Filtro': 'C2599', 'nid': '200664'}},
##                                {'url': 'http://www.extra.com.br/artigosparafestas/', 'parameters': {'Filtro': 'C2894', 'nid': '200665'}},
##                                {'url': 'http://www.extra.com.br/audio/', 'parameters': {'Filtro': 'C3279', 'nid': '200666'}},
##                                {'url': 'http://www.extra.com.br/automotivo/', 'parameters': {'Filtro': 'C836', 'nid': '200667'}},
##                                {'url': 'http://www.extra.com.br/bebes/', 'parameters': {'Filtro': 'C983', 'nid': '200668'}},
##                                {'url': 'http://www.extra.com.br/bebidas/', 'parameters': {'Filtro': 'C2596', 'nid': '200702' }},
##                                {'url': 'http://www.extra.com.br/brinquedos/', 'parameters': {'Filtro': 'C977', 'nid': '200671'}},
##                                {'url': 'http://www.extra.com.br/calcados/', 'parameters': {'Filtro': 'C448', 'nid': '200672'}},
##                                {'url': 'http://www.extra.com.br/camamesabanho/', 'parameters': {'Filtro': 'C1732', 'nid': '200673'}},
##                                {'url': 'http://www.extra.com.br/construcao/', 'parameters': {'Filtro': 'C2547', 'nid': '200674'}},
##                                {'url': 'http://www.extra.com.br/dvdsebluray/', 'parameters': {'Filtro': 'C833', 'nid': '200676'}},
##                                {'url': 'http://www.extra.com.br/eletrodomesticos/', 'parameters': {'Filtro': 'C13', 'nid': '200677'}},
##                                {'url': 'http://www.extra.com.br/instrumentosmusicais/', 'parameters': {'Filtro': 'C2471', 'nid': '200684'}},
##                                {'url': 'http://www.extra.com.br/joias/', 'parameters': {'Filtro': 'C2168', 'nid': '200685'}},
##                                {'url': 'http://www.extra.com.br/livros/', 'parameters': {'Filtro': 'C484', 'nid': '200687'}},
##                                {'url': 'http://www.extra.com.br/malasmochilas/', 'parameters': {'Filtro': 'C1813', 'nid': '200688'}},
##                                {'url': 'http://www.extra.com.br/moda/', 'parameters': {'Filtro': 'C1734', 'nid': '200689'}},
##                                {'url': 'http://www.extra.com.br/natal/', 'parameters': {'Filtro': 'C2042', 'nid': '200792'}},
##                                {'url': 'http://www.extra.com.br/papelaria/', 'parameters': {'Filtro': 'C1639', 'nid': '200692'}},
##                                {'url': 'http://www.extra.com.br/petshop/', 'parameters': {'Filtro': 'C2294', 'nid': '200694'}},
##                                {'url': 'http://www.extra.com.br/promocoes/blackfriday.aspx', 'parameters': {'nid=200507'}},
##                                {'url': 'http://www.extra.com.br/tablets/', 'parameters': {'Filtro': 'C2031', 'nid': '200698'}},
                                ],
                     }
    return departamentos[bandeira]

       

if __name__ == '__main__':
    url = sys.argv[1]
    if (not url.startswith('http')):
        url = 'http://{url}'.format(url=url)
    #url = 'www.extra.com.br'
    
    bandeira = get_bandeira_from_url(url)
    
    if len(sys.argv) == 3:
        adicional = {'departamentos': get_lista_departamentos(bandeira)}
        lista_urls = adicional[sys.argv[2]]
        
    elif len(sys.argv) == 2:
        lista_urls = [{'url': url, 'parameters': None},]
    
    lista_de_imagens = []

    for url in lista_urls:
        print url
        lista_de_imagens += get_lista_imagens(url)
  
    dicionario_arquivos_front = get_lista_arquivos(lista_de_imagens)
    detalhes = get_tamanho_dimensao(dicionario_arquivos_front)
    validados = valida_thresholds(bandeira, detalhes)

    imprime_erros(validados)


import os
import datetime
import sys

'''
Script que verifica se a data de modificacao de um arquivo
e a mesma da data atual e se o tamanho e maior que um certo limite
David Lopes - david.lopes@cnova.com (TI Monitoria)
'''


def modification_date(filename):
    '''
    Metodo que obtem a data de modificacao de um arquivo
    Parametro: caminho completo do arquivo
    Retorno: Data de modiicacao do arquivo
    '''
    
    t = os.path.getmtime(filename)

    #Retorna um objeto DATETIME do Python, somente com o dia mes e ano
    return datetime.datetime.fromtimestamp(t).date()

def get_tamanho(filename):
    '''
    Metodo que obtem o tamanho de um arquivo
    Parametro: caminho completo do arquivo
    Retorno: Tamanho em MB do arquivo
    '''
    
    tamanho = os.path.getsize(filename)
    return tamanho / float(10**6)


def imprime_resultado(texto):
    '''
    Metodo para imprimir o resultado para ser usado no REGEX do Sitescope
    Parametro: texto
    '''
    print ('RESULTADO_' + texto + '_FIM')


try:

    #Argumentos do Script BANDEIRA ARQUIVO THRESHOLD
    #Exemplo arquivos_mobile.py CasasBahia MobileCompleto.zip 100
    bandeira = str(sys.argv[1])
    arquivo = str(sys.argv[2])
    threshold = int(sys.argv[3])

    #Caminho passado pelo Fabio Lanza onde estao os arquivos
    caminho = r'\\fs-front\webshare\Mobile\\' + bandeira + '\\'+ arquivo

    #Data de Hoje
    hoje = datetime.datetime.today().date()

    #Data de modificacao e tamanho do arquivo
    data_modificado = modification_date(caminho)
    tamanho_arquivo = get_tamanho(caminho)


    #Escrevendo no arquivo de log
    #Exemplo:
    #2015-08-31 10:40:10.139000: (2015-08-31 = 2015-08-31)? - (True) - (25.620538> 15)? - (True)  - OK!
    with open('D:\\SiteScope\\scripts\log\\geracao_xml.log', 'a') as arq:
        arq.write(str(datetime.datetime.now()) + ': (' + str(hoje) + ' = ' + str(data_modificado) + ')? - (' + str(hoje == data_modificado) + ') - (' +
                  str(tamanho_arquivo) + '> ' + str(threshold) + ')? - (' + str(tamanho_arquivo > threshold) + ') ')

    #Se a data for a de hoje e o tamanho for maior que o threshold
    if(hoje == data_modificado and tamanho_arquivo > threshold):
       imprime_resultado('Ok! - ' + arquivo +
                         '<br>modificado em ' + str(data_modificado) +
                         '<br>tamanho: ' + str(tamanho_arquivo) + ' MB')
       with open('D:\\SiteScope\\scripts\log\\geracao_xml.log', 'a') as arq:
           arq.write(' - OK!\n')
    #Caso nao
    else:
       imprime_resultado('Falha! - ' + arquivo +
                         '<br>modificado em ' + str(data_modificado) +
                         '<br>tamanho: ' + str(tamanho_arquivo) + ' MB')
       with open('D:\\SiteScope\\scripts\log\\geracao_xml.log', 'a') as arq:
           arq.write(' - Falha!\n')

#Em caso de erros, imprimir no mesmo formato para que o sitescope reporte
except Exception, e:
    imprime_resultado('Falha no script! ' + str(e) )
    with open('D:\\SiteScope\\scripts\log\\geracao_xml.log', 'a') as arq:
           arq.write(' - Falha no script! ' + str(e)  + '\n')
       
   




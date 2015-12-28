
import os
import datetime
import sys
import time



'''
Script que calcula ha quantos minutos um arquivo foi modificado.

David Lopes - david.lopes@cnova.com (TI Monitoria)
'''


def modification_date(filename):
    '''
    Metodo que obtem a data de modificacao de um arquivo
    Parametro: caminho completo do arquivo
    Retorno: Data de modiicacao do arquivo
    '''
    
    t = os.path.getmtime(filename)

    #Retorna um objeto DATETIME do Python
    return datetime.datetime.fromtimestamp(t)


def imprime_resultado(texto):
    '''
    Metodo para imprimir o resultado para ser usado no REGEX do Sitescope
    Parametro: texto
    '''
    print ('RESULTADO_' + texto + '_FIM')


try:

    #Argumentos do Script <caminho> <threshold_em_minutos>
    caminho = str(sys.argv[1])
    threshold = int(sys.argv[2])

    #Data de Hoje
    hoje = datetime.datetime.today()

    #Data de modificacao do arquivo
    data_modificado = modification_date(caminho)
	
    antes_unix =  time.mktime(data_modificado.timetuple())
    depois_unix =  time.mktime(hoje.timetuple())
    diferenca_minutos = int(depois_unix-antes_unix) / 60.0

    #Escrevendo no arquivo de log
    #Exemplo:
    #2015-08-31 10:40:10.139000: (2015-08-31 = 2015-08-31)? - (True) - (25.620538> 15)? - (True)  - OK!
    with open('D:\\SiteScope\\scripts\log\\modicacao_arquivos.log', 'a') as arq:
        arq.write(str(datetime.datetime.now()) + ': (' + str(hoje) + ' = ' + str(data_modificado) + ')? - (' + str(hoje == data_modificado))

    #Se a data for a de hoje e o tamanho for maior que o threshold
    if(diferenca_minutos < threshold):
       imprime_resultado('Ok! - ' + caminho +
                         '<br>modificado em ' + str(data_modificado))
       with open('D:\\SiteScope\\scripts\log\\modicacao_arquivos.log', 'a') as arq:
           arq.write(' - OK!\n')
    #Caso nao
    else:
       imprime_resultado('Falha! - ' + caminho +
                         '<br>modificado em ' + str(data_modificado))
       with open('D:\\SiteScope\\scripts\log\\modicacao_arquivos.log', 'a') as arq:
           arq.write(' - Falha!\n')

#Em caso de erros, imprimir no mesmo formato para que o sitescope reporte
except Exception, e:
    imprime_resultado('Falha no script! ' + str(e) )
    with open('D:\\SiteScope\\scripts\log\\modicacao_arquivos.log', 'a') as arq:
           arq.write(' - Falha no script! ' + str(e)  + '\n')
       
   

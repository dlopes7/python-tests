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
    return datetime.datetime.fromtimestamp(t) #.date()

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
    arquivo_1 = str(sys.argv[2])
    arquivo_2 = str(sys.argv[5])
    
    threshold_t1 = int(sys.argv[3])
    threshold_t2 = int(sys.argv[6])

    threshold_m1 = int(sys.argv[4])
    threshold_m2 = int(sys.argv[7])
    
    #bandeira = 'extra'
    arquivos = {'xml': arquivo_1,
                'zip': arquivo_2}
    
    thresholds_tamanho = {'xml': threshold_t1,
                  'zip': threshold_t2}

    thresholds_minutos = {'xml': threshold_m1,
                  'zip': threshold_m2}

    #Caminho passado pelo Tiago Magri (Front)

    caminho = r'\\fs-front\WEBSHARE\FTP-PARCEIRO\slifeed\\' + bandeira + '\\'

    #Data de Hoje
    hoje = datetime.datetime.today()

    #Data de modificacao e tamanho do arquivo

    erros = []
    sucesso = ''

    for formato in arquivos.keys():     #arquivos[zip]
        tamanho = get_tamanho(caminho + arquivos[formato])
        if tamanho < thresholds_tamanho[formato]:
            erros.append('TAMANHO: ' + arquivos[formato] + ' (' + str(tamanho) + 'MB)')
        else:
            sucesso += arquivos[formato] + ' (' + str(tamanho) + 'MB) '
            
        data_modificado = modification_date(caminho + arquivos[formato])
        minutos_atras = (hoje - data_modificado).seconds // 60

        if minutos_atras > thresholds_minutos[formato]:
            erros.append('MODIFICADO: ' + arquivos[formato] + ' modificado ha ' + str(minutos_atras) + ' minutos')
        else:
            sucesso += 'modificado ha ' + str(minutos_atras) + ' minutos atras<br>'

        with open('D:\\SiteScope\\scripts\log\\geracao_sli.log', 'a') as arq:
            arq.write(str(datetime.datetime.now()) + ': ' + bandeira + ': Arquivo: '+ arquivos[formato] +' Datas: ' + str(hoje) + ' - ' + str(data_modificado) + ': ' +
                      str(minutos_atras) + ' minutos Tamanho: ' + 
                  str(tamanho) + ' > ' + str(thresholds_minutos[formato]) + '? (' + str(tamanho > thresholds_minutos[formato]) + ')\n')



    mensagem = ''
    if(len(erros) > 0):
        for erro in erros:
            mensagem += erro + '<br>'
        imprime_resultado('Falha!<br>' + mensagem)
    else:
        imprime_resultado('OK!<br>' + sucesso)




#Em caso de erros, imprimir no mesmo formato para que o sitescope reporte
except Exception, e:
    imprime_resultado('Falha no script! ' + str(e) )
    with open('D:\\SiteScope\\scripts\log\\geracao_sli.log', 'a') as arq:
           arq.write(str(datetime.datetime.now()) + ': Falha no script! ' + str(e)  + '\n')
       
   




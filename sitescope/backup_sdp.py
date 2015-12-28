import os, time, datetime

'''
Script que lista os arquivos de um diretorio e
verifica se a data de modificacao e a mesma data do dia anterior
Criado por David Lopes
davidribeirolopes@gmail.com
'''


#Apenas para facilitar o Regex do lado do Sitescope - /RESULTADO_(.*?)_FIM/
def imprime_resultado(texto):
    print ('RESULTADO_' + texto + '_FIM')


#Cria a data de acordo com o formato de data do os.listdir
ontem = str(datetime.date.fromordinal(datetime.date.today().toordinal()-1)).split('-')
mes, dia, ano = ontem[1], ontem[2], ontem[0]
data = mes + '_' + dia + '_' + ano

#Lista de arquivos encontrados
lista_arquivos = []

try:
    #primeiro listo os diretorios na pasta BACKUP
    for dir in os.listdir(r"\\10.128.75.16\d$\BACKUP"):
        #se existe um diretorio com a data do dia anterior no nome
        if data in dir:
            #adiciono os arquivos nesse diretorio na lista de arquivos
            for arq in os.listdir(r"\\10.128.75.16\\d$\\BACKUP\\" + dir):
                lista_arquivos.append(arq + '<br>')

    #caso existam arquivos imprimo a lista de arquivos com um Ok! na frente
    if len(lista_arquivos) > 0:
        imprime_resultado ('<br>Ok! ' + str(len(lista_arquivos)) + ' arquivos criados:<br>' +  ''.join(lista_arquivos))

    #caso nao existam arquivos imprime Erro
    else:
        imprime_resultado ('<br>Falha! Nenhum arquivo de backup criado!')

#caso ocorra qualquer erro de leitura, imprime o erro
except Exception, err:
    imprime_resultado('Falha! Nenhum arquivo de backup criado! ' + str(err))
        


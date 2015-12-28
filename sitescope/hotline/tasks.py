import re
import dateutil.parser

#2015-10-12T11:38:16.005
#
with open('D:\SiteScope\scripts\python\hotline\data_ultimo.log', 'r') as ultimo:
    data_mais_recente = dateutil.parser.parse(ultimo.readline())

with open(r'D:\SiteScope\scripts\python\hotline\eventos.log', 'r') as arquivo:
    eventos = {}
    eventos_analizar = {}
    primeiro = True
    completo = False
    analizar = False
    
    for linha in arquivo.readlines():
        
        
        if 'Event[' in linha:
            novo = True
            id_evento = re.match('Event\[(.*?)\]', linha)
            if id_evento:
                num_id =  int(id_evento.group(1))
                eventos[num_id] = {}
        if linha == '\n':
            novo = False
         
        if novo:
            linha = linha.rstrip('\n')
            linha = linha.lstrip(' ')
            splitted = linha.split(':', 1)

            if len(splitted) == 2 and splitted[1] != '':
                completo = False
                chave, valor = splitted
                eventos[num_id][chave] = valor.lstrip(' ')
                
                    
                if chave == 'Date':
                    data = dateutil.parser.parse(valor)
                    
                    if primeiro:
                        with open('D:\SiteScope\scripts\python\hotline\data_ultimo.log', 'w') as ultimo:
                            ultimo.write(str(data))
                        primeiro = False
                    
                    if data > data_mais_recente:
                        analizar = True
                    else:
                        analizar = False
                        continue

  
            elif len(splitted) == 1 and 'Task Scheduler ' in splitted[0]:
                eventos[num_id]['Description'] = splitted[0]
                completo = True
           
        if analizar and completo:
            eventos_analizar[num_id] = eventos[num_id]          



print 'RESULTADO_'
try:
    for evento, dados in eventos_analizar.items():
        if 'of the same task is already running' in dados['Description'] or 'Task Start Failed' in dados['Task']:
            continue
        print '<br>Evento:', evento, '<br>',
        print 'Description:', dados['Description'], '<br>',
        print 'Level:', dados['Level'], '<br>',
        print 'Opcode:', dados['Opcode'], '<br>',
        print 'Date:', dados['Date'], '<br>',
        print 'User Name:', dados['User Name'], '<br>',
        print 'Event ID:', dados['Event ID'], '<br>',
        print 'Task:', dados['Task'], '<br>',
except:
        pass    
print '_FIM'


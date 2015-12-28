import urllib2, urllib
import re

import sys

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

telefones = str(sys.argv[1]).replace('\"','').split('_')
monitor_name = str(sys.argv[2])
monitor_status = str(sys.argv[3])
prefixo = str(sys.argv[4])
arquivo_metricas = str(sys.argv[5])

alertas = []

#print 'Abrindo', arquivo_metricas

try:
	f = open(arquivo_metricas, 'r')
except Exception,e: 
	print str(e)
	
capture = False
conteudo = f.readlines()

for i in xrange(len(conteudo) - 1):
        #print(conteudo[i], conteudo[i+1], capture)
        if capture == True and (conteudo[i] == '\n' or 'The thresholds' in conteudo[i]):
                break
        if 'The thresholds' in conteudo[i] and conteudo[i+1] != '\n':
                #print 'OPA CAPTURE TRUE'
                capture = True
                continue
        if capture == True:
                alertas.append(conteudo[i].replace('\n', ''))
                

#print (alertas)
f.close()


mensagem = 'ALERTA SITESCOPE: ' + prefixo +': '+ monitor_name + ' - ' + str(alertas)
mensagem = mensagem[0:150]

proxy_support = urllib2.ProxyHandler({"http":"http://10.128.131.16:3128"})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

for telefone in telefones:
	url = 'http://system.human.com.br:8080/GatewayIntegration/msgSms.do'
	values = {'dispatch': 'send',
			  'account': '<user>',
			  'code': '<code>',
			  'to': telefone,
			  'msg': mensagem}
	
	
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)

	response = urllib2.urlopen(req)
	
	resposta = response.read()
	#print resposta
	#print 'Enviei \"' +mensagem + '\" para: ' + telefone  

	response.close()


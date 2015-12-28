import httplib
import ssl
from bs4 import BeautifulSoup
import sys

servers = sys.argv[1].split('_')
#servers = ['CHELSEA008']
context = ssl._create_unverified_context()

print('RESULTADO_')

for server in servers:
    try:
        conn = httplib.HTTPSConnection(server + '.dc.nova', context=context)
        conn.request("GET", "/monitoria.aspx")
    except Exception, e:
        if 'Errno 10061' in str(e):
            conn = httplib.HTTPConnection(server + '.dc.nova')
            conn.request("GET", "/monitoria.aspx")
        if 'Errno 11004' in str(e):
            print server, '???', str(e)
            continue

            
    r1 = conn.getresponse()
    response_code, resposta = r1.status, r1.read()
    soup = BeautifulSoup(resposta, 'html.parser')
    div = soup.find(id="lblSucesso")

    if div is None:
        div = 'n/a'
    else:
        div = div.text
        
    print server, response_code, div


            
        #with open('D:/SiteScope/scripts/log/monitoria_aspx.log', 'a') as log:
        #    log.write(server + str(e))
        #    print server, '???', str(e)
        #pass
    
    
print('_FIM')



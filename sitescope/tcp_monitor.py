from fabric.api import run, env
from base64 import b64decode

def tail(f, window=20):
    """
    Returns the last `window` lines of file `f` as a list.
    """
    if window == 0:
        return []
    BUFSIZ = 1024
    f.seek(0, 2)
    bytes = f.tell()
    size = window + 1
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if bytes - BUFSIZ > 0:
            # Seek back one whole BUFSIZ
            f.seek(block * BUFSIZ, 2)
            # read BUFFER
            data.insert(0, f.read(BUFSIZ))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.insert(0, f.read(bytes))
        linesFound = data[0].count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1
    return ''.join(data).splitlines()[-window:]


with open('D:\\SiteScope\\scripts\log\\tcp_fernando.log', 'r') as fin:
    data = fin.read().splitlines(True)

    
with open('D:\\SiteScope\\scripts\log\\tcp_fernando.log', 'w') as fout:
    fout.writelines(data[-70:])

CMD='sudo python /root/tcp-monitor.py'

env.host_string = '10.128.67.29'
env.user = 'svc_monitoria'
env.password = b64decode('SFBAMjAxNENub3Zh')


#['apache_all=78', 'apache_wait=15', 'tm_apache_tcp=1', 'proxy_all=0', 'proxy_wait=0', 'tm_proxy_tcp=-1']

resultado = run(CMD)
resultado = str(resultado).replace('|', ';')

media_apache_all, media_apache_wait, media_tm_apache_tcp, media_proxy_all, media_proxy_wait, media_tm_proxy_tcp  = 0, 0, 0, 0, 0, 0

limite, count = 61.0, 1.0

for line in reversed(list(open('D:\\SiteScope\\scripts\log\\tcp_fernando.log'))):
    if count == limite:
        break
    dados = line.rstrip().replace(' ', '').split(';')[1:]

    if 'alertar' not in dados[0]: 
        media_apache_all += int(dados[0].split("=")[1]) #/ (count-1)
        media_apache_wait += int(dados[1].split("=")[1]) #/ (count-1)
        media_tm_apache_tcp += int(dados[2].split("=")[1]) #/ (count-1)
        media_proxy_all += int(dados[3].split("=")[1]) #/ (count-1)
        media_proxy_wait += int(dados[4].split("=")[1]) #/ (count-1)
        media_tm_proxy_tcp += int(dados[5].split("=")[1]) #/ (count-1)
        count += 1

media_apache_all /= count
media_apache_wait /= count
media_tm_apache_tcp /= count
media_proxy_all /= count
media_proxy_wait /= count
media_tm_proxy_tcp /= count

print media_tm_apache_tcp
 
VALOR_THRESHOLD = 1.5

novo_dado = resultado.replace(' ', '').split(';')[1:]
apache_all, apache_wait, tm_apache_tcp, proxy_all, proxy_wait, tm_proxy_tcp  = int(novo_dado[0].split("=")[1]), int(novo_dado[1].split("=")[1]), int(novo_dado[2].split("=")[1]), int(novo_dado[3].split("=")[1]), int(novo_dado[4].split("=")[1]), int(novo_dado[5].split("=")[1]) 

alertar_apache_all = apache_all >( media_apache_all * VALOR_THRESHOLD)
alertar_apache_wait = apache_wait >( media_apache_wait * VALOR_THRESHOLD)
alertar_tm_apache_tcp = tm_apache_tcp >( media_tm_apache_tcp * VALOR_THRESHOLD)
alertar_proxy_all = proxy_all >( media_proxy_all * VALOR_THRESHOLD)
alertar_proxy_wait = proxy_wait >( media_proxy_wait * VALOR_THRESHOLD)
alertar_tm_proxy_tcp = tm_proxy_tcp >( media_tm_proxy_tcp * VALOR_THRESHOLD)



if alertar_apache_all:
    alertar_apache_all = str(apache_all) + ' (' + str(media_apache_all * VALOR_THRESHOLD) + ')'
print ('apache_all=' + str(apache_all) + ' (' + str(media_apache_all * VALOR_THRESHOLD) + ')' + ';' + 'alertar_apache_all=' + str(alertar_apache_all) )

if alertar_apache_wait:
    alertar_apache_wait = str(apache_wait) + ' (' + str(media_apache_wait * VALOR_THRESHOLD) + ')'
print ('apache_wait=' +  str(apache_wait)  + ' (' + str(media_apache_wait * VALOR_THRESHOLD) + ')'+ ';' + 'alertar_apache_wait=' + str(alertar_apache_wait) )

if alertar_tm_apache_tcp:
    alertar_tm_apache_tcp = str(tm_apache_tcp) + ' (' + str(media_tm_apache_tcp * VALOR_THRESHOLD) + ')'
print ('tm_apache_tcp=' + str(tm_apache_tcp)  + ' (' + str(media_tm_apache_tcp * VALOR_THRESHOLD) + ')'+ ';' + 'alertar_tm_apache_tcp=' + str(alertar_tm_apache_tcp) )

if alertar_proxy_all:
    alertar_proxy_all = str(proxy_all) + ' (' + str(media_proxy_all * VALOR_THRESHOLD) + ')'
print ('proxy_all=' + str(proxy_all) + ' (' + str(media_proxy_all * VALOR_THRESHOLD) + ')'+ ';' + 'alertar_proxy_all=' + str(alertar_proxy_all) )

if alertar_proxy_wait:
    alertar_proxy_wait = str(proxy_wait) + ' (' + str(media_proxy_wait * VALOR_THRESHOLD) + ')'
print ('proxy_wait=' + str(proxy_wait)  + ' (' + str(media_proxy_wait * VALOR_THRESHOLD) + ')'+ ';' + 'alertar_proxy_wait=' + str(alertar_proxy_wait) )

if alertar_tm_proxy_tcp:
    alertar_tm_proxy_tcp = str(tm_proxy_tcp) + ' (' + str(media_tm_proxy_tcp * VALOR_THRESHOLD) + ')'
print ('tm_proxy_tcp=' + str(tm_proxy_tcp) + ' (' + str(media_tm_proxy_tcp * VALOR_THRESHOLD) + ')'+ ';' + 'alertar_tm_proxy_tcp=' + str(alertar_tm_proxy_tcp) )

with open('D:\\SiteScope\\scripts\log\\tcp_fernando.log', 'a') as f:
    f.write(resultado +
            ';alertar_apache_all=' + str(alertar_apache_all) +
            ';alertar_apache_wait=' + str(alertar_apache_wait) +
            ';alertar_tm_apache_tcp=' + str(alertar_tm_apache_tcp) +
            ';alertar_proxy_all=' + str(alertar_proxy_all) +
            ';alertar_proxy_wait=' + str(alertar_proxy_wait) +
            ';alertar_tm_proxy_tcp=' + str(alertar_tm_proxy_tcp) + '\n')



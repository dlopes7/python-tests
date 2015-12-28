from fabric.api import run, env
from base64 import b64decode
import sys


servidor = str(sys.argv[1])
CMD='/opt/zimbra/postfix/sbin/postqueue -p |tail -n1'

env.host_string = servidor
env.user = '<usuario>'
env.password = b64decode('<senha>')

resultado = run(CMD)

if 'empty' in resultado:
    resultado = '0'
else:
    resultado = resultado.split(' ')[4]

print 'RESULTADO_' + str(resultado) + '_FIM'





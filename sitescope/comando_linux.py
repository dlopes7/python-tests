from fabric.api import run, env
from base64 import b64decode
import sys


servidor = str(sys.argv[1])
CMD = str(sys.argv[2]).replace('PIPE', '|')

env.host_string = servidor
env.user = '<usuario>'
env.password = b64decode('<senha>')

resultado = run(CMD)
print 'RESULTADO_'  + str(resultado) + '_FIM'





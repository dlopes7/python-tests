from pymongo import MongoClient
import sys

#Nomes dos bancos
#Extra - npc_release
#Ponto Frio - npc_pontofrio_release
#Casas Bahia - cnova_mcommerce_casas_bahia_production

servidor = sys.argv[1]      #'PSG003.DC.NOVA'
database = sys.argv[2]      #'cnova_mcommerce_casas_bahia_production'
collection = sys.argv[3]    #'produtolista'

try:
    client = MongoClient(servidor, 27017)
    client.admin.authenticate('<usuario>', '<senha>')

    db = client[database]
    resultado = db[collection].count()
    print('RESULTADO_' + str(resultado) + '_FIM')

    client.close()
except Exception, e:
    print('RESULTADO_' + str(e) + '_FIM')

import urllib2
import ssl
from suds import transport
from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
from pycontrol import pycontrol

IMP = Import('http://schemas.xmlsoap.org/soap/encoding/')
DOCTOR = ImportDoctor(IMP)
ICONTROL_URI = '/iControl/iControlPortal.cgi'
SESSION_WSDL = 'System.Session'

class HTTPSUnVerifiedCertTransport(transport.https.HttpAuthenticated):
    def __init__(self, *args, **kwargs):
        transport.https.HttpAuthenticated.__init__(self, *args, **kwargs)
        
    def u2handlers(self):
        handlers = []
        handlers.append(urllib2.ProxyHandler(self.proxy))
        handlers.append(urllib2.HTTPBasicAuthHandler(self.pm)) # python ssl Context support - PEP 0466
        if hasattr(ssl, '_create_unverified_context'):
            ssl_context = ssl._create_unverified_context()
            handlers.append(urllib2.HTTPSHandler(context=ssl_context))
        else:
            handlers.append(urllib2.HTTPSHandler())
        return handlers

def new_get_suds_client(self, url, **kw):
    if not url.startswith("https"):
        t = transport.http.HttpAuthenticated(username=self.username, password=self.password)
        c = Client(url, transport=t, username=self.username, password=self.password, doctor=DOCTOR, **kw)
    else:
        t = HTTPSUnVerifiedCertTransport(username=self.username, password=self.password)
        c = Client(url, transport=t, username=self.username, password=self.password, doctor=DOCTOR, **kw)
    return c


def get_only_pool(nome, pools):
    for pool in pools:
        if pool == nome:
            return pool
    return None

def get_pool_members(monitorar, ip, usuario, senha):
    
    pycontrol.BIGIP._get_suds_client = new_get_suds_client
    device = pycontrol.BIGIP(hostname=ip, username=usuario, password=senha, fromurl=True, wsdls=['LocalLB.Pool'])
    device_member = pycontrol.BIGIP(hostname=ip, username=usuario, password=senha, fromurl=True, wsdls=['LocalLB.PoolMember'])
    

    pl = device.LocalLB.Pool
    mb = device_member.LocalLB.PoolMember
    pools = pl.get_list()

    servidores = {}

    pools_monitorar = get_only_pool(monitorar, pools)
    statuses = mb.get_object_status([pools_monitorar])[0]
    members_nomes =  pl.get_member_v2([pools_monitorar])[0]
    
    for status, nomes in zip(statuses, members_nomes):
        nome = str(nomes.address).replace('/Common/', '').replace('CARRINHO', '')
        ip = str(status.member.address)
        stat =  str(status.object_status.enabled_status)
        description = str(status.object_status.status_description)

        
        servidores[nome] = {}
        servidores[nome]['ip'] = ip
        servidores[nome]['status'] = stat
        servidores[nome]['description'] = description

    return servidores






        




import ftplib
from datetime import datetime

ftp = ftplib.FTP("ftp001.dc.nova")
ftp.login("svc_monitoria", "HP@2014Cnova")

f = open('D:\\SiteScope\\scripts\log\\ftp_david.log', 'a')
try:
   
    ftp.cwd('home/vendas_diarias_cbd/out')
    modifiedTime = ftp.sendcmd('MDTM ' + 'Vendas_Diarias_PF_PontoCom.ok')
    data_modificado =  datetime.strptime(modifiedTime[4:], "%Y%m%d%H%M%S").strftime("%Y-%m-%d")
    data_hoje = str(datetime.now())[:10]

    if data_hoje == data_modificado:
        print "OK"
        f.write(str(datetime.now()) + "\tOK\t" + data_modificado + "\t" + data_hoje + '\n')
    else:
        print "NOT OK"
        f.write(str(datetime.now()) + "\tNOT OK\t" + data_modificado + "\t" + data_hoje + '\n')

    f.close()
except ftplib.error_perm, resp:
    if str(resp) == "550 No files found":
        print "NOT OK"
        f.write(str(datetime.now()) + "\tNOT OK\t" + str(resp))
        f.close()
    else:
        print "NOT OK"
        f.write(str(datetime.now()) + "\tNOT OK\t" + str(resp))
        f.close()
        raise



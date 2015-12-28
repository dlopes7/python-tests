import imaplib
import random
import smtplib
import time

def checa_email_recebido(assunto):
    try:
        mail = imaplib.IMAP4_SSL('webmail2.suanova.com')
        mail.login('<usuario>', '<senha>')
        mail.select("INBOX/SDP - Monitoria")

        result, data = mail.search(None, "ALL")
         
        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string

        latest_email_id = id_list[-1] # get the latest

        for latest in latest_email_id:
            result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
            raw_email = data[0][1].replace('\n', '').replace('=', '').replace('\r', '') # here's the body, which is raw text of the whole email
            if assunto in raw_email:
                return True
            else:
                return False
    except Exception, e:
        print('RESULTADO_Falha!' + str(e) + '_FIM')
            

def envia_email_sdp(assunto):
    try:
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        email = 'servicedesk@suanova.com'
        #email = 'david.lopes@cnova.com'
        me = "ti.monitoria@cnova.com"

        msg = MIMEMultipart('alternative')

        msg['Subject'] = assunto
        msg['From'] = me
        msg['To'] = email

        s = smtplib.SMTP('mailer-corp001.dc.nova')
        s.sendmail(me, email.split(';'), msg.as_string())
        s.quit()
    except Exception, e:
        print('RESULTADO_Falha!' + str(e) + '_FIM')

numero_aleatorio = str(random.randrange(0, 10**8, 2))
texto_assunto = 'MONITORIA_RETORNO_EMAIL_SDP_' + numero_aleatorio
envia_email_sdp(texto_assunto)

minutos_a_esperar = 15
checagens = minutos_a_esperar * 60 / 10
while True:
    resultado = checa_email_recebido(texto_assunto)
    if resultado == True:
        print('RESULTADO_' + 'OK! Chamado aberto e email recebido apos ' + str(((minutos_a_esperar * 60 / 10) - checagens) * 10) + ' segundos! ID ENVIADO: ' + numero_aleatorio + '_FIM')
        break
    else:
        checagens = checagens - 1
        if checagens <= 0:
            print('RESULTADO_' + 'Falha! Chamado nao foi aberto apos ' +str(minutos_a_esperar)+ ' minutos! ID ENVIADO: ' + numero_aleatorio + '_FIM')
            break
        time.sleep(10)
    


    

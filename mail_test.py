import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'tihbaextrema@gmail.com'
sender_password = 'dyvbhqkhqguzvxmj'
recipient_email = 'emailteste@gmail.com'
subject = 'Teste Ping Monitor'
device_list = []
last_alert_time = None
email_sent = False


# Função para enviar o email
def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email enviado com sucesso!")
    except Exception as e:
        print("Ocorreu um erro ao enviar o email:", e)


# Exemplo de mensagem do email
message = "Olá,\n\nEmail de teste!!\n\n"
for device in device_list:
    message += "- " + device + "\n"

# Enviar o email se as condições forem atendidas
if last_alert_time is None or email_sent:
    send_email(subject, message)
    last_alert_time = "Defina o horário aqui"
    email_sent = True

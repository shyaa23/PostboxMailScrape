from lxml import html
import requests
import warnings
import pprint
import datetime

#Send Email Notification:
def notify(sender, password, reciever):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = reciever
    msg['Subject'] = 'Check Mail Notification'
    message = 'Check Your Postbox.'
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(sender, password)
    mailserver.sendmail(sender,reciever,msg.as_string())
    mailserver.quit()


warnings.filterwarnings("ignore")

time = datetime.datetime.now()

USERNAME = "1491"
PASSWORD = "469169"

login_url = 'https://onlinepostbox.gpo.gov.np/'
url = "https://onlinepostbox.gpo.gov.np/PBOnlineMail/ListOnlineMail"
session_requests = requests.session()

# Get login csrf token
response = session_requests.get(login_url,verify=False)
tree = html.fromstring(response.text)
csrf_token = tree.xpath("//input[@name='__RequestVerificationToken']/@value")

# Create payload
payload = {
    "username": USERNAME,
    "password": PASSWORD,
    "__RequestVerificationToken": csrf_token
}

# Perform login
result = session_requests.post(login_url, data = payload, headers = dict(referer = login_url))

#Scrape url
postbox = session_requests.get(url, headers = dict(referer = url))
tree = html.fromstring(postbox.content)

table = tree.xpath('//*[@id="body"]/div[2]/div/section/div[2]/div/table')
for elem in table:
    thead = elem.xpath('//*[@id="body"]/div[2]/div/section/div[2]/div/table/thead')
    tbody = elem.xpath('//*[@id="body"]/div[2]/div/section/div[2]/div/table/tbody')

    for title,value in zip(thead,tbody):
        thead_th = title.xpath('//*[@id="body"]/div[2]/div/section/div[2]/div/table/thead/tr/th/text()')
        thead_th = [word.strip() for word in thead_th]
        rows =title.xpath("//*[@id='body']/div[2]/div/section/div[2]/div/table/tbody/tr")
        if rows:
            for i,item in enumerate(rows):
                tbody_td = item.xpath('//*[@id="body"]/div[2]/div/section/div[2]/div/table/tbody/tr'+str([i+1])+'/td/text()')
        else:
            tbody_td = value.xpath('//*[@id="body"]/div[2]/div/section/div[2]/div/table/tbody/tr/td/text()')
            tbody_td = [word.strip() for word in tbody_td]

        if tbody_td == []:
            print("Empty Postbox........No Mail List")
            data = dict(map(lambda e: (e, ' '), thead_th))
            data['Mail Checked At'] = str(time)
            pprint.pprint(data)
            print("\n")
            notify('sender@gmail.com', 'senderpassword', 'reciever@gmail.com')

        else:
            data = dict(zip(thead_th, tbody_td))
            data['Mail Checked At'] = str(time)
            pprint.pprint(data)
            notify('sender@gmail.com', 'senderpassword', 'reciever@gmail.com')

#To automate the script everyday at 7am.
#sudo crontab -e
#0 7 * * * sudo -u <user> DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send 'Hi' 'Check your mail.'| python /usr/bin/postbox.py
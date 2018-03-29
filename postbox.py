from lxml import html
import requests
import warnings
import pprint

warnings.filterwarnings("ignore")

USERNAME = "1491"
PASSWORD = "469169"

login_url = 'https://onlinepostbox.gpo.gov.np/'
url = "https://onlinepostbox.gpo.gov.np/PBOnlineMail/ListOnlineMail"
session_requests = requests.session()

# Get login csrf token
response = session_requests.get(login_url,verify=False)
tree = html.fromstring(response.text)
csrf_token = tree.xpath("//input[@name='__RequestVerificationToken']/@value")
#print(csrf_token)

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
        #for i,item in enumerate(rows):
        #tbody_td = item.xpath('//*[@id="body"]/div[2]/div/section/div[2]/div/table/tbody/tr'+str([i+1])+'/td/text()')
        tbody_td = value.xpath('//*[@id="body"]/div[2]/div/section/div[2]/div/table/tbody/tr/td/text()')
        tbody_td = [word.strip() for word in tbody_td]

        if tbody_td == []:
            print("EMPTY POSTBOX.....NO MAIL LIST")
            print('\n')
            d = dict(map(lambda e: (e, ' '), thead_th))
            pprint.pprint(d)

        else:
            d = dict(zip(thead_th, tbody_td))
            pprint.pprint(d)
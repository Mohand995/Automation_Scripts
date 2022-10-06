import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
import datetime


now=datetime.datetime.now()  #show current email time sent
email_content=''
SERVER="smtp.gmail.com"
PORT=587
FROM="mohalim9495@gmail.com"
TO="mohalim9495@gmail.com"
PASS="xpohlqobyhtkvupo"

def extract_news(url):
    print("Extracting Hacker News Stories....")
    cnt=''
    cnt+=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response=requests.get(url)
    content=response.content
    soup=BeautifulSoup(content,'html.parser')
    for i , tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt+=((str(i+1)+' :: '+ '<a href="' + tag.a.get('href') + '">' + tag.text + '</a>' + "\n" + '<br>') if tag.text!='More' else '')
    return cnt

def Send_SMTP_Mail(SERVER,PORT,FROM,TO,PASS,email_content):
        msg=MIMEMultipart()
        msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
            now.year)
        msg['From'] = FROM
        msg['To'] = TO
        msg.attach(MIMEText(email_content, 'html'))
        print('Initiating Server...')
        server = smtplib.SMTP(SERVER, PORT)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(FROM, PASS)
        server.sendmail(FROM, TO, msg.as_string())
        print('Email Sent...')
        server.quit()


cnt=extract_news("https://news.ycombinator.com/")
email_content+=cnt
email_content+="<br>----------------------------<br>"
email_content+="<br><br> end of message"

print("Composing Email")

Send_SMTP_Mail(SERVER,PORT,FROM,TO,PASS,email_content)





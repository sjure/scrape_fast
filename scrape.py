import requests
import urllib.request
import time
import smtplib
from html.parser import HTMLParser

emails =["sjurbes@gmail.com"]
url = 'http://www.returbil.no/freecar.asp'

print("Welcome to simple webscraping by SJUR \n\n")


class Gmail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)        
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_message(self,to_email, subject, body):
        ''' This must be removed '''
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + to_email,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            to_email,
            headers + "\r\n\r\n" + body)


emails =["sjurbes@gmail.com"]
class MyHTMLParser(HTMLParser):
    def __init__(self,gm):
        HTMLParser.__init__(self)
        self.in_td= False
        self.col_count=0
        self.from_test = "test"
        self.to_test = "test"
        self.is_taken=False
        self.gm = gm
    
    def handle_data(self,data):
        if(self.in_td):
            #print(data,self.col_count)
            if self.col_count==6:
                #print("from",data)
                self.from_test = data
            elif self.col_count==8:
                #print("to",data)
                self.to_test=data
                #print(self.is_taken)

    def handle_endtag(self,tag):
        if (self.in_td):
            if tag == "tr":
                if "Oslo" in self.from_test and "Trondheim" in self.to_test and not self.is_taken:
                    for mail in emails:
                        self.gm.send_message("sjurbes@gmail.com","Returbil fra oslo til trondheim er ledig","Returbil fra oslo til trondheim er ledig")
                if "Oslo" in self.to_test and "Trondheim" in self.from_test and not self.is_taken:
                    for mail in emails:
                        self.gm.send_message("sjurbes@gmail.com","Returbil fra oslo til trondheim er ledig","Returbil fra oslo til trondheim er ledig")
                self.in_td = False
                self.col_count=0
                
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            try:
                if attrs[0][1] == "#EFEFEF" and len(attrs)==1:
                    self.in_td = True
            except:
                pass
        if self.in_td:
            if tag =="td":
                self.col_count+=1
            if tag =="i":
                self.is_taken=True

gm = Gmail('sjurpython@gmail.com', 'JegHarEnStorPikkOhyeyoloswag2')
parser = MyHTMLParser(gm)
response = requests.get(url)
parser.feed(response.text)

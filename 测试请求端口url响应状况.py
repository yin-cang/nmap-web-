import requests
import re
import pandas as pd
import my_fake_useragent
import urllib3,random
from lxml import etree
from bs4 import BeautifulSoup
import concurrent.futures,threading
import time,xlsxwriter

urllib3.disable_warnings()
ua=my_fake_useragent.UserAgent().random()
header={
    "HOST":"www.baidu.com",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent":ua,
    'Content-Type': 'application/x-www-form-urlencoded',
"Cookie":"BAIDUID=55AAE2ED3F6010B323DB6D14CABCCA47:FG=1; __yjs_duid=1_968c1abfea71a4a41678fde202026c4e1641378810850; BIDUPSID=0665E07CA15B102B7DFA388CDB5832F7; PSTM=1641378815; BD_UPN=13314752; MCITY=-%3A; sugstore=0; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; COOKIE_SESSION=5919_0_7_7_12_9_0_0_7_6_0_0_5982_0_65_0_1650097960_0_1650097895%7C9%231897126_63_1649741503%7C9; BD_HOME=1; H_PS_PSSID=35839_36177_31253_36019_34813_35910_36166_34584_36120_35979_36125_36227_26350_35868_22157_36061; BA_HECTOR=810k0ha42001218hia1h5niqd0q; delPer=0; BD_CK_SAM=1; PSINO=5; BDSVRTM=27; WWW_ST=1650183100145; rsv_jmp_slow=1650183100145; ISWR=12"
}
#hosts=[]
#ports=[]
urls=[]
http=["http://","https://"]
result=[]

start=time.time()
'''
with open("host.txt","r") as f1:
    for host in f1.readlines():
        hosts.append(host.strip())
hosts=list(set(hosts))
with open("port.txt","r") as f2:
    for port in f2.readlines():
        ports.append(port.strip())
ports=list(set(ports))
for i in hosts:
    for j in ports:
        for hp in http:
            if j.strip()=="80" or j.strip()=="443" or j=="":
                urls.append(hp+i)
            else:
                url=hp+i+":"+j
                urls.append(url.strip())
'''
def httest(a,b):
    for hp in http:
        if b.strip() == "80" or b.strip() == "443" or b == "":
            urls.append(hp + a)
        else:
            url = hp + a + ":" + b
            urls.append(url.strip())

def get_tile(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.title.text  # 提取title并打印

def Request(url):
    try:
        print(url)
        req=requests.get(url=url,headers=header,verify=False,allow_redirects=True,timeout=2)
        req.encoding="utf-8"
        code=req.status_code
        if code!=0:
            #print(url+":"+str(code))
            html=req.text
            try:
                title=get_tile(html)
            except:
                title="可疑"
            #print(title)
            result1=url+"-"+str(title)+"-"+str(code)
            print(result1)
            result.append(result1)
    except Exception:
        pass
'''
for i in urls:
    Request(i)
'''

df = pd.read_excel('nmap资产.xlsx',sheet_name='Results',usecols=[1,2])
data=df.values
#print("获取到所有的值:\n{}".format(data))
for i in data:
    a=i[0]
    b=i[1]
    httest(str(a),str(b))
urls=list(set(urls))
#print(urls)




try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        result1 = {executor.submit(Request, i): i for i in urls}
        for future in concurrent.futures.as_completed(result, timeout=3):
            future.result()
            #print(future.result())
except (EOFError, concurrent.futures._base.TimeoutError):
    pass


"""
for i in result:
    jihe=str(i).split("-")
    print(i)
"""

jihe_header=["Url","Title","Status_Code"]
count=1
workbook=xlsxwriter.Workbook("url资产.xlsx")
formats = {"fmt_bold": workbook.add_format({"bold": True}),
               "fmt_conf": workbook.add_format()}
sheet=workbook.add_worksheet("host")
for i in result:
    for a,b in enumerate(jihe_header):
        sheet.write(0,a,b,formats["fmt_bold"])
        jihe=str(i).split("-")
        for c,d in enumerate(jihe):
            sheet.write(count,c,d)
    count+=1

workbook.close()

stop=time.time()
ctime=stop-start
print(ctime)

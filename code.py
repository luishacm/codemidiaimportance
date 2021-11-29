#In this file, there are three separated codes, but they all follow the same logic.
##For the code to work you need to create a folder for each code and inside this folder another two folders 
## one called "arquivos" where you will put a TXT called "linkdasimagens" and another folder named "Imagens" 
## where you will set several folders according to the years of your research
## Example, if you are researching between 2013 and 2015, you will create three folders inside "Imagens" called "2013", "2014" and "2015".
### These codes were made to a specific website if this website changes the code will stop working, and it will need to be adapted
### To use this, the user needs to have a minimum knowledge of programming.


#Code that works for the website https://acervo.estadao.com.br/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import re
import requests

#Options for the user

login = ("yourlogin@gmail.com")
password = ("your@password")
keywords = ["test", "one", "two", "three", "test"]
startyear = 2003
endyear = 2014

#General Options

options = FirefoxOptions()
#options.add_argument("--headless")   #If you delete the initial hashtag you can use this without an interface, it's lighter for your compuuter
options.set_preference("general.useragent.override", "Mozilla/5.0 (X11;     Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0   Safari/537.36")
driver = webdriver.Firefox(options=options)

#making the login on the Estadão website so we can have the images in high quality
    
def loginweb():
    driver.get("https://acesso.estadao.com.br/login")
    driver.find_element_by_xpath('//input[@name="email_login"]').send_keys(login)
    driver.find_element_by_xpath('//input[@name="senha"]').send_keys(password)
    driver.find_element_by_xpath('//input[@value="Entrar"]').click()
    print("Fez login!")
 
#Opening the web navigator, opening the document where the links of the images will be stored
# and creating a function so it can be activated with the right variables

def determinesearch(ano, palavrachave):
    if ano in list(range(2010,2020)):
        decada = ("10")
    if ano in list(range(2000,2010)):
        decada = ("00")
    global searchlink
    searchlink = ("https://acervo.estadao.com.br/procura/#!/{}/Acervo//spo/1/20{}/{}//Primeira".format(palavrachave, decada, ano))
    

#Finding out how many pages there is in the website search page
    
def pagnum ():
    global page_number
    if driver.find_elements_by_class_name("page-ultima-qtd"):
        try:
            page_number = driver.find_element_by_class_name("page-ultima-qtd").text
        except NoSuchElementException:
            pass
    else:
        page_number = 1

#If the website shows an ads up it will automatically close it

def closeads():
    try:
        driver.find_element_by_xpath("//label[contains(text(),'Veja o jornal do dia:')]").click
        time.sleep(10)
        print("Pop-up foi fechado")
    except NoSuchElementException:
        print("Não havia pop-up")
        pass

#This will store all the selected links of the images from the website in a TXT so later we can download the images.

def findlinks(x):
    
    for i in range(int(page_number)):
        try:
            links = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.LINK_TEXT, "LEIA ESTA EDIÇÃO")))
        except TimeoutException:
            break
        try:
            references = [link.get_attribute("href") for link in links]    
            time.sleep(1)              
            txt.write("\n".join(references))
            txt.write("\n")                   
        except NoSuchElementException:
            pass
        print(references)
        try:
            driver.find_element_by_class_name("seta-right").click()
        except NoSuchElementException:
            pass
    txt.close()

#This is the second block of the code: after we got all the links, we will download them now.
##Preparing the variables
    
def downloadimages():
    
    time.sleep(1) 
    lines = [line.rstrip('\n') for line in open("arquivos/linkdasimagens.txt")]
    x = 0
    with open('arquivos/linkdasimagens.txt') as f:
        line_count = 0
        for line in f:
            line_count += 1

    ##It will get the list of links we made and open in the navigator one by one and download each image.
    ##Each downloaded image will be placed in a path of the computer to be determined by the user.
    ##We inserted the Google website to loop too because the Javascript of the site stops the script, this fix the problem partially. 

    for i in range(int(line_count)):
        try:
            time.sleep(3)
            y = lines[x]
            driver.get('http://www.google.com')
            driver.get(y)        
            img = driver.find_element_by_xpath("//img[@class='BRnoselect']")
            src = img.get_attribute('src')
            srcname = driver.find_element_by_xpath("//h1[@class='edicao-data']").text
            subname = re.sub('[^A-Za-z0-9]+', '', srcname)
            dia = subname[:31]
            dia = dia[-2:]
            mes = subname[:36]
            mes = mes[-3:]
            ano = re.sub('[^0-9]+', '', srcname)
            ano = ano[:6]
            ano = ano[-4:]
            nome = ("CapaEstadao" + ano + mes + dia)    
            with open(("Imagens/{}/{}.jpg".format(ano, nome)), "wb") as f:
                f.write(requests.get(src).content)
            x += 1
            print(x)            
        except NoSuchElementException:
            pass

#Running the code according to the variables we wanted in the begining.

txt = open("arquivos/linkdasimagens.txt","a")
txt.close()

if startyear == endyear:
    cicle = 1
else:
    endyear += 1
    cicle = (endyear - startyear)

startyear -= 1
google = ("https://www.google.com")

loginweb()
print("Adquirindo os primeiros links para download")
for y in range(cicle):  #Finding out the links
    startyear += 1
    z = 0
    for x in range(len(keywords)):
        whichword = keywords[z]
        z += 1
        determinesearch(startyear, whichword)
        driver.get(google)
        driver.get(searchlink)
        pagnum()
        txt = open("arquivos/linkdasimagens.txt","a")
        findlinks(1)
        print("Links do ano de {} com a palavra chave '{}' foram adquiridos".format(startyear, whichword))

downloadimages() #downloading the images
print("Processo de download finalizado")





#The following code works for the website https://acervo.oglobo.globo.com

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import requests
import os
import gc

#Variables you need to fill

startyear = 2010          #the year the search will start
endyear = 2014            #the year the search will end
login = ("yourlogin@gmail.com")
senha = ("your@password")
keywords = ["alo", "não", "sim"] #put the keywords you wanna find, always use single words as "hello", but don't use "good morning", the space will make the code to stop working.


#General Options

options = FirefoxOptions()
#options.add_argument("--headless")      #Delete the Hashtag if you don't want the interface of the browser to show up
options.set_preference("general.useragent.override", "Mozilla/5.0 (X11;     Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0   Safari/537.36")
driver = webdriver.Firefox(options=options)

# Login in the website to get high quality images
def loginweb():     
    driver.get("https://login.globo.com/login/1")
    driver.find_element_by_xpath("//input[@id='login']").send_keys(login)
    driver.find_element_by_xpath("//input[@id='password']").send_keys(senha)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    print("Fez login!")

#Finding out how many pages there is, so we can loop this many times.

def findpagnum ():
    global pgnum
    pgnum = driver.find_element_by_class_name("resultados-small").text
    pgnum = pgnum[:20]
    pgnum = re.sub('[^0-9]','', pgnum)
    pgnum = (round(int(pgnum)/20) + 1)

#Algorithym made to improve the speed of the code downloading only once what we want (that's a problem with the website that shows several times the same item)

def checkifexist():
    global my_list
    global q
    try:
        item = driver.find_elements_by_xpath('//figcaption')[q].text
    except IndexError:
        return
    if item in my_list:
        q += 1
    else:
        my_list += [item]

#downloading the images we need      

def downimage(x):    
    driver.implicitly_wait(5)
    driver.find_elements_by_class_name("hoverLupa")[x].click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "ampliar")))
    driver.find_element_by_class_name("ampliar").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//img[@id='mapGrande']")))    
    img = driver.find_element_by_xpath("//img[@id='mapGrande']")
    src = img.get_attribute('src')    
    srcname = driver.find_element_by_xpath("//div[@class='wrapper']//p[@class='title']").text
    subname = re.sub('[^A-Za-z0-9]+', '', srcname)
    dia = subname[:2]
    mes = subname[:7]
    mes = mes[-3:]
    ano = subname[-52:]
    ano = ano[:4]
    nome = ("CapaGlobo" + ano + mes + dia)   
    with open(("Imagens/{}/{}.jpg".format(ano, nome)), "wb") as f:
        f.write(requests.get(src).content)
    driver.refresh()    

#gets the link to download the images
    
def determinesearch(ano):
    if ano in list(range(2010,2019)):
        decada = ("2010")
    if ano in list(range(2000,2009)):
        decada = ("2000")
    if ano in list(range(1990,1999)):
        decada = ("1990")
    if ano in list(range(1980,1989)):
        decada = ("1980")

    if len(keywords) == 1:
        words = keywords[0]
    if len(keywords) > 1:
        words = []
        for x in range(len(keywords)):
            words.extend(keywords[x]+"+")     
    words =''.join(words)

    global searchlink
    searchlink = ("https://acervo.oglobo.globo.com/busca/?tipoConteudo=pagina&pagina={}&ordenacaoData=relevancia&allwords=&anyword={}&noword=&exactword=&decadaSelecionada={}&anoSelecionado={}&primeirapagina=on".format(pg, words, decada, ano))


# Running all the code above in the right order and loop

pg = 1
y = pg - 1
x = 0
if startyear == endyear:
    cicle = 1
else:
    endyear += 1
    cicle = (endyear - startyear) 
startyear -= 1
loginweb()

for o in range(cicle):
    startyear += 1
    determinesearch(startyear)
    driver.get(searchlink)
    findpagnum()
    print("Baixando as capas de {}".format(startyear))
    my_list = []
    for p in range(pgnum):
        x = 0
        y += 1
        i = y - 1
        searchlink = searchlink.replace('pagina={}'.format(i), 'pagina={}'.format(y))
        driver.get(searchlink)
        print("Baixando a página {}".format(p + 1))
        for i in range (20):
            q = i
            checkifexist()
            if q > i:
                continue
            else:
                pass
            downimage(i)




The following code works for the website www.acervo.folha.com.br

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import requests
import os
import gc

#General Options

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11;     Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0   Safari/537.36")
driver = webdriver.Firefox(profile)

#Open the navigator and the TXT
#In driver.get you need to put the link of your search, this is an example where you use the search box of the website selecting years and keywords and then copy the link that the website generates

txt = open("arquivos/hrefsimg.txt","w")
driver.get("https://acervo.folha.com.br/busca.do?sort=desc&page=1&decadeStatus=&jornais=1&chapter=8&keyword=qualquer%3Aministro%3B+minist%C3%A9rio%3B+ministra%3B+itamaraty%3B+minc%3B+mec&periododesc=01%2F06%2F2009+-+10%2F08%2F2010&por=Por+Per%C3%ADodo&startDate=01%2F06%2F2009&endDate=10%2F08%2F2010&days=&month=&year=&jornais=1")
x = 0

#Finding out how many pages there is to loop

pgnum = driver.find_element_by_class_name("results-tool-bar").text
pgnum = pgnum[:20]
pgnum = re.sub('[^0-9]','', pgnum)
pgnum = (round(int(pgnum)/20) + 2)

#Finding out the links

for i in range(pgnum):
    try:
        all_hrefs=[el.get_attribute("href") for el in driver.find_elements_by_partial_link_text("1 -")]
        if all_hrefs:
            txt.write("\n".join(all_hrefs))
            txt.write("\n")
        else:
            pass                
    except NoSuchElementException:
        pass
    
    try:
        all_hrefs2=[el.get_attribute("href") for el in driver.find_elements_by_partial_link_text("A1E -")]
        if all_hrefs2:
            txt.write("\n".join(all_hrefs2))
            txt.write("\n")
    except NoSuchElementException:
        pass

    if x in list(range(20, (60)*20, 20)):
        txt.close()
        txt = open("arquivos/hrefsimg.txt","a")
        gc.collect()
        
    try:
        y = x + 2
        if pgnum > y:
            driver.find_element_by_class_name("next").click()
        else:
            pass
    except NoSuchElementException:
        pass
    
    x += 1
    print(x)

txt.close()

#Preparing the variablees

time.sleep(1) 
lines = [line.rstrip('\n') for line in open("arquivos/hrefsimg.txt")]
x = 0

#Loop to download all images

while True:
    
    y = lines[x]
    driver.get(y)
    
    try:    
        img = driver.find_element_by_xpath("//img[@data-label='1']")
    except NoSuchElementException:
        x += 1
        continue
    
    try:
        src = img.get_attribute('data-zoom')
        findingname = driver.find_element_by_xpath("//input[@id='filter-by-date']")
        srcname = findingname.get_attribute('value')
    except NoSuchElementException:
        pass
    
    u = re.sub('[^A-Za-z0-9]+', '', srcname)
    year = u[-4:]
    month = u[-7:]
    month = month[:3]
    day = u[:2]
    name = ("CapaFolha" + year + month + day)
    
    with open(("Imagens/{}/{}.jpg".format(year, name)), "wb") as f:
        f.write(requests.get(src).content)
        
    x += 1
    print(x)

print("Finalizado")   

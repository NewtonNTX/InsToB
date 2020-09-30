from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from threading import Thread
import PySimpleGUI as sg
import PySimpleGUI
import time
import json
import os
import re

diretory = os.path.dirname(os.path.abspath(__file__))

UpdateNote = """+ Funções

+ Correções/Bugs

+ Versão => 1.0.0"""

DevNote = """Bem-Vindo a primeira versão de InsToB.
Este App foi feito com o objetivo para facilitar o 
desenvolvimento de estratégias e pesquisa de público alvo 
para fins de marketing; acessando sua propria lista de 
seguidores e perfis que está seguindo.
    
Aviso: Não me responsibiliso por qualquer uso inlicito
            deste aplicativo.
       
       Use de forma conciente ;D"""

class InstagramBot:
    def __init__(self):
        self.Thread = False
        self.WhatReturn = ''
        self.Return = ''
        self.Msg = ''

    def re__init__(self):
        self.Thread = False

    def openwindow(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.privatebrowsing.autostart", True)
        options = Options()
        #options.add_argument("--headless")   # -> Oculta o navegador
        #options.set_headless = True
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=diretory + r'/geckodriver')
        self.driver.get('https://www.instagram.com/?hl=pt-br')
        self.Thread = True

    def reloadWindow(self):
        self.driver.get('https://www.instagram.com/?hl=pt-br')

    def login(self, user, password):
        self.user = user.lower()
        self.password = password
        time.sleep(1.5)
        user_element = self.driver.find_element(By.NAME, "username")
        user_element.clear()
        user_element.send_keys(self.user)
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(self.password + Keys.ENTER)
        time.sleep(2)
        test_login = self.driver.page_source[:]
        self.Msg = re.findall(r'<p[\s\S]+?id=\"slfErrorAlert\"[\s\S]+?>([\s\S]+?)</p>', test_login)
        self.Thread = True

    def colect_followers(self):
        self.driver.get('https://www.instagram.com/{}/'.format(self.user))
        time.sleep(2)
        number_followers = self.driver.page_source[:]
        number_followers = number_followers[int(number_followers.find('<div class')):]
        number_followers = number_followers[int(number_followers.find('href="/{}/followers/"'.format(self.user))):]
        number_followers = number_followers[:int(number_followers.find('</span>'))]
        number_followers = int((re.findall(r'title=[\"\'](\d+)[\"\']', number_followers))[0])
        time.sleep(2)
        click_follow = self.driver.find_element(By.TAG_NAME, "body")
        for count in range(0, 4):
            click_follow.send_keys(Keys.TAB)
        click_follow.send_keys(Keys.ENTER)
        time.sleep(2)
        scroll_followers = self.driver.page_source[:]
        scroll_followers = scroll_followers[int(scroll_followers.find('<h1')) + 3:]
        scroll_followers = scroll_followers[int(scroll_followers.find('<h1')):]
        scroll_followers = scroll_followers[int(scroll_followers.find('<svg')):]
        scroll_followers = scroll_followers[int(scroll_followers.find('<div')):]
        scroll_followers = scroll_followers[:int(scroll_followers.find('>'))]
        scroll_followers = (re.findall(r'class=[\'\"]([\s\S]+)[\'\"]', scroll_followers))[0]
        count_break = 0
        while True:
            htmlpage = self.driver.page_source[:]
            htmlpage = htmlpage[int(htmlpage.find('<div class="{}"'.format(scroll_followers))):]
            if int(htmlpage.find('<h4')):
                htmlpage = htmlpage[:int(htmlpage.find('<h4'))]
            else:
                htmlpage = htmlpage[:int(htmlpage.find('</body>'))]
            self.driver.execute_script('window.document.querySelector("div.{}").scrollTo(0, document.querySelector("div.{}").scrollHeight - 50)'.format(scroll_followers, scroll_followers))
            htmllist = re.findall(r'<span [\s\S]*?<a [\s\S]*? title=[\"\'](.{,30})[\"\'] href=[\"\']/\1/[\"\'] [\s\S]*?>',htmlpage, flags=re.I)
            if len(htmllist) >= number_followers or count_break >= 2.5 * number_followers:
                time.sleep(3)
                self.Return = htmllist[:]
                self.WhatReturn = "colect_followers"
                return 
            else:
                count_break += 1

    def colect_following(self):
        self.driver.get('https://www.instagram.com/{}/'.format(self.user))
        time.sleep(2)
        number_following = self.driver.page_source[:]
        number_following = number_following[int(number_following.find('<div class')):]
        number_following = number_following[int(number_following.find('href="/{}/following/"'.format(self.user))):]
        number_following = number_following[:int(number_following.find('</a>'))]
        number_following = number_following[int(number_following.find('<span')):]
        number_following = number_following[int(number_following.find('>')):]
        number_following = int((re.findall(r'>(\d+)</span>', number_following))[0])
        time.sleep(2) 
        click_follow = self.driver.find_element(By.TAG_NAME, "body")
        for count in range(0, 5):
            click_follow.send_keys(Keys.TAB)
        click_follow.send_keys(Keys.ENTER)
        time.sleep(2)
        scroll_following = self.driver.page_source[:]
        scroll_following = scroll_following[int(scroll_following.find('<h1')) + 3:]
        scroll_following = scroll_following[int(scroll_following.find('<h1')):]
        scroll_following = scroll_following[int(scroll_following.find('<svg')):]
        scroll_following = scroll_following[int(scroll_following.find('<div')):]
        scroll_following = scroll_following[:int(scroll_following.find('>'))]
        scroll_following = (re.findall(r'class=[\'\"]([\s\S]+)[\'\"]', scroll_following))[0]
        count_break = 0
        while True:
            htmlpage = self.driver.page_source[:]
            htmlpage = htmlpage[int(htmlpage.find('<div class="{}"'.format(scroll_following))):]
            if int(htmlpage.find('<h4')):
                htmlpage = htmlpage[:int(htmlpage.find('<h4'))]
            else:
                htmlpage = htmlpage[:int(htmlpage.find('</body>'))]
            self.driver.execute_script('window.document.querySelector("div.{}").scrollTo(0, document.querySelector("div.{}").scrollHeight - 50)'.format(scroll_following, scroll_following))
            htmllist = re.findall(r'<span [\s\S]*?<a [\s\S]*? title=[\"\'](.{,30})[\"\'] href=[\"\']/\1/[\"\'] [\s\S]*?>',htmlpage, flags=re.I)
            if len(htmllist) >= number_following or count_break >= 2.5 * number_following:
                time.sleep(3)
                return htmllist
            else:
                count_break += 1

    def colect_hastags(self):
        self.driver.get('https://www.instagram.com/{}/'.format(self.user))
        time.sleep(3) 
        click_follow = self.driver.find_element(By.TAG_NAME, "body")
        for count in range(0, 5):
            click_follow.send_keys(Keys.TAB)
        click_follow.send_keys(Keys.ENTER)
        time.sleep(3)
        for count in range(0, 3):
            click_follow.send_keys(Keys.TAB)
        click_follow.send_keys(Keys.ENTER)
        time.sleep(2)
        scroll_hashtags = self.driver.page_source[:]
        scroll_hashtags = scroll_hashtags[int(scroll_hashtags.find('<h1')) + 3:]
        scroll_hashtags = scroll_hashtags[int(scroll_hashtags.find('<h1')):]
        scroll_hashtags = scroll_hashtags[int(scroll_hashtags.find('<svg')):]
        scroll_hashtags = scroll_hashtags[int(scroll_hashtags.find('<div')):]
        scroll_hashtags = scroll_hashtags[:int(scroll_hashtags.find('>'))]
        scroll_hashtags = (re.findall(r'class=[\'\"]([\s\S]+)[\'\"]', scroll_hashtags))[0]
        count_break = 0
        testlist = []
        while True:
            htmlpage = self.driver.page_source[:]
            htmlpage = htmlpage[int(htmlpage.find('<div class="{}"'.format(scroll_hashtags))):]
            htmlpage = htmlpage[:int(htmlpage.find('</body>'))]
            try:
                self.driver.execute_script('window.document.querySelector("div.{}").scrollTo(0, document.querySelector("div.{}").scrollHeight - 50)'.format(scroll_hashtags, scroll_hashtags))
            finally:
                htmllist = re.findall(r'href=[\"\']/explore/tags/([\s\S]{,150})?/[\"\']',htmlpage, flags=re.I)
                if len(testlist) == len(htmllist):
                    finallist = []
                    for count in range(0, len(htmllist), 2):
                        finallist.append(htmllist[count])
                    time.sleep(3)
                    return finallist
                else:
                    time.sleep(0.5)
                    testlist = htmllist

    def activity_Likes(self):
        stop = 0
        self.driver.get('https://www.instagram.com/{}/'.format(self.user))
        time.sleep(2)
        number_Photos = self.driver.page_source[:]
        number_Photos = number_Photos[int(number_Photos.find('<ul')):]
        number_Photos = number_Photos[:int(number_Photos.find('</li>'))]
        number_Photos = int(re.findall(r'>([\d]+)</span>?', number_Photos, flags=re.I)[0])
        url_Photos = []
        list_test = []
        result = {}
        while True:    
            links_photos = self.driver.page_source[:]
            links_photos = links_photos[int(links_photos.find('<body class=""')):int(links_photos.find("</main>"))]
            colect_links_photos = re.findall(r'<a href=\"/p/([\s\S]{,15})/\" ', links_photos, flags=re.I)
            if number_Photos <= len(url_Photos):
                for add_likes in url_Photos:
                    self.driver.get("https://www.instagram.com/p/" + add_likes + "/")
                    time.sleep(2)
                    list_likes = self.driver.page_source[:]
                    list_likes = list_likes[int(list_likes.find('<body ')):]
                    list_likes = list_likes[int(list_likes.find('<header ')):int(list_likes.find('</footer>'))]
                    list_likes = list_likes[int(list_likes.find('<section ')) + 9:]
                    list_likes = list_likes[int(list_likes.find('<section ')):int(list_likes.find('<ul '))]
                    try:
                        list_likes_0 = list_likes[int(list_likes.find('<img ')):]
                        list_likes_0 = re.findall(r'<button class=\"([\s\S]+?)\"[\s\S]+?</button>', list_likes_0, flags=re.I)[0].split()
                        list_likes_0 = self.driver.find_elements(By.CSS_SELECTOR, "button." + list_likes_0[0])
                        list_likes_0[1].click()
                        time.sleep(1)
                        click_scroll_likes = self.driver.find_element(By.TAG_NAME, "body")
                        for count in range(0, 2):
                                click_scroll_likes.send_keys(Keys.TAB)
                        result.update({add_likes:[]})
                        while True:
                            time.sleep(2)
                            colect_likes = self.driver.page_source[:]
                            colect_likes = colect_likes[int(colect_likes.find('</footer>')):]
                            colect_likes = colect_likes[int(colect_likes.find('<div class')):]
                            colect_likes = colect_likes[int(colect_likes.find('<svg')):]
                            colect_likes = colect_likes[int(colect_likes.find('</div></div></div>')):]
                            colect_likes = re.findall(r'href=\"/([\s\S]+?)/\"', colect_likes, flags=re.I)
                            print(colect_likes)
                            for colect_like in colect_likes:
                                if 1 > result[add_likes].count(colect_like):
                                    result[add_likes].append(colect_like)
                            if colect_likes != list_test:
                                list_test = colect_likes
                                for count in range(0, 10):
                                    click_scroll_likes.send_keys(Keys.ARROW_DOWN)
                            else:
                                list_test = []
                                break
                    except:
                        try:
                            print()
                        except:
                            result.update({add_likes:None})   
                    time.sleep(1)
                return result
            else:
                for links in colect_links_photos:
                    if 1 > url_Photos.count(links):
                        url_Photos.append(links)
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)

    def check_Results(self, colect_followers, colect_following, activity_Likes): # Construir
        '''try:
                    with open("./Code/Projetos/Bot Insta/{}.json".format(self.user), "r") as outfile:
                        save = json.load(outfile)
                        for followColect in htmllist:
                            for count, followCheck in enumerate(save["followers"]):
                                if followCheck == followColect:
                                    break
                                elif count + 1 == len(save["followers"]):
                                    print("Seguidor Novo: " + followColect)
                        for followCheck in save["followers"]:
                            for count, followColect in enumerate(htmllist):
                                if followCheck == followColect:
                                    break
                                elif count + 1 == len(htmllist):
                                    print("Parou de Seguir Você: " + followCheck)
                        outfile.write(json.dumps({"followers":htmllist}, indent=4))
                except:
                    with open("./Code/Projetos/Bot Insta/{}.json".format(self.user), "w") as outfile:
                        outfile.write(json.dumps({"followers":htmllist}, indent=4))
                            break
                try:
                    with open("./Code/Projetos/Bot Insta/{}.json".format(self.user), "r") as outfile:
                        save = json.load(outfile)
                        for followColect in htmllist:
                            for count, followCheck in enumerate(save["followers"]):
                                if followCheck == followColect:
                                    break
                                elif count + 1 == len(save["followers"]):
                                    print("Seguidor Novo: " + followColect)
                        for followCheck in save["followers"]:
                            for count, followColect in enumerate(htmllist):
                                if followCheck == followColect:
                                    break
                                elif count + 1 == len(htmllist):
                                    print("Parou de Seguir Você: " + followCheck) 
                        outfile.write(json.dumps({"followers":htmllist}, indent=4))
                    except:
                        with open("./Code/Projetos/Bot Insta/{}.json".format(self.user), "w") as outfile:
                            outfile.write(json.dumps({"followers":htmllist}, indent=4))     
                    break
                else:
                    count_break += 1'''

    def save_Results(self, colect_followers, colect_following, activity_Likes):  # Construir
        print()
        
        
        
        '''self.driver.get('https://www.instagram.com/accounts/activity/')
        time.sleep(2)
        list_activity = self.driver.page_source[int(self.driver.page_source.find('<main')):int(self.driver.page_source.find('</main>'))]
        for divsCount in range(0, 4):
            list_activity = list_activity[int(list_activity.find('<div')) + 4:]
        list_activity = list_activity[int(list_activity.find('<div')):]
        class_list = (re.findall(r'<div class=[\'\"]([\s\S]*?)[\'\"] role=[\'\"]button[\'\"] ' , list_activity, flags=re.I))[0]
        list_activity = list_activity[:int(list_activity.find('</main>'))]
        notification = (self.driver.find_elements(By.CLASS_NAME, (class_list.split())[0]))
        #for count, noti in enumerate(notification):
            #likes_selector = noti.find_elements(By.TAG_NAME, 'div')
            #for likes in likes_selector:
                #print(likes)'''


        
    
        #for (divs of document.querySelectorAll('div')) {
        #    if (Number(divs.querySelectorAll('div').length) == 3) { 
        #        var div = divs.parentNode
        #        console.log(div.querySelector('a').href)
        #        console.log(div.querySelectorAll('div')[4].querySelector('a').href)
        #    }
        #}

        #div.PUHRj:nth-child(1)


        #print(Bonifo.colect_followers())
        #print(Bonifo.colect_following())
        #print(Bonifo.colect_hastags())
        #Bonifo.activity_Likes()



def Login(NameWindow):
    sg.theme('Reddit')
    layout = [
        [sg.Text(' '*80)],
        [sg.Text('Usuário:'), sg.Input(key='usuario')],
        [sg.Text('Senha:  '), sg.Input(key='senha', password_char='*')],
        [sg.Text(' '*80, key='result[0]', text_color='red', justification='c')],
        [sg.Text(' '*80, key='result[1]', text_color='red', justification='c' ,visible=False)],
        [sg.Text(' '*80, key='result[2]', text_color='red', justification='c' ,visible=False)],
        [sg.Text(' '*30), sg.Checkbox('Salvar o Login?', key='savelogin')],
        [sg.Text(' '*35), sg.Button('Entrar', focus=True)]
    ]
    return sg.Window(NameWindow, layout)

def ResultLogin(Msg):
    if len(Msg) <= 60 :
        return [Msg]
    elif 60 < len(Msg) <= 120:
        Msg = Msg.split()
        line1 = ""; line2 = ""
        for count, word in enumerate(Msg):
            line1 += word + " "
            if 60 < len(line1):
                line1 = line1[:line1.rfind(Msg[count]) - 1]
                break
        for count in range(count, len(Msg)):
            line2 += Msg[count] + " "
            if 60 < len(line2):
                line2 = line2[:line2.rfind(Msg[count]) - 1]
                break
        return [line1, line2]
    else:
        Msg = Msg.split()
        line1 = ""; line2 = ""; line3 = ""
        for count, word in enumerate(Msg):
            line1 += word + " "
            if 60 < len(line1):
                line1 = line1[:line1.rfind(Msg[count]) - 1]
                break
        for count in range(count, len(Msg)):
            line2 += Msg[count] + " "
            if 60 < len(line2):
                line2 = line2[:line2.rfind(Msg[count]) - 1]
                break
        for count in range(count, len(Msg)):
            line3 += Msg[count] + " "
            if 60 < len(line3):
                line3 = line3[:line3.rfind(Msg[count]) - 1]
                break
        return [line1, line2, line3]

def SaveLogin(Bool, tuple_login=tuple()):
    if Bool:
        print()# Salvando Ultimo login válido
        #print(tuple_login)

def Home(NameWindow):
    sg.theme('Reddit')
    titleconfig = {"font":("Helvetica", 16), "justification":'center', "size":(75, 1)}
    textbox = {"size":(100, 30), "background_color":'#d3d3d3', "auto_size_text":20, 
                "border_width":15, "font":("Helvetica", 12)}
        # Linha do Text Box 105 Letras A
    layout_Updates = [
        [sg.Text('Atualizações',**titleconfig)],
        [sg.Text(UpdateNote, key='UpdateNote',**textbox)]]
    layout_DevNotes = [
        [sg.Text('DevNotes',**titleconfig)],
        [sg.Text(DevNote, key='DevNote',**textbox)]]
    layout_Home = [
        [sg.TabGroup([[
            sg.Tab('Atualizações', layout_Updates),
            sg.Tab('DevNotes', layout_DevNotes)
        ]])]]


    output_box = {"size":(40, 30)}
    output_boxActvity = {}
    layout_followers = [
        [sg.Text('Seguidores',**titleconfig)],
        [sg.Text('Ultimo Scan:'),sg.Text(' '* 52),sg.Text('Resultado:'),sg.Text(' '* 55),sg.Text('Novo Scan:')],
        [sg.Output(**output_box),sg.Output(**output_box, pad=((11,11),(0,0))),sg.Output(**output_box,key="Followers_new")],
        [sg.Text(size=(1, 5), pad=((0,0),(0,18)))]
        ]
    layout_following = [
        [sg.Text('Perfis Seguidos',**titleconfig)],
        [sg.Text('Ultimo Scan:'),sg.Text(' '* 52),sg.Text('Resultado:'),sg.Text(' '* 55),sg.Text('Novo Scan:')],
        [sg.Output(**output_box),sg.Output(**output_box, pad=((11,11),(0,0))),sg.Output(**output_box,key="Following_new")],
        [sg.Text(size=(1, 5), pad=((0,0),(0,18)))]
        ]
    layout_activity = [
        [sg.Text('Atividades',**titleconfig)],
        [sg.Text('Notificões'),sg.Text(' ' * 56),sg.Text('Likes Removido das Fotos:')],
        [sg.Output(**output_box),sg.Output(**output_box)],
        [sg.Text(size=(1, 5), pad=((0,0),(0,18)))]
        ]
    layout_MyInsta = [
        [sg.TabGroup([[
            sg.Tab('Seguidores', layout_followers),
            sg.Tab('Perfis Seguidos', layout_following),
            sg.Tab('Atividades', layout_activity)
        ]])]
    ]

    layout_target = [
        [sg.Text('Alvo',**titleconfig)]
    ]
    layout_followersTarget = [
        [sg.Text('Seguidores(Alvo)',**titleconfig)]
    ]
    layout_followingTarget = [
        [sg.Text('Perfis Seguidos(Alvo)',**titleconfig)]
    ]
    layout_activityTarget = [
        [sg.Text('Atividades(Alvo)',**titleconfig)]
    ]
    layout_InsTarget = [
        [sg.TabGroup([[
            sg.Tab('Alvo', layout_target),
            sg.Tab('Seguidores(Alvo)', layout_followersTarget),
            sg.Tab('Perfis Seguidos(Alvo)', layout_followingTarget),
            sg.Tab('Atividades(Alvo)', layout_activityTarget)
        ]])]
    ]

    layout_Exit = [
        [sg.Button('Sair', key='Exit')]
    ]
    
    tab_config = {"element_justification":"center"}
    listmenu = [
        [
            sg.Tab('Início', layout_Home,**tab_config),
            sg.Tab('Seu Instagram', layout_MyInsta,**tab_config),
            sg.Tab('InsTarget', layout_InsTarget,**tab_config),
            sg.Tab('Sair', layout_Exit,**tab_config)
            ]
        ]

    layout = [[sg.TabGroup(listmenu)]]
    return sg.Window(NameWindow, layout)


Bonifo = InstagramBot();
Thread(target=Bonifo.openwindow).start()
windowBonifo = Login('BoT Instagram')
login = False
while True:
    if Bonifo.Thread:
        sg.popup_animated(image_source=None);
        events, value = windowBonifo.Read(timeout=1)
        if events == 'Entrar':
            if 0 < len(value['usuario']) < 31 and 5 < len(value['senha']):
                Bonifo.re__init__()
                Thread(target=Bonifo.login, args=(value['usuario'], value['senha'],)).start()
                windowBonifo.close()
                while not Bonifo.Thread:
                    sg.popup_animated(image_source=diretory + '/loading.gif')
                    time.sleep(0.1)
                sg.popup_animated(image_source=None)
                if 0 < len(Bonifo.Msg):
                    Thread(target=Bonifo.reloadWindow).start()
                    windowBonifo = Login('BoT Instagram');time.sleep(1); 
                    windowBonifo.Read(timeout=0.1)
                    result_login = ResultLogin(Bonifo.Msg[0])
                    for count in range(len(result_login)):
                        windowBonifo['result['+ str(count) +']'].Update(result_login[count], visible=True)
                else:
                    SaveLogin(value['savelogin'], (value['usuario'], value['senha']))
                    time.sleep(1);
                    # Criar uma novo open pra plataforma
                    del windowBonifo; login = True
                    windowBonifo = Home('BoT Instagram')
                    break
                    #time.sleep(1);Thread(target=Bonifo.colect_followers);Bonifo.re__init__();
            else:
                windowBonifo['result[0]'].Update("Caracteres Insuficientes.")
        if events == sg.WINDOW_CLOSED or events == 'Exit':
            break
    else:
        sg.popup_animated(image_source=diretory + '/loading.gif')
        time.sleep(0.1)
        

if login:
    while True:
        events, value = windowBonifo.Read(timeout=1)
        print(events)
        if events == sg.WINDOW_CLOSED or events == 'Exit':
            break


sg.popup_animated(image_source=None)
windowBonifo.close()
Bonifo.driver.close()

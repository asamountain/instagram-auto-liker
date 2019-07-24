    # -*- coding: utf-8 -*-

# Never maintain 1 more chrome when you implement this
# Replaces 28-30 lines ( id, passd, hashtag )
# 2 options : 
#    1) homefeed liking
#    2) tag feed liking
# need to type 't' for tag likin

# 2019-04-19 sound effect added : Mario-coin-sound
# 2019-04-20 img alt log appear on server side


import time
import pyglet as pg
import selenium
import sys
import random
import datetime

from tinydb import TinyDB, Query
from tinydb import where

from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException , NoSuchElementException

# for checking up the error
from traceback import print_exc

# waiting function added
from selenium.webdriver.support.ui import WebDriverWait

def addAccount(db, userDataDir) :
                print('Will add new account info')
                id = input('ID > ')
                passd = input('PW > ')
                folder = input('Cookie Folder Name > ')
                followerCount = int(input('How many follow today? > '))
                userDataDir = "user-data-dir=" + folder

                db.insert({'id':id,'passd':passd,'folder':folder,'followerCount':followerCount})
                return db, userDataDir


def main():
    print('Instagram Auto Liker Activating...')

    # Chrome init
    try:
        folder=''
        userDataDir = ''
        db = TinyDB('account.json', sort_keys=False, separators=(',',': '))

        
        if len(db.all()) == 0 :
            print('None of account info detected')
            addAccount(db,userDataDir)

        else : 
            
            switch = int(input('What Would you like to do? \n 1. login \n 2. add account \n 3. remove accounts \n > '))

            if switch == 1 : 
               print(db.all())
               loginSelection = int(input('Which account would you login? > '))
               selectedAccount = db.get(doc_id=loginSelection)
               print(selectedAccount)
               id = selectedAccount['id']
               passd = selectedAccount['passd']
               folder = selectedAccount['folder']
               followerCount = selectedAccount['followerCount']
               print (id, passd, folder, followerCount)

            elif switch == 2:
                addAccount(db,userDataDir)

            elif switch == 3 :
                removal = input('Would you like to remove all login info? y or n > ')
                if removal == 'y' : 
                    db.purge()
                    db.all()
                else :
                    pass


        # To put a Cookie folder 
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}

        userDataDir = "user-data-dir=" + folder
        chrome_options.add_argument(userDataDir)
        chrome_options.add_experimental_option("prefs",prefs)
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.implicitly_wait(3)
        url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
        driver.get(url)


        hashtag = [u"#유기묘",u"#사지마세요입양하세요",u"#사지말고입양하세요",u"#환경보호",u"#플라스틱",u"#플라스틱프리챌린지",u"#일회용품줄이기",u"#요가원",u"#일회용품줄이기",u"#제로웨이스트",u'#요가여행',u"#요가프로필",u"#yogabarn",u"#radiantlyyoga",u"#ecofriendly",u"#plasticfree",u"#플라스틱프리",u"#발리요가",u"#발리요가",u"#명상",u"#stillness",u"#mediation",u"#요가반",u"#ecofriendly",u"#ecolife",u"#에코라이프",u"#플라스틱줄이기"] 
        # hashtag = [u"#아깽이",u"#아깽이그램",u"#냥이",u"#구조냥",u"#catstagram",u"#kitten",u"#아깽이",u'#구조고양이',u"#고양이",u"#집사",u"#냥스타그램",u"#냥이",u"#고양이그램"]
        # hashtag = [u"#긍정부자",u"#여행자",u"#배낭여행",u"#동물구조",u"#생산성",u"#독서그램",u"#독서스타그램"]

        time.sleep(1)

        # Check whether it's login page or not
        try :
            print('#3 trying to user info for login')
            username = driver.find_element_by_name('username')
            username.send_keys(id)

            password = driver.find_element_by_name('password')
            password.send_keys(passd)

            password.send_keys(Keys.ENTER)
            
            print('#4 login Succeded')
            
        except NoSuchElementException  :
            print('no need login')
            pass

            
        # type t or h on cmd
            # t = HashTag liker
            # h = Homefeed liker
        user_input = input("MODE : 't'ag ? or 'h'omefeed ?  ")
        print ('user_input : %s' % user_input)   


        # ----------------------------------------------------- Option Choose
        # Homefeed liker 
        if user_input == 'h' : 
            print ('%s key pressed, Homefeed liker Activated' % user_input) 
            
            # scrolling & liked counts init in Homefeed
            c = 0
            print('home like %s counting init' % c)
            for i in range(0, 200):
                like = driver.find_elements_by_css_selector("span.fr66n button span.glyphsSpriteHeart__outline__24__grey_9")
                print ('Like Hearts : %s ' % like)
                if len(like)==0 : 
                    print('There is no more hearts likable')
                    break
                else : 
                    home_feed_liker(like, driver, c)
                    time.sleep(0.5)
                    scrolling(driver,c)



        # hashtag liker
        elif user_input =='t' :
            print (' %s key pressed, Tag Liker Activated' % user_input)
            print ('tags : [ %s ] ' % hashtag )
            f = 0
            i = 0
            while ( i < len(hashtag) ):
                hashtag_liker(driver, hashtag, i, f, followerCount)
                i = i + 1

        else:
            user_input = input("'H'omefeed / on 'T'ag feed > ")
            print (': %s' % user_input)   


        time.sleep(10)

       
    except Exception as e:
        print ('type is:', e.__class__.__name__)
        print_exc()






def hashtag_liker(driver, hashtag, i,f, followerCount):
        lenList = len(hashtag)-1
        ranNum = random.randint(0,lenList)
        print ('%s th hashtag in hashtag list, will be chosen ' % ranNum)

        # hashtag input field lookup
        hashtag_input_elem = driver.find_element_by_css_selector("input.XTCLo.x3qfX") # search input targeting
        print ('#6 hashtag input %s' % hashtag[ranNum] )
        hashtag_input_elem.send_keys(hashtag[ranNum]) # type into Hashtag input blank
        hashtag_input_elem.send_keys(Keys.ENTER)
         # hashtag searching

        # Click Tag list on Dropdown 
        print ('#7 try to click target hastag list')
        target_tag_elem_list = driver.find_elements_by_css_selector('a.yCE8d  ')
        print ('target_tag_elem_list length :', len(target_tag_elem_list))
        try : 
            target_tag_elem = target_tag_elem_list[0]
            print ('target_tag_elem : ' , target_tag_elem)
            target_tag_elem.click() # first listed hashtag click!
            # hastag list isn't clickable, then...
        except : 
            pass
       


        # Click Most recent img
        try:
            # most_recent_img = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[1]/img')
            most_recent_img =driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
        except NoSuchElementException :
            most_recent_img =driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]')

        most_recent_img.click()

        # clicked_img = driver.find_element_by_css_selector('img.FFVAD')
        # img_alt = clicked_img.get_attribute('alt')
        # print ('img alt : %s ' % img_alt)
        
        nsee_count = 0
        for i in range(0,500):

            # Like!
            try :
                like = driver.find_element_by_css_selector("span.fr66n button span.glyphsSpriteHeart__outline__24__grey_9")
                clicked_img = driver.find_element_by_css_selector('img.FFVAD')
                img_alt = clicked_img.get_attribute('alt')
                print ('img alt : %s ' % img_alt)
                
                print ('like : %s ' % like)
                like.click()

                print ('like clicked! %s th ' % i )
           
                # Follow!
                follow = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                elem_class = follow.get_attribute('class')           

                if '_8A5w5' in elem_class :
                    pass # 'already following' button has the '_8a5w5' class name

                elif f < followerCount :   # 30 people following possible in a term only!
        
                    # print ('follow click unactivated'    )
                    follow.click()
                    print ('follow clicked! %s th following! ' % f)
                    f = f + 1
                else :
                    pass

                # Click right post
                right_arrow = driver.find_element_by_css_selector("a.HBoOv.coreSpriteRightPaginationArrow")
                right_arrow.click()

                time.sleep(1)

            # if cannot find like icon, it's already choosed before, so click right
            except NoSuchElementException :
                nsee_count =  nsee_count + 1
                print ('already liked or no heart on this page, %s times missed! ' % nsee_count)
                if nsee_count == 10 :
                    break
                else :
                    try : 
                        right_arrow = driver.find_element_by_css_selector("a.HBoOv.coreSpriteRightPaginationArrow")
                        right_arrow.click()
                    except NoSuchElementException :
                    # break loop, go to next hashtag
                        break
                    pass


        # winsound.PlaySound('mario-stage-clear.mp3',winsound.SND_FILENAME)
        print ('like all done! on hashtag!  !! XD! Happy yah!!' )
        
        driver.get('https://instagram.com/')
        

def home_feed_liker(like, driver,c ):
        ec = 0

        for like_link in like:
            try:
                print('How many likes in this page > %s ' % len(like) )
                print('like_link : %s ' % like_link)
                like_link.location_once_scrolled_into_view
                like_link.click()
                time.sleep(0.5)
                c = c + 1
                print('%s th liked! ' % c)

            except Exception as e:
                str_e = str(e)
                print(str_e)
                ec=ec+1
                print
                print('Home Feed Liker : %s times passed!' % ec )
                print
                if ec == 10 : 
                    driver.get('https://instagram.com')
                else :
                    return None

                
        
def scrolling(driver,s):
    try:
        print('Scrolling!')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    except Exception as es:
        print ('type is:', es.__class__.__name__)
        print_exc()

main()

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


def main():
    print('Instagram Auto Liker Activating...')

    # Encode init
    print('Encode init')

    # Chrome init
    try:
        # Chrome options
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)


        chrome_options.add_argument("--start-maximized")


        print ('----------------------------------------')
        print ('[login id, identified]')
        print ('id : %s' % id )
        print ('pw : %s' % passd )
        print ('----------------------------------------')
        print (chrome_options._arguments)

        # Creating driver
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.implicitly_wait(5)
        # 1st driver opens the url
        url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
        driver.get(url)



        print('#1 chrome to open')

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
                home_feed_liker(like, driver, c)
                time.sleep(0.5)
                scrolling(driver,c)



        # hashtag liker
        elif user_input =='t' :
            print (' %s key pressed, Tag Liker Activated' % user_input)

            f = 0
            i = 0
            while ( i < len(hashtag) ):
                hashtag_liker(driver, hashtag, i, f)
                i = i + 1

        else:
            user_input = input("t or h?")
            print (': %s' % user_input)   


        time.sleep(10)

       
    except Exception as e:
        print ('type is:', e.__class__.__name__)
        print_exc()






def hashtag_liker(driver, hashtag, i,f):
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
        target_tag_elem = target_tag_elem_list[0]
        print ('target_tag_elem : ' , target_tag_elem)
        target_tag_elem.click() # first listed hashtag click!



        # Click Most recent img
        try:
            # most_recent_img = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[1]/img')
            most_recent_img =driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
        except NoSuchElementException :
            most_recent_img =driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]')

        most_recent_img.click()

        clicked_img = driver.find_element_by_css_selector('img.FFVAD')
        img_alt = clicked_img.get_attribute('alt')
        print ('img alt : %s ' % img_alt)
        
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

                elif f < 30 :   # 30 people following possible in a term only!
        
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
                print(' ')
                print('like_link : %s ' % like_link)
                print(' ')
                like_link.location_once_scrolled_into_view
                like_link.click()
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

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
import pyarabic.araby as araby
import random
import time
import threading
import requests
import sys
import pyperclip


# i = [
#     "قُلْ أَعُوذُ بِرَبِّ النَّاسِ",
#     "مَلِكِ النَّاسِ",
#     "إِلَٰهِ النَّاسِ",
#     "مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ",
#     "الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ",
#     "مِنَ الْجِنَّةِ وَالنَّاسِ"
# ]

i = ['قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ مِنْ شَرِّ مَا خَلَقَ وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ  وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ',
     'قُلْ أَعُوذُ بِرَبِّ النَّاسِ ,  مَلِكِ النَّاسِ  إِلَٰهِ النَّاسِ مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ  الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ مِنَ الْجِنَّةِ وَالنَّاسِ', 'قُلْ هُوَ اللَّهُ أَحَدٌ اللَّهُ الصَّمَدُ لَمْ يَلِدْ وَلَمْ يُولَدْ وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ']


keyboard = Controller()


# Initiate the browser
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("--disable-extensions")
option.add_argument('--disable-gpu')
option.add_argument('--window-size=10x10')
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

#
driver = webdriver.Chrome(options=option)
driver.get('https://www.facebook.com/')
username = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")
submit = driver.find_element_by_xpath(
    "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button")


def clearConsole(): return print('\n' * 150)


def setDefaultInputs():
    global userMail
    userMail = 'YOUR EMAIL'
    global userPswd
    userPswd = 'YOUR PASS'


# Check Credentials
if(len(sys.argv) == 3):
    if(len(sys.argv[1]) > 6 & len(sys.argv[2]) > 6):
        userMail = sys.argv[1]
        userPswd = sys.argv[2]
    else:
        setDefaultInputs()
else:
    setDefaultInputs()

username.send_keys(userMail)
password.send_keys(userPswd)

# Check Duration
if(int(sys.argv[3]) > 119):
    Duration = int(sys.argv[3])
else:
    Duration = 300

submit.click()
WebDriverWait(driver, 10).until_not(EC.title_is(driver.title))
driver.find_element_by_xpath('/html/body').click()
time.sleep(4)


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def Ayat():

    clearConsole()
    print('STARTING SERVICE @ ' + str(Duration) + ' / Seconds !')

    s = requests.get(url='http://api.alquran.cloud/v1/ayah/' +
                     str(random.randint(1, 6235))+'/ar.asad').json()
    #

    imgUrl = requests.get(
        url='https://pixabay.com/api/?key=18637251-d69e18d5fb1bebfc1c62359fa&q=masjid&page='+str(random.randint(1, 3))+'&per_page=200').json()['hits'][random.randint(0, 199)]['largeImageURL']
    pyperclip.copy(imgUrl)

    keyboard.press('p')
    keyboard.release('p')

    time.sleep(4)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL)
    actions.send_keys("v")
    actions.key_up(Keys.CONTROL)
    actions.perform()
    time.sleep(2)

    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL)
    actions.send_keys("z")
    actions.key_up(Keys.CONTROL)
    actions.perform()
    time.sleep(2)

    # actions.send_keys(i[random.randint(0, len(i)-1)])
    # Paste picture
    # actions.key_down(Keys.CONTROL)
    # actions.send_keys("v")
    # actions.key_up(Keys.CONTROL)
    # actions.perform()

    actions = ActionChains(driver)
    actions.send_keys('ـ ﷽ ـ' + '\n')
    actions.send_keys(s['data']['text'])
    actions.send_keys('\n' + ' [ ' + araby.strip_diacritics(s['data']['surah']['name']) + ' : ' +
                      str(s['data']['numberInSurah']) + ' ] ')

    actions.perform()
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[3]/div[2]/div/div').click()
    time.sleep(4)
    # driver.close()
    # driver.quit()


Ayat()
set_interval(Ayat, Duration)

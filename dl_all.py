# import dryscrape
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import os
import urllib
import argparse
import csv
import re



downloaded_links = set()
download_type = 0
SIDEBAR_LOAD_URL ='#course-page-sidebar > div > ul.course-navbar-list > li:nth-child(n)'

def mkdir_safe(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_filename(path):
    return "".join([c for c in path if re.match(r'\w', c)])


def wait_for_load(session):
    # session.wait_for(lambda session: len(session.css('#course-page-sidebar > div > ul.course-navbar-list > li:nth-child(n)')) >= 1)
    WebDriverWait(session, 30).until(
        lambda session: len(session.find_elements_by_css_selector(SIDEBAR_LOAD_URL)) >=1)

def render(session, path):
    if download_type==0 or download_type==2:
        # session.render(path+'.png')
        session.save_screenshot(path+'.png')
    if download_type==0 or download_type==1:
        f = open(path+'.html', 'wb')
        # f.write(session.body().encode('utf-8'))
        f.write(session.page_source.encode('utf-8'))
        f.close()

def login(session, URL, email, password):   #ugly ugly code in here
    session.get(URL)
    # print(session.find_elements_by_css_selector('#user-modal-email')))
    WebDriverWait(session, 30).until(
        lambda session: len(session.find_elements_by_css_selector('#user-modal-email'))>2)



    x = session.find_elements_by_css_selector('#user-modal-email')[1]
    x.send_keys(email)
    x = session.find_elements_by_css_selector('#user-modal-password')[1]
    x.send_keys(password)
    # print(os.getcwd())
    render(session, os.getcwd()+'/entered_login')
    session.find_elements_by_css_selector('form > button')[1].click()

    WebDriverWait(session, 30).until(
        lambda session: len(session.find_elements_by_css_selector(SIDEBAR_LOAD_URL)) >=1 or
                        len(session.find_elements_by_css_selector('.c-coursePage-sidebar-enroll-button'))>=1 or
                        len(session.find_elements_by_css_selector('#agreehonorcode'))>=1 or
                        session.page_source.find('Remove from watchlist')!=-1)

    if len(session.find_elements_by_css_selector('.c-coursePage-sidebar-enroll-button')) >=1:
        session.find_elements_by_css_selector('.c-coursePage-sidebar-enroll-button')[0].click()  #enroll button
        WebDriverWait(session, 10).until(lambda session:  len(session.find_elements_by_css_selector(SIDEBAR_LOAD_URL)) >=1 or
                                                          len(session.find_elements_by_css_selector('.fullbleed'))>=1 or
                                                          session.page_source.find('we will notify you by email when it starts')!=-1 or
                                                          session.page_source.find('ll email you if there are new session dates')!=-1)
        if len(session.find_elements_by_css_selector('.fullbleed'))>=1 and session.find_elements_by_css_selector('.fullbleed')[0].text.find('Learn more')==-1:
            session.find_elements_by_css_selector('.fullbleed')[0].click() #go to course button
            WebDriverWait(session, 10).until(lambda session: len(session.find_elements_by_css_selector(SIDEBAR_LOAD_URL)) >=1 or
                                                         len(session.find_elements_by_css_selector('#agreehonorcode'))>=1)
            if len(session.find_elements_by_css_selector(SIDEBAR_LOAD_URL)) >=1:
                pass
            elif len(session.find_elements_by_css_selector('#agreehonorcode'))>=1:
                session.find_elements_by_css_selector('#agreehonorcode')[0].click()
                wait_for_load(session)
        elif len(session.find_elements_by_css_selector(SIDEBAR_LOAD_URL)) >=1:
            pass
        else:
            print("Error: Impossible to access course"+URL)
            return -1
    elif len(session.find_elements_by_css_selector('#agreehonorcode'))>=1:
        session.find_elements_by_css_selector('#agreehonorcode')[0].click()
        wait_for_load(session)
    elif session.page_source.find('Remove from watchlist')!=-1:
        print("Error: Impossible to access course"+URL)
        return -1

    render(session, os.getcwd()+'/course_home')
    return 0

def download_all_zips_on_page(session, path='assignments'):
    links = session.find_elements_by_css_selector('a')

    if not os.path.exists(path):
        os.makedirs(path)
    txt_file = open(path+'/links.txt', 'w')
    links = [i for i.get_attribute('href') in links]
    for i in links:
        url = i
        if url==None:
            continue
        url_ex = os.path.splitext(url)[1]
        txt_file.write(url+'\n')
        hw_strings = ['.zip', '.py', '.m', '.pdf', '.txt']
        is_hw = False
        for j in hw_strings:
            if url_ex.find(j)!=-1:
                is_hw = True
                continue

        if is_hw:
            # print(url)
            if url in downloaded_links:
                continue
            else:
                downloaded_links.add(url)
            try:
                if sys.version_info >= (3, 0):
                    urllib.request.urlretrieve(url, path+url[url.rfind('/'):])
                else:
                    urllib.urlretrieve(url, path+url[url.rfind('/'):])
            except urllib.error.HTTPError:
                print("Failed to download "+url)
                continue
            render(session, os.getcwd()+'/'+path+'/zip_page')

def get_quiz_types(session):
    links = session.find_elements_by_css_selector('#course-page-sidebar > div > ul.course-navbar-list > li:nth-child(n) > a')
    for idx in range(len(links)):
        links[idx] = (links[idx].get_attribute('href'), links[idx].text)
        if links[idx][0][0]=='/':
            links[idx] = ('https://class.coursera.org'+links[idx][0], links[idx][1])
            # print(links)

    links = [i for i in links if i[0].find('/quiz')!=-1]
    links = list(set(links))
    return links


def get_quiz_info(session, url, category_name):
    session.get(url)
    wait_for_load(session)
    render(session, os.getcwd()+'/'+category_name)
    links = session.find_elements_by_css_selector('#spark > div.course-item-list > ul:nth-child(n) > li > div:nth-child(n) > div > a')
    for idx in range(len(links)):
        links[idx] = links[idx].get_attribute('href')

    names = session.find_elements_by_css_selector('#spark > div.course-item-list > ul:nth-child(n) > li > div:nth-child(n) > h4')
    for idx in range(len(names)):
        names[idx] = names[idx].text.replace(' ', '_')
        names[idx] = names[idx][:names[idx].rfind('Help Center')-len('Help Center')]
    # print(names)
    return zip(links, names)

class Quiz(object):
    url = ''
    name = ''
    number = 0
    def __init__(self, url, number, name):
        self.url = url
        self.number = number
        self.name = name



def download_quiz(session, quiz, category_name):
    session.get(quiz.url)
    wait_for_load(session)
    path = category_name+'/'+str(quiz.number)+'_'+clean_filename(quiz.name)+'/'
    mkdir_safe(path)

    if session.current_url.find('attempt')==-1:
        if len(session.find_elements_by_css_selector('#spark > form > p > input')) == 0:
            print("Error: Couldn't download "+quiz.name)
        session.find_elements_by_css_selector('#spark > form > p > input')[0].click()
        wait_for_load(session)

    download_all_zips_on_page(session, path)
    render(session, os.getcwd()+'/'+path+str(quiz.number)+'_'+quiz.name)

def download_all_quizzes(session, quiz_info, category_name):
    # print(quiz_info)
    for idx, i in enumerate(quiz_info):
        quiz_obj = Quiz(i[0], idx, clean_filename(i[1]))
        download_quiz(session, quiz_obj, clean_filename(category_name))

def get_assign_info(session):
    session.get(class_url+'assignment')
    wait_for_load(session)
    render(session, os.getcwd()+'/assignment_home')
    links= session.find_elements_by_css_selector('#spark > div.course-item-list > ul:nth-child(n) > li > div:nth-child(2) > a')
    for idx in range(len(links)):
        links[idx] = links[idx].get_attribute('href')

    name = session.find_elements_by_css_selector('#spark > div.course-item-list > ul:nth-child(n) > li > h4')
    for idx in range(len(name)):
        name[idx] = name[idx].text
        print(name[idx])
        # name[idx] = name[idx][:name[idx].rfind('Help Center')-len('Help Center')]
        name[idx] = name[idx].split('\n')[0]

    print(name)
    return zip(links, name)

def download_all_assignments(session, assign_info):
    for i in assign_info:
        session.get(i[0])
        wait_for_load(session)
        download_all_zips_on_page(session, 'assignments/'+i[1])

def download_sidebar_pages(session):
    links = session.find_elements_by_css_selector('#course-page-sidebar > div > ul.course-navbar-list > li:nth-child(n) > a')
    # print(links)
    for idx in range(len(links)):
        links[idx] = (links[idx].get_attribute('href'), clean_filename(links[idx].text))
        if links[idx][0][0]=='/':
            links[idx] = ('https://class.coursera.org'+links[idx][0], links[idx][1])
    links = [i for i in links if i[0].find('/quiz')==-1 and i[0].find('class.coursera.org')!=-1 and i[0].find('/lecture')==-1]
    links = list(set(links))
    print(links)
    for i in links:
        session.get(i[0])
        wait_for_load(session)
        path = i[1]+'/'
        download_all_zips_on_page(session, path)
        render(session, os.getcwd()+'/'+path+i[1])

def get_class_url_info(x):
    cur = x[0].rstrip()
    cur = cur.rstrip('/')
    class_slug = cur[cur.rfind('/')+1:]
    class_url = "https://class.coursera.org/"+class_slug+'/'

    return (class_url, class_slug)

parser = argparse.ArgumentParser('')
parser.add_argument('-u', help="username/email")
parser.add_argument('-p', help="password")
parser.add_argument('--path', help="give a path for the folder coursera-downloads to be created")
parser.add_argument('--download_type', help='0 for .html and .png, 1 for .html only, and 2 for .png only', type=int, default=1)
parser.add_argument('--headless', help='If Phantom.JS is installed, enable this option to hide the browser', action="store_true")
parser.add_argument('-q', help="download quizzes?", action="store_true")
parser.add_argument('-a', help="download assignments?", action="store_true")
parser.add_argument('-v', help="download videos using coursera-dl?", action="store_true")
parser.add_argument('--ns', help="Don't download sidebar links", action="store_true")

args = parser.parse_args()
if not args.u or not args.p:
    print("Please enter a username and a password using the -u and -p tags")
    sys.exit()

if args.download_type:
    download_type = args.download_type

csvfile = open('classes.csv', 'r')
reader = csv.reader(csvfile, delimiter = ' ')
if args.path:
    os.chdir(args.path)
mkdir_safe("coursera-downloads")
os.chdir("coursera-downloads")

for i in reader:

    class_url, class_slug = get_class_url_info(i)
    print(class_url, class_slug)
    mkdir_safe(class_slug)
    if (args.v):
        os.system('coursera-dl -u '+args.u+' -p '+args.p+' --path='+os.getcwd()+' '+class_slug)
    os.chdir(class_slug)

    # session = dryscrape.Session()
    session=''
    if args.headless:
        session = webdriver.PhantomJS()
    else:
        session = webdriver.Firefox()
    print("Logging In....")
    error = login(session, class_url, args.u, args.p )
    if (error==-1):
        session.close()
        continue
    print("Logged in!")
    # if

    if not args.ns:
        download_sidebar_pages(session)

    if (args.q):
        # quiz_info = get_quiz_info(session)
        print("Downloading Quizzes....")
        quiz_links = get_quiz_types(session)
        for i in quiz_links:
            print("Downloading "+i[1])
            quiz_info = get_quiz_info(session, i[0], i[1])
            download_all_quizzes(session, quiz_info, i[1])
    # print(class_url)
    if (args.a):
        mkdir_safe("assignments")
        assign_info = get_assign_info(session)
        download_all_assignments(session, assign_info)
    os.chdir('..')
    session.close()












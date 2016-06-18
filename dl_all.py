import dryscrape
import time
import sys
import os
import urllib
import argparse
import csv


def wait_for_load(session):
    session.wait_for(lambda: len(session.css('#course-page-sidebar > div > ul.course-navbar-list > li:nth-child(n)')) >= 1)

def login(session, URL, email, password):
    session.visit(URL)
    session.wait_for(lambda: len(session.css('#user-modal-email'))>2)
    x = session.css('#user-modal-email')[1]
    x.set(email)
    x = session.css('#user-modal-password')[1]
    x.set(password)
    print os.getcwd()
    session.render(os.getcwd()+'/entered_login.png')
    session.css('form > button')[1].click()
    wait_for_load(session)
    session.render(os.getcwd()+'/course_home.png')

def download_all_zips_on_page(session, path='assignments'):
    links = session.css('a')

    if not os.path.exists(path):
        os.makedirs(path)
    txt_file = open(path+'/links.txt', 'w')

    for i in links:
        txt_file.write(i.get_attr('href')+'\n')
        if i.get_attr('href').find('.zip')!=-1:
            print i.get_attr('href')

            urllib.urlretrieve(i.get_attr('href'), path+i.get_attr('href')[i.get_attr('href').rfind('/'):])
            session.render(path+'/zip_page.png')

def obtain_quiz_info(session, url, category_name):
    session.visit(url)
    wait_for_load(session)
    session.render(category_name+'_home.png')
    links = session.css('#spark > div.course-item-list > ul:nth-child(n) > li > div:nth-child(n) > div > a')
    for idx in range(len(links)):
        links[idx] = links[idx].get_attr('href')

    names = session.css('#spark > div.course-item-list > ul:nth-child(n) > li > div:nth-child(n) > h4')
    for idx in range(len(names)):
        names[idx] = names[idx].text().replace(' ', '_')
        names[idx] = names[idx][:names[idx].rfind('Help Center')-len('Help Center')]
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
    session.visit(quiz.url)
    wait_for_load(session)
    path = category_name+'/'+str(quiz.number)+'_'+quiz.name+'/'
    if not os.path.exists(path):
        os.makedirs(path)

    if session.url().find('attempt')==-1:
        session.css('#spark > form > p > input')[0].click()
        wait_for_load(session)

    download_all_zips_on_page(session, path)
    session.render(os.getcwd()+'/'+path+str(quiz.number)+'_'+quiz.name+'.png')

def download_all_quizzes(session, quiz_info, category_name):
    for idx, i in enumerate(quiz_info):
        quiz_obj = Quiz(i[0], idx, i[1])
        download_quiz(session, quiz_obj, category_name)

def obtain_assign_info(session):
    session.visit(class_url+'assignment')
    wait_for_load(session)
    session.render(os.getcwd()+'assignment_home.png')
    links= session.css('#spark > div.course-item-list > ul:nth-child(n) > li > div:nth-child(2) > a')
    for idx in range(len(links)):
        links[idx] = links[idx].get_attr('href')

    name = session.css('#spark > div.course-item-list > ul:nth-child(n) > li > h4')
    for idx in range(len(name)):
        name[idx] = name[idx].text()
        name[idx] = name[idx][:name[idx].rfind('Help Center')-len('Help Center')]

    return zip(links, name)

def download_all_assignments(session, assign_info):
    for i in assign_info:
        session.visit(i[0])
        wait_for_load(session)
        download_all_zips_on_page(session, 'assignments/'+i[1])


parser = argparse.ArgumentParser('')
parser.add_argument('-u', help="username/email")
parser.add_argument('-p', help="password")
parser.add_argument('-q', help="download quizzes?", action="store_true")
parser.add_argument('-a', help="download assignments?", action="store_true")
parser.add_argument('-v', help="download videos using coursera-dl?", action="store_true")
args = parser.parse_args()
if not args.u or not args.p:
    print "Please enter a username and a password using the -u and -p tags"
    sys.exit()

csvfile = open('classes.csv', 'r')
reader = csv.reader(csvfile, delimiter = ' ')
if not os.path.exists("coursera-downloads"):
    os.mkdir("coursera-downloads")
os.chdir("coursera-downloads")

for i in reader:
    cur = i[0].rstrip()
    class_url = ''
    class_slug = ''
    if cur.find('class.coursera')==-1:
        class_url = 'https://class.coursera.org/'+cur+'/'
        class_slug = cur
    else:
        class_url = cur
        cur = cur.rstrip('/')
        class_slug = cur[cur.rfind('/')+1:]
    print class_url
    print class_slug

    os.mkdir(class_slug)
    if (args.v):
        os.system('coursera-dl -u '+args.u+' -p '+args.p+' --path='+os.getcwd()+' '+class_slug)
    os.chdir(class_slug)
    os.mkdir('assignments')
    # class_url= "https://class.coursera.org/pgm-003/"
    # class_url = 'https://class.coursera.org/neuralnets-2012-001/'
    # class_url='https://class.coursera.org/algs4partII-007'

    session = dryscrape.Session()
    print "Logging In...."
    login(session, class_url, args.u, args.p )
    print "Logged in!"


    if (args.q):
        # quiz_info = obtain_quiz_info(session)
        print "Downloading Quizzes...."
        links = session.css('#course-page-sidebar > div > ul.course-navbar-list > li:nth-child(n) > a')
        for idx in range(len(links)):
            links[idx] = (links[idx].get_attr('href'), links[idx].text())
            if links[idx][0][0]=='/':
                links[idx] = ('https://class.coursera.org'+links[idx][0], links[idx][1])
        print links

        links = [i for i in links if i[0].find('/quiz')!=-1]
        links = list(set(links))

        print links
        for i in links:
            print "Downloading "+i[1]
            quiz_info = obtain_quiz_info(session, i[0], i[1])
            download_all_quizzes(session, quiz_info, i[1])
    # print class_url
    if (args.a):
        assign_info = obtain_assign_info(session)
        download_all_assignments(session, assign_info)
    os.chdir('..')












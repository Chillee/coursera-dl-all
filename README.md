# coursera-dl-all

#NOTE: THIS PROJECT IS OBSOLETE AFTER 6/30/2016. Coursera has fully committed to their new format, and this application was designed for their old class format. 
Extend the Coursera Downloader by downloading quizzes and assignments (and hopefully forum posts soon!). Uses coursera-dl in the process.  

![An example of download](http://www.imgur.com/HTd028B.png)

##Features
Cross-Platform (theoretically!) Python 2 & 3  
Download quizzes  
Download important files on assignment pages  
Download videos (credits to coursera-dl)  
Download sidebar links (Errata, Resources, etc.)  
Download text file of important links.  
Ability to automatically sign up for a class / bypass the honor code stuff (so you don't need to sign up for a class manually to download it).  
A list of all classes on the old platform for Coursera  


##Step by Step Instructions (Thanks to Light1980 for the initial write up)
1. Make sure you have Firefox installed (below version 47)
2. Make sure you have python installed (2 or 3, although 3 is preferred)
3. Install coursera_dl with pip if you want to download videos. `pip install coursera_dl`
4. Download this repository as a zip file.
5. Unzip the file to your preferred location.
7. Fill in classes.csv file with your course url / slugs and save. `pgm-003` or `class.coursera.org/pgm-003`
8. open up your terminal/CMD and change your directory to the location of dl_all.py.
For example:  
`cd F:\coursera-dl-all-master\coursera-dl-all-master`
9. Write command like (the things in parenthese are for explanation and should not be kept)

`python dl_all.py -u your_coursera_account -p your_password  -v(download video) -a(download assignment) -q(download quiz) --path the_location_of_download`

##Todo:
Add support for forums  
Add support for human graded assignments  
Fix bugs for any courses  
Suggestions?

##Installation
-Coursera-Dl. This must be installed if you want to download videos. If you only need to download non video stuff, just don't use the -v tag.  
pip install coursera-dl

-Selenium  
pip install selenium

-PhantomJS. (optional) If you want to run the program with the browser invisible, install this

##
##To run:

First populate the classes.csv with slugs or URLs of desired classes. Slugs would be things like pgm-003 while the URL would be https://class.coursera.org/pgm-003

note: coursera.org/learn/<class> doesn't work.  
Next, run the program with the following tags:
-u: for username/email  
-p: for password  
-q: (optional) to download quizzes  
-v: (optional) to download videos  
-a: (optional) to download assignments  
--path: (optional) a path for coursera-download folder to be downloaded to
--download_type: (optional) 0 for .html and .png files for each page, 1 for .html only, 2 for .png only
--headless: (optional) if you install PhantomJS, you can run this program without that pesky browser popping up.

So classes.csv might look something like:

https://class.coursera.org/gametheory-005/
neuralnets-2012-001

while your command line prompt would be:

python dl_all.py -u horacehe2007@yahoo.com -p hunter2 -q -v

note: you must be signed up for the courses.
Note: A list of all classes is provided (not in the right format though)

##Output
The output is sorted into categories. Assignments is always there, and the other categories are pulled from the site itself.

Each category (e.g. Quizzes, Assignments, Homework) is split into subfolders for each quiz/assignment. Each of these folders hold a screenshot of the page, all zip files on the page, a links.txt holding all links on the page (in case there's files that you need to download that aren't a zip file).

This would download all the quizzes and videos for the game theory and neural nets course.

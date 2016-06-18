# coursera-dl-all
Extend the Coursera Downloader by downloading quizzes and assignments (and hopefully forum posts soon!). Uses coursera-dl in the process.

Dependencies:
-Coursera-Dl. This must be installed if you want to download videos. If you only need to download non video stuff, just don't use the -v tag.  
-dryscrape https://dryscrape.readthedocs.io/en/latest/installation.html#recommended-installing-dryscrape-from-pypi

To run:
First populate the classes.csv with slugs or URLs of desired classes. Slugs would be things like pgm-003 while the URL would be https://class.coursera.org/pgm-003

Next, run the program with the following tags:
-u: for username/email  
-p: for password  
-q: (optional) to download quizzes  
-v: (optional) to download videos  
-a: (optional) to download assignments  

So classes.csv might look something like:

https://class.coursera.org/gametheory-005/
neuralnets-2012-001

while your command line prompt would be:

python dl_all -u horacehe2007@yahoo.com -p hunter2 -q -v

This would download all the quizzes and videos for the game theory and neural nets course.

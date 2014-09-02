import urllib
import urllib2
import re
from twython import Twython
from BeautifulSoup import BeautifulSoup

#Twitter info
#TO DO: Need to move into its own file
APP_KEY = "nWDbGdIEm8jXn8NGowtdlzPKV"
APP_SECRET = "ZqF6uQim5p3ATT3ta7RcwmzVzzrMEzcvhpbO5MOScnPJc3Yr0f"
OAUTH_TOKEN = "237003031-Oa3EOrmIGLfE8mKwaG0aWd7AmNGKUKnSP2UvyCJq"
OAUTH_TOKEN_SECRET = "HmNu5qgaWj77jm7N47rpG1rpV2tuHfeT20XTBgY8hC0Jt"

#Array of URLs to scrape
urls = ["http://www.buzzfeed.com/food"]
i=0

#Loop through our URLs and dump them into a file
#TO DO: Write each URL to a unique file or handle processing here
#Only buzzfeed right now, so it is passable
while i< len(urls):
  htmlfile = urllib.urlopen(urls[i])
  htmltext = htmlfile.read()
  f = open("temp.txt", "w")
  f.write(htmltext)
  f.close()
  i+=1

#Open our temp file for reading
f = open("temp.txt", "r")

#Set a key
#TO DO: Provide organic mechanism to delimit on (Unsure if really needed)
key = "href"

#Create our list to work with
url_list = []

#Loop through the lines in the file and find our 2nd key, do some fancy processing
#TO DO: Set 2nd key in a variable
for line in f:
  if 'gt_click="2"' in line:
    before_key, key, after_key = line.partition(key)
    url_list.insert(0, after_key.split('"')[1])

f.close()

i=0
url_list_temp = []

#Be slightly lame and work with a temp list to get a unique list
#TO DO: This method is a bit slow, need to make faster, possibly with set
for i in url_list:
  if not i in url_list_temp:
    url_list_temp.insert(0, i)

temp = ['http://www.buzzfeed.com{0}'.format(i) for i in url_list_temp]

#Let's get our properly formatted URL list out to a file
#TO DO: Write to DB
f = open("urls.txt", 'w')
for i in temp:
  f.write("%s\n" % i)
f.close()

#And let's extract some titles now that we have URLs to work with
#TO DO: Write to DB
f = open("urls.txt", 'r')
o = open("titles.txt", 'w')
for i in f:
  soup = BeautifulSoup(urllib2.urlopen("%s" % i))
  o.write("%s\n" % soup.title.string)
f.close()
o.close()

#Set twitter vars
twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#Create some arrays
t_url_arr = []
t_title_arr = []
t_title_arr_temp = []

#Populate URL array
f = open("urls.txt", 'r')
for i in f:
  t_url_arr.insert(0, i)
f.close()

#Populate title array
f = open("titles.txt", 'r')
for i in f:
  t_title_arr.insert(0, i)
f.close()

#Some hackery to chop out nonsense from the titles
for i in t_title_arr:
  t_title_arr_temp.insert(0, i.replace("&#39;", "'"))

t_title_arr = []

for i in t_title_arr_temp:
  t_title_arr.insert(0, i.replace(" &amp;", ""))

#Post to Twitter
for i in range(0, len(t_url_arr)):
  twitter.update_status(status=t_title_arr[i] + t_url_arr[i])

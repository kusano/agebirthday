#!/usr/bin/python
# coding: utf-8

# ageの誕生日絵のアップを監視してTwitterに呟く

import urllib, re, time, tweepy

from token import *

URL			= "http://www.age-soft.co.jp/whatsnew/"
TWEETED		= "agebirthday.txt"		# 発言済みの日付を記録
LOG			= "agebirthdaylog.txt"		# ログ
# 検索用正規表現
REG			= (ur"""<p class="post-date">(?P<date>.*)</p>\s*"""+
			   ur"""<h3>(?P<title>.*)イラストを(アップ|掲載|公開).*?</h3>""")

def main():
	tweeted = open(TWEETED,"r").read().decode("utf-8").split()
	
	data = urllib.urlopen(URL).read().decode("utf-8")
	
	c = 0
	
	for m in re.finditer(REG,data):
		date = m.group("date")
		title = m.group("title")
		if date not in tweeted:
			print date,title
			
			tweet( u"%s ■%sイラストがアップロードされました■ http://www.age-soft.co.jp/" % (date,title) )
			
			tweeted += [date]
			log("tweeted")
		c += 1
	
	if c==0:
		log("??? no match")
		tweet( u"@kusano_k マッチ数0" )
	
	open(TWEETED,"w").write("\n".join(tweeted).encode("utf-8"))
	log("checked")

def tweet(msg):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	api.update_status(msg)

def log(msg):
	open(LOG,"a").write((time.strftime("%Y/%m/%d %H:%M:%S")+" "+msg+"\n").encode("utf-8"))

if __name__=="__main__":
	main()

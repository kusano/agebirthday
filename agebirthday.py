#!/usr/bin/python
# coding: utf-8

# ageの誕生日絵のアップを監視してTwitterに呟く

import urllib, re, time, tweepy

from token import *

URL			= "http://www.age-soft.co.jp/whats_new.html"
TWEETED		= "agebirthday.txt"		# 発言済みの日付を記録
LOG			= "agebirthdaylog.txt"		# ログ
# 検索用正規表現
REG			= (ur"""<div class="title1">([0-9/]*)　?(<.*?>)?</div>"""+
			   ur"""[\r\n]*"""+
			   ur"""<div class="title2">(.*?)イラストを(アップ|掲載|公開).*?</div>""")

def main():
	tweeted = open(TWEETED,"r").read().split()
	
	data = urllib.urlopen(URL).read().decode("cp932")
	#data = open("whats_new.html").read().decode("cp932")
	
	c = 0
	
	for m in re.finditer(REG,data):
		date = m.group(1)
		title = m.group(3)[1:]	# ■を削除
		if date not in tweeted:
			# print date,title
			
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
	open(LOG,"a").write(time.strftime("%Y/%m/%d %H:%M:%S")+" "+msg+"\n")

if __name__=="__main__":
	main()

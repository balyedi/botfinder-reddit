#!/usr/bin/env python3
import praw,json,math,time,datetime
from pprint import pprint

# parse credentials
fcred = open("credentials.json","r")
credentialsraw = fcred.read()
credentials = json.loads(credentialsraw)

# parse blacklisted comments 
fbcomment = open("blacklistedcomments.json","r")
bcommentraw = fbcomment.read()
bcomment = json.loads(bcommentraw)

reddit = praw.Reddit(
	client_id=credentials["client_id"],
	client_secret=credentials["client_secret"],
	password=credentials["password"],
	user_agent=credentials["user_agent"],
	username=credentials["username"]
)
_ = 0
commenttotype = """### This comments author looks like a bot to me
Im not sure though

Suspicion level = textherelollul

^Im ^a ^bot ^and ^you ^can ^improve ^me ^by ^opening ^issues ^in ^Github

[^^My ^^source ^^code ](https://github.com/balyedi/botfinder-reddit)"""

def sortFunc(e):
	return e.created_utc
suslevel = 0 # x percent sure its a bot
commentifslvl = 30 # if suslevel is more than x percent,comment about it.
attempts = 0
attemptslimit = len(bcomment) 
while True:
	for comment in reddit.subreddit("all").comments(limit=40): # get last 1000 comments
		author = comment.author
		if author.is_mod == False: # lets dont make mods angry :)
			print(comment.body)
			createdin = author.created_utc
			print("checking the comment if it contains one of the blacklisted comments...")
			for listline in bcomment:
				if comment.body == listline:
					suslevel = 20
					print(f"suslevel: {suslevel}")
					print("checking creation date and first comments date...")
					if author.created_utc < 1638476222:
						comment_list = []
						i = 0
						for comment in reddit.redditor(author.name).comments.new(limit=None):
							comment_list.append(comment)
							comment_list.sort(key=sortFunc)
							if math.fabs(author.created_utc-comment_list[0].created_utc) > 46849486:
								suslevel = suslevel + 30
								if suslevel > commentifslvl: # if suspicion is larger than the limit,reply about this
									comment.reply(commenttotype.replace("textherelollul",str(suslevel)))
									suslevel = 0
									break
				else:
					attempts = attempts + 1
					if attempts == attemptslimit:
						attempts = 0
						break
			if suslevel > commentifslvl:
				comment.reply(commenttotype.replace("textherelollul",str(suslevel)))
				suslevel = 0
				continue

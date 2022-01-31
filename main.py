import praw,json

f = open("credentials.json","r")
credentialsraw = f.read()
credentials = json.loads(credentialsraw)

reddit = praw.Reddit(
	client_id=credentials["client_id"],
	client_secret=credentials["client_secret"],
	password=credentials["password"],
	user_agent=credentials["user_agent"],
	username=credentials["username"]
)

print(reddit.user.me())

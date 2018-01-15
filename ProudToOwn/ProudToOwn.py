import praw
import time

numberOfReplys = 0
commentCount = 0

print("Logging in...")
r = praw.Reddit(client_id='',
                     client_secret='',
                     password='',
                     user_agent='',
                     username='')  #todo
print(r.user.me())

print("Grabbing subreddit...\n")
subreddit = r.subreddit("suns")

lines_to_match = ["three pointer", "three-pointer", "3 pointer", "3-pointer", "three pointers", "three-pointers", "3 pointers", "3-pointers"]

cache = []
commentsTracker = []

def run_bot():
    global numberOfReplys
    global commentCount

    print("Grabbing comments...")
    comments = subreddit.comments(limit=30)

    firsttime = False

    for comment in comments:
        comment_text = comment.body
        comment_textlower = comment.body.lower()
        author = comment.author
        #print(comment_text)

        for string in lines_to_match:
            if string in comment_textlower:
                startIdx = comment_textlower.find(string)
                endIdx = startIdx + len(string)
                quoted = comment_text[startIdx:endIdx]

        isMatch = any(string in comment_textlower for string in lines_to_match)

        if comment.id not in commentsTracker:
            commentsTracker.append(comment.id)
            commentCount = commentCount + 1

        if comment.id not in cache and isMatch and author.name != "INSERT USERNAME": #todo
            cache.append(comment.id)
            print("Match Found! Comment ID: " + comment.id)
            print(comment_text)
            try:
                comment.reply(">" + quoted + "\n\nProud to own the three point zone. Fulton Homes donates $100 to Suns charities")
                print("Reply successful!")
                numberOfReplys = numberOfReplys + 1
            except praw.exceptions.APIException:
                print("Caught Exception")
                pass


    print("Replied " + str(numberOfReplys) + " times")
    print("Comments viewed: " + str(commentCount) + "\n")

while True:
    run_bot()
    time.sleep(10)
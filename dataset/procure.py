import praw
import os
import pandas as pd
import datetime

def setUp(usrnm, passwd, cl_id, cl_sc):
    print('Getting Reddit Data...')
    reddit = praw.Reddit(client_id=cl_id, client_secret=cl_sc, user_agent='reddit_back', username=usrnm, password=passwd)

    return reddit

def firstTimeLinux():
    file_path = '/home/' + os.environ.get('USER') + '/'
    file = open(file_path + "_rb.dat", "w")
    file.write("Ran" + "\n")
    client_id = input('Please enter your Client ID:\t')
    client_secret = input('Please enter your Client Secret:\t')
    username = input('Please enter your Reddit Username:\t')
    password = input('Please enter your Reddit Password:\t')
    file.write(client_id + "\n")
    file.write(client_secret + "\n")
    file.write(username + "\n")
    file.write(password + "\n")
    file.close()

def extractData(reddit):
    reddit.read_only = True
    subreddit = reddit.subreddit('india')

    flairs = ["Politics",
            "Non-Political",
            "[R]eddiquette",
            "AskIndia",
            "Policy/Economy",
            "Business/Finance",
            "Science/Technology",
            "Scheduled",
            "Sports",
            "Food",
            "AMA",
            "Photography",
            "CAA-NRC-NPR",
            "Coronavirus"]

    topics = { "author":[],
                    "body":[],
                    "comments":[],
                    "comms_num":[],
                    "flair": [],
                    "id": [],
                    "score":[],
                    "title": [],
                    "url": [],
                    "created":[]}
    print('Collecting Flair Data...')
    flair_count = 1
    for flair in flairs:
        submissions = subreddit.search(flair, limit=100)
        for submission in submissions:
            
            topics["flair"].append(flair)
            topics["title"].append(submission.title)
            topics["score"].append(submission.score)
            topics["id"].append(submission.id)
            topics["url"].append(submission.url)
            topics["comms_num"].append(submission.num_comments)
            topics["created"].append(submission.created)
            topics["body"].append(submission.selftext)
            topics["author"].append(submission.author)
            
            #   Remove comments that are accessed by clicking on More Comments, limit = 0 implies no clicking
            submission.comments.replace_more(limit=0)
            comment = ''
            #   Only using top level comments
            for top_level_comment in submission.comments:
                comment = comment + ' ' + top_level_comment.body
            topics["comments"].append(comment)
        print('Collected flair: ',flair_count,' ',flair,' out of 12')
        flair_count = flair_count + 1

    topics_df = pd.DataFrame(topics)
    #   The created time is in Unix Time, convert it to timestamp before proceding
    print('Done Collecting Data, writing as csv')
    topics_df.to_csv('dataset.csv', index=False)

if __name__ == "__main__":
    file_path = '/home/' + os.environ.get('USER') + '/'
    client_id = ''
    client_secret = ''
    username = ''
    password = ''
    if os.path.isfile(file_path + "_rb.dat"):
        #	If the file exists, meaning it has already been set up
        file = open(file_path + "_rb.dat", "r")
        lines = file.readlines()
        client_id = lines[1].strip()
        client_secret = lines[2].strip()
        username = lines[3].strip()
        password = lines[4].strip()
        file.close()

        #	Setting up reddit, :
        reddit = setUp(username, password, client_id, client_secret)
        #   Main functon here:
        extractData(reddit)
        print('Done')
    else:
        if os.environ.get("DESKTOP_SESSION") in ["ubuntu", "gnome", "unity", "mate", "cinnamon"]:
            firstTimeLinux()
        print('Username and Password are all set!')
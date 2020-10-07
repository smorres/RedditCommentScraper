import requests
import json
import datetime
import csv

r = requests.get('https://www.reddit.com/r/worldnews/.json', headers = {'User-agent': 'Chrome'})

#returns a list of posts in the subreddit above
def reddit_posts():
    def get_posts():
        for post in r.json()['data']['children']:
            x = post['data']['title']
            yield(x)
    new_posts = get_posts() #returns generator object
    #print(new_posts)
    reddit_post = list(new_posts)
    #print(reddit_post)
    return(reddit_post)
#reddit_posts()

#print("\n\nreddit post:" + str(reddit_post))
#returns a list of URLs from the articles in each post
def get_links():
    def get_urls():
        for post in r.json()['data']['children']:
            y = post['data']['url']
            yield(y)
    new_urls = get_urls()
    url_list = list(new_urls)
    #print('\nGetting List of article URLs:\n\n'+str(url_list))
    return(url_list)

def get_permalinks():
    def get_perma():
        for post in r.json()['data']['children']:
            y = post['data']['permalink']
            yield(y)
    new_urls = get_perma()

    url_list = list(new_urls)
    #print(url_list)
    return(url_list)

#attempting to get a list of comments within each post, only able to currently get the top comment
def reddit_comments(index):
    current_post = get_permalinks()
    link = str('https://www.reddit.com'+current_post[index]+".json")
    new_post = requests.get(link, headers = {'User-agent': 'Chrome'})
    print("\n\nThis is num comments:\n"+str(new_post.json()[0]['data']['children'][0]['data']['num_comments']))
    def get_comments():
        for post in new_post.json():
            try:
                i=0
                if new_post.json()[0]['data']['children'][0]['data']['num_comments'] > 100:
                    while i < 100:
                        x = post['data']['children'][i]['data']['body']
                        i+=1
                        yield(x)
                else:
                    while i < new_post.json()[0]['data']['children'][0]['data']['num_comments']:
                        x = post['data']['children'][i]['data']['body']
                        i+=1
                        yield(x)
            except KeyError:
                continue
                
    new_comments = get_comments() #returns generator object
    comment_list = list(new_comments)
    #print("\n\nthis is the comment list:\n"+str(comment_list)+"\n\n")
    return(comment_list)
    
#reddit_comments()

#print(r.json()['data']['children'][0]['data']['body'])

post_list = reddit_posts()
target_word = 'Trump' #getting all post titles containing the 'target_word'
  
# using list comprehension  
# to get string with substring  
target_articles = [i for i in post_list if target_word in i] 
#print('\nGetting Post Titles Mentioning The Target Word:\n\n'+str(target_articles))

indexes = 0
post_indexes = []
for title in target_articles:
    post_indexes.append(post_list.index(target_articles[indexes]))
    indexes+=1
#print("\nGetting post indexes:\n\n" + str(post_indexes))
#We have the index of the post, get the URL

#get comments from required post

for index in post_indexes:
    print("\n\n\n\nHERE ARE THE REQUIRED COMMENTS FROM POSTS MENTIONING '", target_word,  "' (no more than 100 comments):\n\n")
    top_100_comments = reddit_comments(index)
    print("\n\n"+str(top_100_comments))

""""
url_list = get_links()
link_list = []
indexes = 0
for index in post_indexes:
    link_list.append(url_list[post_indexes[indexes]]) #returns links to origional articles
    indexes+=1
print("\nGetting Links: \n\n"+str(link_list))
"""

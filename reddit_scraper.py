import requests
import json
import datetime
import csv

r = requests.get('https://www.reddit.com/r/usanews/.json', headers = {'User-agent': 'Chrome'})

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
    print('\nGetting List of article URLs:\n\n'+str(url_list))
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
    print("\n\nNumber of comments:\n"+str(new_post.json()[0]['data']['children'][0]['data']['num_comments']))
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
    if comment_list != []:
        return(comment_list)
    else:
        print("\n\nNO COMMENTS\n\n")
        return(None)
    
#reddit_comments()

#print(r.json()['data']['children'][0]['data']['body'])
def main():
    post_list = reddit_posts()
    target_word_1 = 'Trump' #getting all post titles containing the 'target_word'
    target_word_2 = 'Biden'
    # using list comprehension  
    # to get string with substring  
    target_articles_1 = [i for i in post_list if target_word_1 in i] 
    target_articles_2 = [i for i in post_list if target_word_2 in i] 
    print('\nNumber of Post Titles Mentioning Trump:\n\n',len(target_articles_1),"\n")
    print('\nNumber of Post Titles Mentioning Biden:\n\n',len(target_articles_2),"\n")

    
    post_indexes_trump = []
    post_indexes_biden = []
    if len(target_articles_1) != 0:
        indexes = 0
        for title in target_articles_1:
            post_indexes_trump.append(post_list.index(target_articles_1[indexes]))
            indexes+=1
        indexes = 0
        for index in post_indexes_trump:
            print("\n\nHERE ARE THE REQUIRED COMMENTS FROM ARTICLE '", target_articles_1[indexes],  "' (no more than 100 comments):\n\n")
            top_100_comments = reddit_comments(index)
            print("\n\nComments: "+str(top_100_comments))
            print("\n\n==================================================")
    else:
        print("\n\nNO CURRENT ARTICLES MENTIONING TRUMP")
    
    if len(target_articles_2) != 0:
        indexes = 0
        for title in target_articles_2:
            post_indexes_biden.append(post_list.index(target_articles_2[indexes]))
            indexes+=1
        indexes = 0
        for index in post_indexes_biden:
            print("\n\nHERE ARE THE REQUIRED COMMENTS FROM POSTS MENTIONING '", target_articles_2[indexes],  "' (no more than 100 comments):\n\n")
            print(str(reddit_posts()))
            top_100_comments = reddit_comments(index)
            print("\n\nComments: "+str(top_100_comments))
            print("\n\n==================================================")

    else:
        print("\n\nNO CURRENT ARTICLES MENTIONING BIDEN")
    
    """"
    url_list = get_links()
    link_list = []
    indexes = 0
    for index in post_indexes:
        link_list.append(url_list[post_indexes[indexes]]) #returns links to origional articles
        indexes+=1
    print("\nGetting Links: \n\n"+str(link_list))





    with open("rawcommentdata.txt", "w") as text_file:
        text_file.write(str(top_100_comments))
    main()


    """
main()

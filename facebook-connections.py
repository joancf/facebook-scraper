import os, datetime, time, csv, threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from tkinter import *

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()



        self.Mutual = Button(frame, text="push befor start  to expand to all friends", command=self.mutual)
        self.Mutual.pack(side=LEFT)
        self.hi_there = Button(frame, text="push after login", command=self.say_hi)
        self.hi_there.pack(side=LEFT)   
        self.stop = Button(frame, text="STOP and Save", fg="red", command=self.stop)
        self.stop.pack(side=LEFT)
 
        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)
    def handle_my_custom_event(event):
        frame.quit

 
    def say_hi(self):
        def callback():
            friends=scrape_1st_degrees()
            scrape_friends(friends)
        t = threading.Thread(target=callback)
        t.start()

        

    def mutual(self):
        global mutualOnly
        mutualOnly=0

    def stop(self):
        global stop
        stop=True

# --------------- Ask user to log in -----------------
def fb_login():
    print("Opening browser...")
    browser.get("https://www.facebook.com/")

# --------------- Scroll to bottom of page -----------------
def scroll_to_bottom():
    print("Scrolling to bottom...")
    last_height=-1
    sleeps=0
    while True:
            # if bowser does not grow for a minute also break
            height = browser.execute_script("return document.body.scrollHeight")
            if  last_height == height :
                print("%d steps, Blocked! at size %d" % (sleeps, last_height))
                if  sleeps >100 :   #25 seconds 
                    break
            last_height = height
            try:
                browser.find_element_by_class_name('_4khu') # class after friend's list
                print("Reached end!")
                break
            except:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.25)
                sleeps+=1
                pass

# --------------- Get list of all friends on page ---------------
def scan_friends():
    global userName    
    friends = []
    try:
        userName=browser.find_element_by_id("fb-timeline-cover-name").text
        print('Scanning page '+ userName +' for friends...')
    except:
        print('Error when Scanning page username for friends...')
    friend_cards = browser.find_elements_by_xpath('//div[@id="pagelet_timeline_medley_friends"]//div[@class="fsl fwb fcb"]/a')
    for friend in friend_cards:
        if friend.get_attribute('data-hovercard') is None:
            # print(" %s (INACTIVE)" % friend.text)
            friend_id = friend.get_attribute('ajaxify').split('id=')[1]
            friend_active = 0
        else:
            # print(" %s" % friend.text)
            friend_id = friend.get_attribute('data-hovercard').split('id=')[1].split('&')[0]
            friend_active = 1

        friends.append({
            'name': friend.text.encode('ascii', 'ignore').decode('ascii'), #to prevent CSV writing issues
            'id': friend_id,
            'active': friend_active
            })

    print('Found %r friends on page!' % len(friends))
    return friends


# --------------- Scrape 1st degree connections ---------------
def scrape_1st_degrees():
    global user
    global userId
 
    #Get your unique Facebook ID
    profile_icon = browser.find_element_by_css_selector("[data-click='profile_icon'] > a > span > img")
    myid = profile_icon.get_attribute("id")[19:]

    #Scan your Friends page (1st-degree connections)
    print("Opening Friends page...")
    browser.get("https://www.facebook.com/" + myid + "/friends")
    scroll_to_bottom()
    myfriends = scan_friends()
    friends={}
    #Write connections to CSV File
    for friend in myfriends:
        friends[friend['id']]=friend['name']
        edges.append([myid,friend['id']])
    user=userName
    userId=myid
    return friends



# --------------- Scrape 2nd degree connections. ---------------
#This can take several days if you have a lot of friends!!
def scrape_friends(friends):
    global stop
    idx=1
    myfriends=list(friends.keys())
    for friend in myfriends :
        if stop:
            break
        #Load URL of friend's friend page
        if mutualOnly is "0" :
            scrape_url = "https://www.facebook.com/"+ friend + "/friends?source_ref=pb_friends_tl"
        else:
            scrape_url = "https://www.facebook.com/"+ friend + "/friends_mutual?source_ref=pb_friends_tl"
        browser.get(scrape_url)

        #Scan your friends' Friends page (2nd-degree connections)
        idx+=1 
        print("%d) %s" % (idx, friends[friend]+"--"+ scrape_url))
        if idx>4:
            break
        scroll_to_bottom()
        their_friends = scan_friends()

        #Write connections to CSV File
        print('Writing connections to CSV...')
        for person in their_friends:
            #if only mutual no new friends
            if (person['id'] in friends) or mutualOnly is "0" :
                friends[person['id']]=person['name']
                edges.append([person['id'],friend  ])
    print ('Saving file friends.gdf...')
    f = open(user+"_connections.gdf","w",encoding="utf8")
    f.write("nodedef> name ,label\n")
    f.write(userId+ ","+user+"\n")
    for friend in friends :
        f.write(friend+',"'+friends[friend]+'"\n')
    f.write("edgedef> node1,node2 \n")   
    for edge in edges:
        f.write(edge[0]+","+edge[1]+"\n")
    f.close()
    print ('Saved!')

# --------------- Start Scraping ---------------

# Configure browser session
wd_options = Options()
wd_options.add_argument("--disable-notifications")
wd_options.add_argument("--disable-infobars")
wd_options.add_argument("--mute-audio")
browser = webdriver.Chrome(chrome_options=wd_options)
user=""
userName=""
userId=""
edges=[]
mutualOnly =1
stop=False
now = datetime.now()
fb_login()
root = Tk()


app = App(root)

root.mainloop()


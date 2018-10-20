# Facebook Scraper
This tool lets you download a GDF network

## Installation
You'll need to have python, pip, and Crhome Driver 

Once that's all set up:

1. Clone this repository
2. `cd` into the cloned folder 
4. Create a python enviornment 
3. `pip install -r requirements.txt`
4. Download chromedriver  https://sites.google.com/a/chromium.org/chromedriver/
5. Copy the cromedriver into the bin folder of your environment

I ran it using python 3.5.2

## Get GDF of connections & IDs
Getting your list of friends is no longer possible via the Facebook Graph API, so you can use this. It has 2 modes:
1) Download a list of your connections, and 
2) Download a list of your 2nd-degree connections for social network analysis. You can choose between downloading mutual friends or al 2n-degree friends 
3) Save data to a GDF file

### Get your 2n-degree network connections (your friends' friends)
Note: This could take days if you have lots of friends!

1a. Run ```python facebook-connections.py 0```,  to get all of your friends' friends .
1b. Run ```python facebook-connections.py 0```,  to get only your friends' mutual friends .
2. A browser window will open. Fill out your username & password and log in.
3. Press Enter in the terminal after logging in.
4. You should the script looping through your Facebook friends' friend pages.
5. A GDF file will be created with the data (your_name_connections.gdf)

**Note**: This currently may get tripped up by in some situations, because the scroll_to_bottom() function doesn't accurately detect when it's at the bottom of the friends list. Please feel free to improve with a pull request!

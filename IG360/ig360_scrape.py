from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from .utility_methods.utility_methods import *
from .utility_methods.json_methods import *
from .utility_methods.analysis_methods import *
from random import randint
import pandas as pd

import time
import os

class IG360Scrape:

    def __init__(self, config, username="", password=""):
        """Creates an instance of the IG360 Scrape class

        Creates an instance of the IG360 Scrape class.  IG360 uses Selenium and Google Chrome to login to 
        Instagram, collect profile/post/follower data and output as JSON data

        Args:
            config (str): Location of the configuration file (config.ini)
            username (str): Instagram account login.  If not specified then value in config.ini is used
            password (str): Instagram account password.  If not specified then value in config.ini is used
        """
        # set user name and password
        if (len(username) > 0):
            self.username = username
            self.password = password
        else:
            self.username = config['IG_AUTH']['USERNAME']
            self.password = config['IG_AUTH']['PASSWORD']
        
        # set other attributes
        self.code_version = 0.9
        self.simple_stopwords = ['a', 'the', 'if', 'then', 'what', 'where', 'why', 'who', 'who', 'whom']
        self.url_login = config['IG_URLS']['URL_LOGIN']
        self.url_post = config['IG_URLS']['URL_POST']
        self.url_user = config['IG_URLS']['URL_USER']
        self.url_tag = config['IG_URLS']['URL_TAG']
        self.selenium_driver_path = config['ENVIRONMENT']['CHROMEDRIVER_PATH']
        self.logged_in = False
        self.record_profile = dict()
        self.record_post = dict()
        self.record_post_list = []
        self.record_follower_list = []
        self.record_following_list = []
        

    @insta_method
    def login(self):
        """Logs into Instagram

        Logs into Instgram using the credentials specified when the IG360 object was created
        """
        # open url
        self.driver = webdriver.Chrome(self.selenium_driver_path)
        self.driver.get(self.url_login)
        time.sleep(5)

        # find elements
        btn_login = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]')
        input_user = self.driver.find_element_by_name('username')
        input_pass = self.driver.find_element_by_name('password')

        # action: enter user/pass, click login button
        input_user.send_keys(self.username)
        input_pass.send_keys(self.password)
        btn_login.click()


    def __inifinite_expand_comments(self):
        """Expand the comment section of a post

        Expands the comment section of a post so that more posts can be scraped.
        This is an internal routine, meant to be called by other routines

        Returns:
            bool: True if there are no more comments to expand, else false   
        """
        btn_exp = self.driver.find_elements_by_xpath("//button[@class='dCJp8 afkep']")

        if len(btn_exp) > 0:
            btn_exp[0].click()
            return False
            
        return True



    def __pop_scrape(self, cnt_tab_focus, scrape_element, scrape_class, scrape_subdiv='', scrape_extract='text'):
        """Scrape all html elements of a specified class from an Instagram pop up window

        Scrape all html elements of a specified class from an Instagram pop up window. Designed to be used with followers or users followed.

        Args:
            cnt_tab_focus (int): number of times to hit the tab key to get focus before attempting to scroll pop-up window
            scrape_element (str): HTML element type to be targeted for scraping
            scrape_class (str): Class name within element to be targeted for scraping

        Returns:
            list: all the items (as defined by input class) that can be found in the pop up window   
        """
        popup_list = []
        finished = False
        prev_list_len = 0

        #   process pop up window elements
        while not finished:
            # scroll down
            tactions = ActionChains(self.driver)
            tactions.send_keys(Keys.TAB)
            for i in range (cnt_tab_focus):
                tactions.perform()
                time.sleep(1)
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.END)
            actions.perform()
            time.sleep(randint(3,8))

            # extract target elements within views, add to list
            new_elements = self.driver.find_elements_by_xpath("//{}[@class='{}']{}".format(scrape_element, scrape_class, scrape_subdiv))
            eval("popup_list.extend(i." + scrape_extract + " for i in new_elements)")

            # de-duplicate target list
            popup_list = list(set(popup_list))
 
            # check if done / refresh
            if len(popup_list) == prev_list_len:
                finished = True
                return popup_list
            else:
                prev_list_len = len(popup_list)


    @insta_method
    def __nav_user(self, user):
        """Navigate to a user's profile page

        Navigate to a user's profile page. 

        Args:
            user (str): Instagram account user name
        """
        loaded = False
        while loaded == False:
            self.driver.get(self.url_user.format(user))
            txt_404 = self.driver.find_elements_by_xpath('//*[@class=" p-error dialog-404"]')
            if len(txt_404) == 0:
                loaded = True
                time.sleep(randint(5,8))
            else:
                wait_time = randint(600,900)
                print("404 Returned. Waiting {} seconds...".format(wait_time))
                time.sleep(wait_time)



    @insta_method
    def __nav_post(self, picture_id):
        """Navigate to a post page

       Navigate to a post page

        Args:
            picture_id (str): Intagram Post ID
        """
        loaded = False
        while loaded == False:
            self.driver.get(self.url_post.format(picture_id))
            txt_404 = self.driver.find_elements_by_xpath('//*[@class=" p-error dialog-404"]')
            if len(txt_404) == 0:
                loaded = True
                time.sleep(randint(5,8))
            else:
                wait_time = randint(600,900)
                print("404 Returned. Waiting {} seconds...".format(wait_time))
                
                time.sleep(wait_time)


    @insta_method
    def scrape_followers(self, user):
        """Get list of followers for a specified user

        Get list of followers for a specified user

        Args:
            user (str): Instagram account user name
        """
        # navigate to user's profile page, click on followers link
        self.__nav_user(user)
        self.driver.find_element_by_xpath("//a[@class='-nal3 ']").click()
        time.sleep(randint(7,10))

   

        # capture full list of followers from pop-up window
        cnt_tab_focus = 3
        scrape_element = 'a'
        scrape_class = 'FPmhX notranslate  _0imsa '
        ext_followers = self.__pop_scrape(cnt_tab_focus, scrape_element, scrape_class)

        # update profile record
        self.record_follower_list = ext_followers


    @insta_method
    def scrape_following(self, user):
        """Get list of accounts a specified user is following

        Get list of accounts a specified user is following

        Args:
            user (str): Instagram account user name
        """
        # navigate to user's profile page, click on followers link
        self.__nav_user(user)
        self.driver.find_elements_by_xpath("//a[@class='-nal3 ']")[1].click()
        time.sleep(randint(7,10))

        # capture full list of followers from pop-up window
        cnt_tab_focus = 4
        scrape_element = 'a'
        scrape_class = 'FPmhX notranslate  _0imsa '
        ext_following = self.__pop_scrape(cnt_tab_focus, scrape_element, scrape_class)

        # update profile record
        self.record_following_list = ext_following  


    @insta_method
    def scrape_profile(self, user):
        """Get profile for a specified user

        Get profile for a specified user

        Args:
            user (str): Instagram account user name
        """
        # navigate to user's profile page
        self.__nav_user(user)
        
        # find elements
        txt_user_name = self.driver.find_element_by_xpath('//*[@class="_7UhW9       fKFbl yUEEX   KV-D4             fDxYl     "]')
        txt_verified = self.driver.find_elements_by_xpath('//*[@title="Verified"]')
        txt_posts = self.driver.find_elements_by_xpath('//span[@class="g47SY "]')[0]
        txt_followers = self.driver.find_elements_by_xpath('//span[@class="g47SY "]')[1]
        txt_following = self.driver.find_elements_by_xpath('//span[@class="g47SY "]')[2]
        txt_full_name = self.driver.find_elements_by_xpath('//h1[@class="rhpdm"]')
        txt_description = self.driver.find_elements_by_xpath('//div[@class="-vDIg"]/span')

        # extract text values
        ext_user_name = txt_user_name.text
        ext_verified = min(len(txt_verified),1)
        ext_posts = int(txt_posts.text.replace(',',''))
        ext_followers = int(txt_followers.get_attribute("title").replace(',',''))
        ext_following = int(txt_following.text.replace(',',''))
        if len(txt_full_name) > 0:
            ext_full_name = txt_full_name[0].text
        else:
            ext_full_name = ''
        if len(txt_description) > 0:
            ext_description = txt_description[0].text
        else:
            ext_description = ''     

        # Update profile record
        self.record_profile = {
            'user_name' : ext_user_name,
            'ind_verified' : ext_verified,
            'num_posts' : ext_posts,
            'num_followers' : ext_followers,
            'num_following' : ext_following,
            'full_name' : ext_full_name,
            'description' : ext_description
        }


    @insta_method
    def scrape_post(self, picture_id, get_likes=True):
        """Extract details of an instagram post

        Extract details of an instagram post

        Args:
            url_post (str): URL to direct instagram post
            get_likes (boolean, optional): Determine whether to scrape likes (time-consuming)
        """       
        # navigate to post URL
        self.__nav_post(picture_id)

        # expand to see all comments
        ind_all_comments = False
        while ind_all_comments == False:
            ind_all_comments = self.__inifinite_expand_comments()
            time.sleep(3)

        # find main post elements
        sl_location = self.driver.find_elements_by_class_name("O4GlU")
        sl_post = self.driver.find_element_by_class_name("EtaWk")
        sl_poster = self.driver.find_elements_by_xpath("//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")
        sl_likes = self.driver.find_elements_by_xpath("//button[@class='sqdOP yWX7d     _8A5w5    ']/span")
        sl_postDate = self.driver.find_elements_by_xpath("//time[@class='_1o9PC Nzb55']")

        # extract name, location, comments, date
        if len(sl_location) > 0:
            ext_location = sl_location[0].text
        else:
            ext_location = ''
        if len(sl_poster) > 0:
            ext_poster = sl_poster[0].text
        else:
            ext_poster = '-1' 
        if len(sl_likes) > 0:
            ext_likes = sl_likes[0].text
        else:
            ext_likes = '-1'           
        post_user_header = sl_post.text[0:sl_post.text.find('\n')+1]
        ext_post = sl_post.text.replace(post_user_header,'')
        post_date = sl_postDate[0].get_attribute("datetime")

        # click like button and scrape likes
        ext_like_list = []
        if get_likes:
            btn_likes = self.driver.find_elements_by_xpath("//button[@class='sqdOP yWX7d     _8A5w5    ']")
            if len(btn_likes) > 0:
                btn_likes[0].click()
                time.sleep(randint(7,10))

                # capture full list of followers from pop-up window
                cnt_tab_focus = 2
                scrape_element = 'div'
                scrape_class = '_7UhW9   xLCgt      MMzan  KV-D4             fDxYl     '
                scrape_subdiv = '/a'
                scrape_extract = "get_attribute('title')"
                ext_like_list = self.__pop_scrape(cnt_tab_focus, scrape_element, scrape_class, scrape_subdiv, scrape_extract)

        # update post record
        self.record_post = {
            'picture_id': picture_id,
            'post_date': post_date,
            'poster': ext_poster,
            'location': ext_location,
            'likes' : ext_likes,
            'post': ext_post,
            'like_list' : ext_like_list
        }


    @insta_method
    def scrape_post_list(self, user, max_pics):
        """Extracts URLs for most recent posts on an IG user's home page

        Extracts URLs for most recent posts on an IG user's home page

        Args:
            user (str): Instagram account user name
            max_pics (int): Maximum number of URL's 
        """
        #navigate to user's profile page
        self.__nav_user(user)

        post_list = []
        finished = False
        prev_list_len = 0
        while not finished:
            # scroll down
            self.driver.find_element_by_tag_name("html").send_keys(Keys.END)
            time.sleep(randint(3,8))

            # extract target elements within views, add to list
            imgs = self.driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']")
            for img in imgs:
                specialPix = img.find_elements_by_class_name("u7YqG")
                if (len(specialPix) == 0):
                    txtNewURL = img.find_element_by_tag_name("a").get_attribute('href')
                    if txtNewURL not in post_list:
                        post_list.append(txtNewURL)
                else:
                    if (specialPix[0].find_element_by_tag_name("span").get_attribute('aria-label') in ['IGTV','Video']) == False:
                        txtNewURL = img.find_element_by_tag_name("a").get_attribute('href')
                        if txtNewURL not in post_list:
                            post_list.append(txtNewURL)

            # check if done / refresh
            if len(post_list) >= max_pics:
                finished = True
            if finished == False:
                if len(post_list) <= prev_list_len:
                    finished = True
                else:
                    prev_list_len = len(post_list)

        # update post list record
        if len(post_list) < max_pics:
            self.record_post_list = post_list
        else: 
            self.record_post_list = post_list[:max_pics]


    def get_user_lists(self):
        return util_get_user_lists(self.record_follower_list, self.record_following_list)


    def get_user_part_lists(self):
        return util_get_user_part_lists(self.record_follower_list, self.record_following_list)


    def get_posts(self):
        return util_get_posts(self.record_post_list)


    def get_profile_data(self):
        return util_get_profile_data(self.record_profile)


    def get_post_data(self):
        return util_get_post_data(self.record_post)


    def parse_post(self, raw_post):
        """Parse post data 

        Parse post data to extract summary and detail information -
            -Total number of words in the post
            -Number of non-hashtag words
            -Number of unique non-hashtag words
            -List of non-hashtag words that appear in post
            -List of instagram accounts that commented in post

        Args:
            raw_post (str): Instagram post contents (as extracted by method scrape_post)
        """
        return util_parse_post(raw_post, self.simple_stopwords)


    def json_write_fp(self, tgt_user, dir_output):
        """Write standardized Full Profile (FP) file

        Write standardized Full Profile (FP) file.  JSON file will output the following (previously extracted) information -
            -Base information (number of posts, full name, etc)
            -Accounts following target account
            -Accounts that target account follows
            -URL's for target account's most recent posts

        Args:
            tgt_user (str): Instagram target account user name
            dir_output (str): Output directory for JSON files
        """
        return util_json_write_fp(tgt_user, dir_output, self.record_follower_list, self.record_following_list, self.record_post_list, self.code_version, self.record_profile)
 

    def json_write_ps(self, tgt_user, dir_output, src_fp_file, post_data):
        """Write standardized Post Details (PS) file

        Write standardized Post Details (PS) file.  JSON file will output the following (previously extracted) information -
            -Post contents, comments, list of likers

        Args:
            tgt_user (str): Instagram target account user name
            dir_output (str): Output directory for JSON files
            src_fp_file (str): Filename for Standardized Profile (FP) file.  Assumed to be located in directory specified by dir_output
            post_data (str): List of instagram post data (as extracted with the scrape_post method)
        """
        return util_json_write_ps(tgt_user, dir_output, src_fp_file, post_data, self.code_version)
       

    def util_json_write_mp(self, tgt_user, dir_output, profiles):
        """Write standardized Multi-Profile (MP) file

        This is a utility function, meant to be called by the instance method json_write_fp.
        Write standardized Multi-Profile (MP) file.  JSON file will output the following (previously extracted) information -
            -Base profile data (user name, verification status, numer of posts, number of followers, number followed, full name, description)
            -Date of user's most recent post

        Args:
            tgt_user (str): Instagram target account user name
            dir_output (str): Output directory for JSON files
            code_version (float): IG360 instance variable.  Code version
            profiles (list): Profile data records.  (previously extracted) Fields should be as follows -
                user_name (str)
                ind_verified (int) 
                num_posts (int)
                num_followers (int)
                num_following (int)
                full_name (string)
                description (string)
                dt_last_post (string: '%Y-%m-%dT%H:%M:%SZ')
        """
        util_json_write_mp(tgt_user, dir_output, self.code_version, profiles)


# -----------------------------------------------------------
# QA --- this will run automatically if being called directly
# -----------------------------------------------------------

if __name__ == '__main__':

    config_file_path = 'config.ini'
    config = init_config(config_file_path)
    # login
    scraper = IG360Scrape(config)
    scraper.login()

    # scrape a profile
    #scraper.scrape_profile("alsaydali")
    #print(scraper.record_profile)

    # scrape a post
    scraper.scrape_post('B9o71NFB3sN')
    print("{}".format(scraper.record_post))
 
    # get list of posts to process
    #scraper.scrape_post_list("ghost.acolyte.v2", 2)
    #print("Posts Found: {}".format(scraper.record_post_list))
    #print("Num Posts: {}".format(len(scraper.record_post_list)))

    # capture list of followers
    scraper.scrape_followers('alsaydali')
    print("Followers: {}".format(scraper.record_follower_list)) 

    #capture list of following
    #scraper.scrape_following('alsaydali')
    #print("Following: {}".format(scraper.record_following_list))
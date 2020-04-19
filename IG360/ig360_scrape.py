from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .utility_methods.utility_methods import *
from .utility_methods.json_methods import *
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
        self.code_version = 0.85
        self.url_login = config['IG_URLS']['URL_LOGIN']
        self.url_post = config['IG_URLS']['URL_POST']
        self.url_user = config['IG_URLS']['URL_USER']
        self.url_tag = config['IG_URLS']['URL_TAG']
        self.driver = webdriver.Chrome(config['ENVIRONMENT']['CHROMEDRIVER_PATH'])
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


    def __pop_scrape(self, scroll_class1, scroll_class2, scrape_element, scrape_class):
        """Scrape all html elements of a specified class from an Instagram pop up window

        Scrape all html elements of a specified class from an Instagram pop up window. Designed to be used with followers or users followed.

        Args:
            scroll_class1 (str): Primary class name within element to be targeted for scrolling
            scroll_class2 (str): Secondary class name within element to be targeted for scrolling
            scrape_element (str): HTML element type to be targeted for scraping
            scrape_class (str): Class name within element to be targeted for scraping

        Returns:
            list: all the items (as defined by input class) that can be found in the pop up window   
        """
        popup_list = []
        finished = False
        prev_list_len = 0
        while not finished:
            # scroll down
            self.driver.find_element_by_xpath("//div[@class='{}' or @class='{}']".format(scroll_class1, scroll_class2)).click()
            time.sleep(randint(1,3))
            self.driver.find_element_by_tag_name("html").send_keys(Keys.END)
            time.sleep(randint(3,8))

            # extract target elements within views, add to list
            new_elements = self.driver.find_elements_by_xpath("//{}[@class='{}']".format(scrape_element, scrape_class))
            popup_list.extend(i.text for i in new_elements)

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
        self.driver.get(self.url_user.format(user))
        time.sleep(randint(5,8))


    @insta_method
    def __nav_post(self, picture_id):
        """Navigate to a post page

       Navigate to a post page

        Args:
            picture_id (str): Intagram Post ID
        """
        self.driver.get(self.url_post.format(picture_id))
        time.sleep(randint(3,5))


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
        time.sleep(randint(3,6))

        # capture full list of followers from pop-up window
        scroll_class1 = '_7UhW9   xLCgt      MMzan   _0PwGv           fDxYl     '
        scroll_class2 = 'wFPL8 '
        scrape_element = 'a'
        scrape_class = 'FPmhX notranslate  _0imsa '
        ext_followers = self.__pop_scrape(scroll_class1, scroll_class2, scrape_element, scrape_class)

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
        time.sleep(randint(3,6))

        # capture full list of followers from pop-up window
        scroll_class1 = '_7UhW9   xLCgt      MMzan   _0PwGv           fDxYl     '
        scroll_class2 = 'wFPL8 '
        scrape_element = 'a'
        scrape_class = 'FPmhX notranslate  _0imsa '
        ext_following = self.__pop_scrape(scroll_class1, scroll_class2, scrape_element, scrape_class)

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
        txt_user_name = self.driver.find_element_by_xpath('//h2[@class="_7UhW9       fKFbl yUEEX   KV-D4            fDxYl     "]')
        txt_verified = self.driver.find_elements_by_xpath('//*[@title="Verified"]')
        txt_posts = self.driver.find_elements_by_xpath('//span[@class="g47SY "]')[0]
        txt_followers = self.driver.find_elements_by_xpath('//span[@class="g47SY "]')[1]
        txt_following = self.driver.find_elements_by_xpath('//span[@class="g47SY "]')[2]
        txt_full_name = self.driver.find_element_by_xpath('//h1[@class="rhpdm"]')
        txt_description = self.driver.find_element_by_xpath('//div[@class="-vDIg"]/span')

        # extract text values
        ext_user_name = txt_user_name.text
        ext_verified = min(len(txt_verified),1)
        ext_posts = int(txt_posts.text.replace(',',''))
        ext_followers = int(txt_followers.get_attribute("title").replace(',',''))
        ext_following = int(txt_following.text.replace(',',''))
        ext_full_name = txt_full_name.text
        ext_description = txt_description.text

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
    def scrape_post(self, picture_id):
        """Extract details of an instagram post

        Extract details of an instagram post

        Args:
            url_post (str): URL to direct instagram post
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
        btn_likes = self.driver.find_elements_by_xpath("//button[@class='sqdOP yWX7d     _8A5w5    ']")
        if len(btn_likes) > 0:
            btn_likes[0].click()
            time.sleep(3)
            self.driver.find_element_by_xpath("//div[@class='_7UhW9   xLCgt      MMzan   _0PwGv           fDxYl     ']").click()
            time.sleep(3)

            #capture likes until none left
            ext_like_list = []
            finished = False
            cnt_prev_list_len = 0
            while not finished:
                #scroll down
                self.driver.find_element_by_xpath("//div[@class='_7UhW9   xLCgt      MMzan   _0PwGv           fDxYl     ']").click()
                time.sleep(1)
                self.driver.find_element_by_tag_name("html").send_keys(Keys.END)
                time.sleep(3)
                
                #extract name for every like visible
                likepack = self.driver.find_elements_by_xpath("//div[@class='                   Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                                              ']")
                ext_like_list.extend(liker.text for liker in likepack)

                # clean up duplicates
                ext_like_list = list(set(ext_like_list))
 
                # check if done / refresh
                if len(ext_like_list) == cnt_prev_list_len:
                    finished = True
                else:
                    cnt_prev_list_len = len(ext_like_list)

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
            if len(post_list) > max_pics:
                finished = True
            if finished == False:
                if len(post_list) == prev_list_len:
                    finished = True
                    return post_list
                else:
                    prev_list_len = len(post_list)

        # update post list record
        self.record_post_list = post_list[:max_pics]


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
       



# -----------------------------------------------------------
# QA --- this will run automatically if being called directly
# -----------------------------------------------------------

if __name__ == '__main__':

    config_file_path = 'config.ini'
    config = init_config(config_file_path)
    # login
    #scraper = IG360Scrape(config)
    #scraper.login()

    # scrape a profile
    #scraper.scrape_profile("alsaydali")
    #print(scraper.record_profile)

    # scrape a post
    #scraper.scrape_post('B9ZPklXht6f')
    #print(scraper.record_post)

    # get list of posts to process
    #scraper.scrape_post_list("tonyrobbins", 2)
    #print("Posts Found: {}".format(scraper.record_post_list))
    #print("Num Posts: {}".format(len(scraper.record_post_list)))

    # capture list of followers
    #scraper.scrape_followers('alsaydali')
    #print("Followers: {}".format(scraper.record_follower_list))

    #capture list of following
    #scraper.scrape_following('alsaydali')
    #print("Following: {}".format(scraper.record_following_list))
   
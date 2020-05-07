import re


def util_get_user_lists(record_follower_list, record_following_list):
    return (record_follower_list, record_following_list)


def util_get_user_part_lists(record_follower_list, record_following_list):
    lst_both = list(set(record_follower_list).intersection(record_following_list))  
    lst_follower_only = list(set(record_follower_list) - set(lst_both))
    lst_folowing_only = list(set(record_following_list) - set(lst_both))
    return (lst_follower_only,lst_folowing_only,lst_both)


def util_get_posts(record_post_list):
    return record_post_list


def util_get_profile_data(record_profile):
    return (record_profile['user_name'],record_profile['ind_verified'],record_profile['num_posts']
            ,record_profile['num_followers'],record_profile['num_following'],record_profile['full_name'],record_profile['description'])


def util_get_post_data(record_post):
    return (record_post['picture_id'],record_post['post_date'],record_post['poster'],record_post['location']
        ,record_post['likes'],record_post['post'],record_post['like_list'])




def util_parse_post(raw_post, simple_stopwords):
    """Utility Function: Parse post data 

    This is a utility function, meant to be called by the instance method parse_post.
    Parse post data to extract summary and detail information -
        -Total number of words in the post
        -Number of non-hashtag words
        -Number of unique non-hashtag words
        -List of non-hashtag words that appear in post
        -List of instagram accounts that commented in post

    Args:
        raw_post (str): Instagram post contents (as extracted by method scrape_post)
        simple_stopwords (list:string): set of stop words to ignore when analyzing post contents
    """
    raw_post_split = re.split("\\n[0-9]+[mhdw]", raw_post)
    
    # extract words and tags
    lst_words = []
    lst_hashtags = []
    for w in raw_post_split[0].split():
        if w[0] == "#":
            lst_hashtags.append(w)
        else:
            if w not in simple_stopwords:
                w_clean = re.match("[a-zA-Z0-9_]+.*[a-zA-Z0-9_]", w)
                if w_clean != None:
                    lst_words.append(w_clean.group(0))
    
    # extract list of commenters
    commenter_list = []
    for comm in raw_post_split[1:]:
        commsec = re.split("\\n", comm)
        user_found = False
        for cphrase in commsec:
            if user_found == False:
                if (len(cphrase)>0) and (len(cphrase.split()) == 1) and  (cphrase not in ['Reply']):
                    commenter_list.append(cphrase)
                    user_found = True
    
    # assemble and output
    lst_words_dist = list(set(lst_words))
    lst_hashtags_dist = list(set(lst_hashtags))
    commenter_list_dist = list(set(commenter_list))
    return (len(lst_words+lst_hashtags), len(lst_words), len(lst_words_dist), lst_words_dist, len(lst_hashtags_dist), lst_hashtags_dist, commenter_list_dist)

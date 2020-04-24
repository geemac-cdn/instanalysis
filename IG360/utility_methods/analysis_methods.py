

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


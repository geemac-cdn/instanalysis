import pandas as pd
import datetime
import json
import re
from pathlib import Path


def util_json_write_fp(tgt_user, dir_output, record_follower_list, record_following_list, record_post_list, code_version, record_profile):
    """Utility Function: Write standardized Full Profile (FP) file

    This is a utility function, meant to be called by the instance method json_write_fp.
    Write standardized Full Profile (FP) file.  JSON file will output the following (previously extracted) information -
        -Base information (number of posts, full name, etc)
        -Accounts following target account
        -Accounts that target account follows
        -URL's for target account's most recent posts

    Args:
        tgt_user (str): Instagram target account user name
        dir_output (str): Output directory for JSON files
        record_follower_list (list[str]): IG360 instance variable.  Instagram accounts following the target account
        record_following_list (list[str]): IG360 instance variable.  Instagram accounts being followed by the target account
        record_post_list (list[str]): IG360 instance variable.  Most recent posts by the target account
        code_version (float): IG360 instance variable.  Code version.
        record_profile (dict): IG360 instance variable.  Dictionary of profile 
    """
    if Path.exists(dir_output):
        # combine follow lists into single dictionary
        dict_lists = {
            "followers" : record_follower_list,
            "user_follows" : record_following_list,
            "recent_posts" : record_post_list
        }

        # create header dictionary
        dt_run = datetime.datetime.now()
        dict_header = {
            "run_datetime" : dt_run.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "ig_record_type" : "fp",
            "code_version" : code_version
        }

        # combine all dictionaries
        dict_final = {**dict_header, **record_profile, **dict_lists}

        # output as JSON
        fn_out = re.sub(r'[\W]','',dict_header["ig_record_type"]) + '_' + tgt_user + '_' \
            + str(dt_run.year) + str(dt_run.month).zfill(2) + str(dt_run.day).zfill(2) + str(dt_run.hour).zfill(2) + str(dt_run.minute).zfill(2) + '.json'
        fn_out_full = dir_output / fn_out
        with open(fn_out_full, 'w') as json_file:
            json.dump(dict_final, json_file)

        # completion
        print("Output File: {}".format(fn_out_full))
        return [True,fn_out_full]
    else:
        return [False,""]


def util_json_write_ps(tgt_user, dir_output, src_fp_file, post_data, code_version):
    """Utility Function: Write standardized Post Details (PS) file

    This is a utility function, meant to be called by the instance method util_json_write_ps.
    Write standardized Post Details (PS) file.  JSON file will output the following (previously extracted) information -
        -Post contents, comments, list of likers

    Args:
        tgt_user (str): Instagram target account user name
        dir_output (str): Output directory for JSON files
        src_fp_file (str): Filename for Standardized Profile (FP) file.  Assumed to be located in directory specified by dir_output
        post_data (str): List of instagram post data (as extracted with the scrape_post method)
        code_version (float): IG360 instance variable.  Code version
    """
    # create output header
    if Path.exists(dir_output):
        dt_run = datetime.datetime.now()
        dict_final = {
            "run_datetime" : dt_run.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "ig_record_type" : "ps",
            "code_version" : code_version,
            "fp_source" : src_fp_file,
            "posts" : post_data
        }

        # output as JSON
        fn_out = re.sub(r'[\W]','',dict_final["ig_record_type"]) + '_' + tgt_user + '_' \
            + str(dt_run.year) + str(dt_run.month).zfill(2) + str(dt_run.day).zfill(2) + str(dt_run.hour).zfill(2) + str(dt_run.minute).zfill(2) + '.json'
        fn_out_full = dir_output / fn_out
        with open(fn_out_full, 'w') as json_file:
            json.dump(dict_final, json_file)

        # completion
        print("Output File: {}".format(fn_out_full))
        return [True,fn_out_full]

    else:
           return [False,""]


def util_json_write_mp(tgt_user, dir_output, code_version, profiles):
    """Utility Function: Write standardized Multi-Profile (MP) file

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
    # assemble multi-profile data
    profile_data = []
    for profile in profiles:
        key_fields = ['user_name', 'ind_verified', 'num_posts', 'num_followers', 'num_following', 'full_name', 'description', 'dt_last_post']
        new_dict_record = dict(zip(key_fields,profile))
        profile_data.append(new_dict_record)
    dict_profiles = {
        "profiles" : profile_data
    }

    # create header dictionary
    dt_run = datetime.datetime.now()
    dict_header = {
        "run_datetime" : dt_run.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "ig_record_type" : "mp",
        "code_version" : code_version
    }

    # combine all dictionaries
    dict_final = {**dict_header, **dict_profiles}

    # output as JSON
    fn_out = re.sub(r'[\W]','',dict_header["ig_record_type"]) + '_' + tgt_user + '_' \
        + str(dt_run.year) + str(dt_run.month).zfill(2) + str(dt_run.day).zfill(2) + str(dt_run.hour).zfill(2) + str(dt_run.minute).zfill(2) + '.json'
    fn_out_full = dir_output / fn_out
    with open(fn_out_full, 'w') as json_file:
        json.dump(dict_final, json_file)
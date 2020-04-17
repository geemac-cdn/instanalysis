import pandas as pd
import datetime
import json
import re
from pathlib import Path



def util_json_write_fp(tgt_user, dir_output, record_follower_list, record_following_list, record_post_list, code_version, record_profile):
    """
    Description

    Args:
        x:int: desc
        x:int: desc
        x:int: desc
        x:int: desc
        x:int: desc
        x:int: desc
        x:int: desc

    Returns:
        x:success: Whether the file was successfully written
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
    """
    Description

    Args:
        x:int: desc
        x:int: desc
        x:int: desc
        x:int: desc
        x:int: desc
        x:int: desc
        x:int: desc

    Returns:
        x:success: Whether the file was successfully written
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

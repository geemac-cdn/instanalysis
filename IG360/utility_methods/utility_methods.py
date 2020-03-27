import configparser
import functools
import time

def init_config(config_file_path):
    """
    Initializes the configuration

    Args:
        config_file_path:str: Path to .ini configuration file
    """

    # assert config file has the correct extension
    path = config_file_path.split('.')
    assert(path[len(path)-1] == 'ini')
    
    #read configuration
    config = configparser.ConfigParser() 
    config.read(config_file_path)
    return config


def insta_method(func):
    """
    Instagram method decorator.  Sleeps before and after calling any methods
    that interact with Instagram

    Args:
        func:function: Function to wrap

    Returns:
        wrapper:function: Wrapper function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(4)
        func(*args, **kwargs)
        time.sleep(4)

    return wrapper



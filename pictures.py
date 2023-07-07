from random import randint
import os, os.path

DIR = os.path.dirname(__file__) + "/pictures"

# print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))

def Picture():
    try:
        pictures = [name for name in os.listdir(DIR)]
    except FileNotFoundError as ex:
        print(f"FileNotFoundError: {ex}")
        return None
    
    if len(pictures) != 0:
        randomPicture = DIR + "/" + pictures[randint(0, len(pictures) - 1)]
        return randomPicture
    else:
        return None
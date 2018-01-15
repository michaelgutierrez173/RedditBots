import praw
import requests
import os
import sys
import re
import ctypes
import platform


print("Logging in...")
r = praw.Reddit(client_id='',
                     client_secret='',
                     password='',
                     user_agent='',
                     username='')  #todo
print(r.user.me())

print("Grabbing subreddit...\n")

def get_top_image(sub_reddit):
    """Get image link of most upvoted wallpaper of the day
    :sub_reddit: name of the sub reddit
    :return: the image link
    """

    submissions = sub_reddit.get_new(limit=10) if False else sub_reddit.new(params={"t": "hour"}, limit=10)

    for submission in submissions:
        ret = {"id": submission.id}
        if submission.over_18:
            continue
        url = submission.url
        # Strip trailing arguments (after a '?')
        url = re.sub(R"\?.*", "", url)
        if url.endswith(".jpg") or url.endswith(".png"):
            ret["url"] = url
            return ret
        # Imgur support
        if ("imgur.com" in url) and ("/a/" not in url) and ("/gallery/" not in url):
            if url.endswith("/new"):
                url = url.rsplit("/", 1)[0]
            id = url.rsplit("/", 1)[1].rsplit(".", 1)[0]
            ret["url"] = "http://i.imgur.com/{id}.jpg".format(id=id)
            return ret

def run_bot():

    print("Grabbing image...")
    image = get_top_image(r.subreddit("wallpapers"))
    print(image.get("url"))
    response = requests.get(image.get("url"), allow_redirects=False)

    save_dir = "Pictures\\reddit"

    # If image is available, proceed to save
    if response.status_code == requests.codes.ok:
        # Get home directory and location where image will be saved
        # (default location for Ubuntu is used)
        home_dir = os.path.expanduser("~")
        save_location = "{home_dir}\{save_dir}\{subreddit}-{id}.jpg".format(home_dir=home_dir, save_dir=save_dir,
                                                                            subreddit="reddit",
                                                                            id=image["id"])

        print("location: " + save_location)
        if os.path.isfile(save_location):
            sys.exit("Info: Image already exists, nothing to do, the program is" \
                     " now exiting")

        # Create folders if they don't exist
        dir = os.path.dirname(save_location)
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Write to disk
        with open(save_location, "wb") as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)

        # Check OS and environments
        platform_name = platform.system()
        # Windows
        if platform_name.startswith("Win"):
            # Python 3.x
            if sys.version_info >= (3, 0):
                ctypes.windll.user32.SystemParametersInfoW(20, 0, save_location, 3)
            # Python 2.x
            else:
                ctypes.windll.user32.SystemParametersInfoA(20, 0, save_location, 3)
    else:
        sys.exit("Error: Image url is not available, the program is now exiting.")


run_bot()

import subprocess
import time

def time_helper(seperator = '_', to_sec = False):
    """
    return a string like 2020_09_11_22_43_00 (if to_sec is True) or 2020_09_11_22_43 (if to_sec is False)
    """
    localtime = time.asctime(time.localtime(time.time()))
    if to_sec:
        return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M" + seperator + "%S", time.localtime()) 
    return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M", time.localtime()) 

add_git = "git add ."
update_time = time_helper('-')
commit_git = "git commit -m \" auto update " + update_time + "\""
push_git = "git push origin main"

sleep_time = 60
while True:
    subprocess.call(add_git)
    subprocess.call(commit_git)
    subprocess.call(push_git)
    print("Current update finished, next update will be in ")
    time.sleep(sleep_time)
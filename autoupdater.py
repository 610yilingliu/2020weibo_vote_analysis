import subprocess
import time
import sys
import os

def time_helper(seperator = '_', to_sec = False):
    """
    return a string like 2020_09_11_22_43_00 (if to_sec is True) or 2020_09_11_22_43 (if to_sec is False)
    """
    localtime = time.asctime(time.localtime(time.time()))
    if to_sec:
        return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M" + seperator + "%S", time.localtime()) 
    return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M", time.localtime()) 

class Logger(object):
    def __init__(self, filename, stream=sys.stdout):
	    self.terminal = stream
	    self.log = open(filename, 'a', encoding = 'utf-8')

    def write(self, message):
	    self.terminal.write(message)
	    self.log.write(message)

    def flush(self):
	    pass


add_git = "git add ."
update_time = time_helper('-')
commit_git = "git commit -m \" auto update " + update_time + "\""
push_git = "git push origin main"

sleep_time = 3600

if not os.path.exists('./update_log'):
    os.mkdir('./update_log')
sys.stdout = Logger('./update_log/' + update_time + '.log')

while True:
    for cmd in [add_git, commit_git, push_git]:
        curmsg = subprocess.run(cmd, capture_output= True)
        print(str(curmsg.stdout, encoding = 'utf-8'))
    nxt_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + sleep_time))
    print("Current update finished, next update will be in " + nxt_time + '\n\n')
    time.sleep(sleep_time)
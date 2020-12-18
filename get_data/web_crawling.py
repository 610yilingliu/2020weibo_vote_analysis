import requests
import time
import sys
import pandas as pd
from bs4 import BeautifulSoup

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

def get_html(url):
    """
    :type url: String, url of weibo voting page
    :rtype html: String, html source code
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    }
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        t = time_helper(to_sec= True)
        print("Page error in t")
        # return None if status code is not 200
        return
    html = r.text
    return html

def get_votes(html):
    """
    :type html: String, html source code of weibo voting page
    :rtype data_df: Pandas DataFrame
    """
    if not html:
        return None
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('ul')
    sources = table.find_all('dl')


    def extractor(source):
        source_raw = source.prettify()
        rk_start = "<em>"
        rank_start = source_raw.find(rk_start)
        rank_end = source_raw.find("</em>")
        rank = int(source_raw[rank_start + len(rk_start): rank_end].replace('No.', '').strip())
        name_soup = source.find(class_ = "txt")
        name = name_soup.get_text()

        vote_soup = source.find(class_ = "num")
        vote_uncleaned = vote_soup.get_text()
        vote = int(vote_uncleaned.replace('票', '').replace(',', ''))
        
        return rank, name, vote
    
    ranks, names, votes = [], [], []

    kq = soup.find(class_ = "kq_list_1")
    if kq:
        ranks.append(1)
        n = kq.find(class_ = "txt").get_text()
        v_soup = kq.find(class_ = "num")
        v_uncleaned = v_soup.get_text()
        v = int(v_uncleaned.replace('票', '').replace(',', ''))
        names.append(n)
        votes.append(v)

    for source in sources:
        single_data = extractor(source)
        r, n, v = single_data
        ranks.append(r)
        names.append(n)
        votes.append(v)

    data = {
        "rank": ranks,
        "name": names,
        "vote": votes 
    }
    data_df = pd.DataFrame(data)
    return data_df

def main():
    """
    :type pd_dataframe: Pandas DataFrame
    :export: multiple csv files
    """
    logname = time_helper()
    sys.stdout = Logger('./logs/' + logname + '.log')
    while True:
        t = time_helper()
        game_fname = 'game-' + t + '.csv'
        print("Writing current data to ./game_data/" + game_fname )
        games_html = get_html("https://huodong.weibo.com/netchina2020/people?sub_rank=1")
        game_votes = get_votes(games_html)
        if game_votes is not None:
            game_votes.to_csv("./game_data/" + game_fname)

        star_fname = 'star-' + t + '.csv'
        print("Writing current data to ./star_data/" + star_fname)
        stars_html = get_html("https://huodong.weibo.com/netchina2020/kq")
        star_votes = get_votes(stars_html)
        if star_votes is not None:
            star_votes.to_csv("./star_data/" + star_fname)

        all_fname = 'all-' + t + '.csv'
        print("Writing current data to ./2020_data/" + all_fname)
        all_html = get_html("https://huodong.weibo.com/netchina2020/people?sub_rank")
        all_votes = get_votes(all_html)
        if all_votes is not None:
            all_votes.to_csv('./2020_data/' + all_fname)

        time.sleep(1200)

        

main()
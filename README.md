# 2020weibo_vote_analysis
2020微博年度热点人物投票分析(其实是想看投票有多水)

## Requirement

**Python version**

 3.7.1

### web_crawling.py

beautifulsoup4==4.9.3

pandas==0.25.3

requests==2.23.0

### analyzer.ipynb

pandas==0.25.3

matplotlib==3.1.1

## Web Crawling


```
cd get_data
python web_crawling.py
```

or

```
cd get_data
python3 web_crawling.py
```

## Data Analyze

use Jupyter Notebook to run `./data_analyze/analyzer.ipynb` to see the result

## Auto update to Github

```
python autoupdater.py
```

## Tips

- You can also merge `web_crawling.py` and `autoupdater.py` to run all command at once.
- All important functions are commented, see the input type and usage inside `.py` and `.ipynb` files

## Report

Will be available after 2021.1.7
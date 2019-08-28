# Reddit Datascience Poster

Scrapes several sources for data-science blog posts and whitepapers and posts them to a subreddit: [r/ds_links](http://www.reddit.com/r/ds_links/)

I also used cron to schedule the script to run every day at 6:00 AM and 6:00 PM


### Source Links:
*  [Flowingdata](https://flowingdata.com/)
*  [datascience.com](https://www.datascience.com/resources/topic/white-papers)
*  [data science foundation](https://datascience.foundation/sciencewhitepaper)
*  [IBM](https://www.ibmbigdatahub.com/whitepapers)
*  [arxiv](https://arxiv.org/search/cs?query=data+science&searchtype=all&abstracts=show&order=-announced_date_first&size=50)

### Required Packages:
*  `requests` – HTTP request library
*  `bs4` – Used to parse html response
*  `lxml` – Used by BeautifulSoup
*  `praw` – Used to post to Reddit
*  `feedparser` – Used for collecting links from IBM, which uses an RSS feed

### Other Requirements:
* `Python 3`
* `Virtualenv`
* Reddit developer account & app info
* (Optional) `cron`

### Instructions for Running:
1. Setup a python 3 virtualenv, `venv`, and install the required packages from `requirements.txt`
2. Rename `credentials_example.py` to `credentials.py` and change the `ID`, `SECRET`, `U`, and `P` variables with the correct info for your reddit account and app
3. Rename `run_example.sh` to `run.sh` and edit the path on line 3 to be the path to the current directory
4. (Optional) Schedule `run.sh` with `cron`



### To schedule with cron:

Edit the crontab file with `crontab -e`, then add the following line to the end of the file:

`0 6 * * * ~/path/to/my/dir/run.sh`

Which will schedule the script to run every morning at 6:00 AM



# Investing Scraper

Investing Scraper is an asynchronous webcrawler that utilises the Scrapy Framework. It scrapes an economic calendar, earnings calendar and stock market news and stores the information in a Postgres database. Additionally, data can be subscribed to via Redis Pubsub, allowing updates to be viewed in real time.
### Packages:

[Scrapy](https://doc.scrapy.org/en/0.10.3/intro/overview.html) - To build the asynchronous framework.

[Scrapy Random User-Agent](https://github.com/cnu/scrapy-random-useragent) - To avoid IP address blocking

[Dataset](https://dataset.readthedocs.io/en/latest/quickstart.html) - To access the Postgres database.

[Redis](http://redis-py.readthedocs.io/en/latest/) - So that data can be subscribed to in real time.

[Pandas](http://pandas.pydata.org/pandas-docs/stable/) - For easy data manipulation.

You will also need the following to deploy, schedule and monitor your crawling jobs:

[Scrapyd](http://scrapyd.readthedocs.io/en/stable/) - A Scrapy spider daemon.

[SpiderKeeper](https://github.com/DormyMo/SpiderKeeper) - A spider UI.

There is a script shown in the <b>Install Packages</b> section that allows you to quickly download all of these at once.

## Getting Started in 3 Steps

The following steps will get you up and running with the Investing Crawler. Note: this has only been tested with Python 3.5.3 from Anaconda.

### 1. Clone Repository

Get the repository manually by clicking the download button above or use the command line.
```
git clone https://github.com/jrocco2/invest_scraper.git
```

### 2. Install Packages

Investing Scraper requires the packages listed above. IF you dont have them run the command below in your root directory to quickly dowload all the packages.

```
python crawler_setup.py
```
### 3. Configure the crawler

Now the crawler settings must be configured to connect to the Postgres and Redis databases. Open the settings.py file and edit the  POSTGRES_DB_URL, REDIS_HOST and REDIS_PORT to match your setup. 
```
# settings.py
POSTGRES_DB_URL = 'postgresql://admin:password@localhost:5432/postgres'  # DB to connect to
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
```
### Run the crawler
From the root of the project you can run one of the following commands to run a crawler in the terminal.

Economic Calendar:
```
scrapy crawl invest_scrape
```

Earning Calendar:
```
scrapy crawl earn_scrape
```

Stock Market News:
```
scrapy crawl news_scrape
```

Congratulations! You just run your first job. A few things to note:
1) Your Postgres Database will be now be populated with the data from the crawler you chose to run. The crawler automatically creates and populates the databse for you.

If you ran the invest_scrape crawler, you can run the economic_view.sql file to view current and upcoming events as well as compare 'actual' values to the 'forecast' values.

![postgres_view](https://github.com/jrocco2/invest_scraper/blob/master/screenshots/Postgres_view.JPG)

2) You received a large logfile output in the terminal if you want to save that as a txt file you can do so by going into settings.py and uncommenting LOG_FILE. This will store the log information in the project's root directory as 'mylog.txt'.
```
#LOG_FILE = 'mylog.txt'
```
3) The data was published with Redis. Assuming your using a locally hosted version of Redis, you can run the redis_subscribe.py file in a seperate terminal to view new data entering in real time.
```
python redis_subscribe.py
```

## Deploy
![start_up](https://github.com/jrocco2/invest_scraper/blob/master/screenshots/SpiderKeeper1.JPG)

Now that the crawler is setup, we can use the Scraypd and SpiderKeeper packages to keep the project running in the background as well as schedule periodic jobs and montior performance.

In the project root directory run the 'scrapyd' command.
```
scrapyd
```
Then in the projects root directory run a separate terminal with the following spiderkeeper commands to package your crawler, connect to the scrapyd server and deploy the user interface.
```
python scrapyd-deploy --build-egg output.egg
spiderkeeper --server=http://localhost:6800 --no-auth
```
This will create a server at http://localhost:5000 you can now access via your browser.

## Schedule - 1 Minute periodic jobs

Do the following in the SpiderKeeper UI:

1) Create a project with any name.
2) Upload the output.egg file generated in the previous section.
3) Go to 'Periodic Jobs' then click 'Add Job' in the right hand corner.
4) Select one of your spiders ('invest_scrape', 'earn_scrape', 'news_scrape'  ).
5) Click 'Choose Minute' and set to 'every minute' and click 'Create'.
6) Done! Go to the 'Dashboard' to watch the jobs execute every minute.

![running_jobs](https://github.com/jrocco2/invest_scraper/blob/master/screenshots/SpiderKeeper6.JPG)

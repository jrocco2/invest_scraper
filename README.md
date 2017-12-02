# Investing Scraper

Investing Scraper is an asynchronous webcrawler that utilises the Scrapy Framework. Its role is to scrape an economic calendar and automatically store the information in a Postgres database. Additionally, data can be subscribed to via Redis, allowing updates to be viewed in real time.

## Getting Started

The following steps will get you up and running with the Investing Crawler. Note: this has only been tested with Python 3.5.3 from Anaconda

### Clone Repository

Get the repository manually by clicking the download button above or use the command line.
```
git clone https://github.com/jrocco2/investing_crawler.git
```

### Package Requirements
Investing Scraper has a few package requirements you will need to install if you don't have them.

[Scrapy](https://doc.scrapy.org/en/0.10.3/intro/overview.html) - To build the asynchronous framework.

[Dataset](https://dataset.readthedocs.io/en/latest/quickstart.html) - To access the Postgres database.

[Redis](http://redis-py.readthedocs.io/en/latest/) - So that data can be subscribed to in real time.

[Pandas](http://pandas.pydata.org/pandas-docs/stable/) - For easy data manipulation.

You will also need the following to deploy, schedule and monitor your crawling jobs:

[Scrapyd](http://scrapyd.readthedocs.io/en/stable/) - A Scrapy spider daemon.

[SpiderKeeper](https://github.com/DormyMo/SpiderKeeper) - A spider UI.

To make sure you have all the packages go the project root directory and execute the following:
```
python crawler_setup.py
```

### Configuring the crawler

Now the crawler settings must be configured to connect to the Postgres and Redis databases. Open the settings.py file and edit the  POSTGRES_DB_URL, REDIS_HOST and REDIS_PORT to match your setup. Aditionally, you can also edit the POSTGRES_TABLE_NAME and REDIS_PUBLISH_NAME if you want but this optional.
```
# settings.py
POSTGRES_DB_URL = 'postgresql://joseph:password@localhost:5432/postgres'  # DB to connect to
POSTGRES_TABLE_NAME = 'economic_calendar'  # If it doesnt exist it will be created
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PUBLISH_NAME = 'economic_calendar'
```
### Run the crawler
From the root of the project run the following command in the terminal.
```
scrapy crawl invest_scrape
```
Congratulations! You just run your first job. A few things to note:
1) Your Postgres Database will be now be populated with today's economic calendar data. If you haven't already created the table in your database the crawler will have created it for you.

You can run the economic_view.sql file to view current and upcoming events as well as compare 'actual' values to the 'forecast' values.

![postgres_view](https://github.com/jrocco2/invest_scraper/blob/master/Postgres_view.JPG)

2) You received a large logfile output in the terminal if you want to save that as a txt file you can do so by going into settings.py and uncommenting LOG_FILE. This will store the log information in the project's root directory as 'mylog.txt'
```
#LOG_FILE = 'mylog.txt'
```
3) The data was published with Redis. Assuming your using a locally hosted version of Redis and you didnt change the REDIS_PUBLISH_NAME then you can run the redis_subscribe.py file in a seperate terminal to view the data in real time.
```
python redis_subscribe.py
```

## Deploy
![start_up](https://github.com/jrocco2/invest_scraper/blob/master/SpiderKeeper1.JPG)

Now that the crawler is setup we can use the Scraypd and SpiderKeeper packages to keep the project running in the background as well as schedule periodic jobs and montior performance.

In the project root directory run the 'scrapyd' command.
```
scrapyd
```
Then in the projects root directory run a separate terminal with the following spiderkeeper commands package your crawler, to connect to the scrapyd server and deploy the user interface.
```
python scrapyd-deploy --build-egg output.egg
spiderkeeper --server=http://localhost:6800 --no-auth
```
This will create a server at http://localhost:5000 you can now access via your browser.

## Schedule

Do the following in the SpiderKeeper UI:

1) Create a project with any name
2) Upload the output.egg file in your root project directory
3) Go to 'Periodic Jobs' then click 'Add Job' in the right hand corner
4) Click 'Choose Minute' and set to 'every minute' and click 'Create'
5) Done! Go to the 'Dashboard' to watch the jobs execute every minute.

![running_jobs](https://github.com/jrocco2/invest_scraper/blob/master/SpiderKeeper6.JPG)

## Crawl Speed Check
In the dashboard you can see the log files. Opening the log files gives lots of valuable information including the start and end time for processing. Although it varies depending on the machine, my computer runs each job in 6-8 seconds.

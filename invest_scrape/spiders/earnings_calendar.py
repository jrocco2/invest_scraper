import scrapy
from invest_scrape.items import EarningScraperItem
from invest_scrape.spiders.shared.spider_functions import *
import json
from scrapy.selector import Selector
import re
from datetime import datetime
import logging


class EarnScrape(scrapy.Spider):
    name = "earn_scrape"

    # Define where the spider begins
    start_urls = ["https://www.investing.com/earnings-calendar/"]
    custom_settings = {
        'ITEM_PIPELINES': {'invest_scrape.pipelines.EarningScraperPipeline': 300}
    }

    def parse(self, response):
        """
        Automatically called to handle each of the requests for the start_urls.

        Sends a POST to the calendar with desired filters.

        :param response: The GET response from the start url
        :return: response from POST and passes it to earn_calendar()
        """
        yield scrapy.FormRequest("https://www.investing.com/earnings-calendar/Service/getCalendarFilteredData",
                                 formdata={
                                     'country[]': ['29', '25', '54', '145', '34', '174', '163', '32', '70', '6', '27',
                                                   '37', '122', '15', '113', '107', '55', '24', '59', '71', '22', '17',
                                                   '51', '39', '93', '106', '14', '48', '33', '23', '10', '35', '92',
                                                   '57', '94', '68', '103', '42', '109', '188', '7', '105', '172', '21',
                                                   '43', '20', '60', '87', '44', '193', '125', '45', '53', '38', '170',
                                                   '100', '56', '52', '238', '36', '90', '112', '110', '11', '26',
                                                   '162', '9', '12', '46', '41', '202', '63', '123', '61', '143', '4',
                                                   '5', '138', '178', '75'],
                                     'currentTab': 'thisWeek',
                                     'submitFilters': '1',
                                     'limit_from': '0',
                                 },
                                 callback=self.earn_calendar,
                                 headers={'X-Requested-With': 'XMLHttpRequest'}
                                 )

    def earn_calendar(self, response):
        """
        Extract desired information from the response and send it down the pipeline.

        :param response: Information retrieved from FormRequest() in parse()
        :return: EarningScraperItem instance to pipeline
        """
        item = EarningScraperItem()
        data = response.body.decode('utf-8')
        data = json.loads(data)

        # Extract fields from html using xpath()
        containers = Selector(text=data['data']).xpath("//tr")
        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        for info in containers:
            # item = EarningScraperItem()  # Enable this when debugging (and comment out above one)
            # this will refresh the class on each iteration. Therefore missing items of the class will not show when
            # printed in the except statement below and may be the where the error is coming from.
            try:

                id_check = info.xpath(".//@_r_pid").extract_first()  # Check for valid id or don't create item
                if info.xpath(".//td[contains(@class, 'theDay')]"):
                    date = info.xpath(".//td[contains(@class, 'theDay')]/text()").extract_first()
                    date = datetime.strptime(date, "%A, %B %d, %Y").strftime("%Y/%m/%d %H:%M:%S")
                elif id_check:
                    item['id'] = int(id_check)
                    item['date'] = date
                    item['country'] = info.xpath(".//td[contains(@class, 'flag')]/span/@title").extract_first()
                    item['company'] = info.xpath(".//td[contains(@class, 'earnCalCompany')]/span/text()").extract_first()
                    item['short_code'] = info.xpath(".//td[contains(@class, 'earnCalCompany')]/a/text()").extract_first()
                    # Where 1 = Before Market Open, 2 = During Market, 3 = After Market Close
                    item['market_time'] = info.xpath(".//@data-value").extract_first()

                    eps_actual = info.xpath(".//td[contains(@class,'eps_actual')]/text()").extract_first()
                    if eps_actual == '--':  # If -- is found set number to None
                        item['eps_actual'] = None
                    else:
                        item['eps_actual'] = eps_actual

                    forecasts = info.xpath(".//td[contains(@class,'leftStrong')]/text()").extract()
                    eps_forecast = re.sub(r'/\xa0+', '', forecasts[0])  # Remove non-breaking spaces
                    if eps_forecast == '--':
                        item['eps_forecast'] = None
                    else:
                        item['eps_forecast'] = eps_forecast

                    rev_actual = re.sub(r'/\xa0+|,', '', info.xpath(".//td[contains(@class,'rev_actual')]/text()").extract_first())
                    rev_actual_units = unit_splitter(rev_actual)
                    item['rev_actual'] = rev_actual_units[0]

                    rev_forecast = re.sub(r'/\xa0+|,', '', forecasts[1])  # Remove non-breaking spaces
                    rev_forecast_units = unit_splitter(rev_forecast)
                    item['rev_forecast'] = rev_forecast_units[0]

                    mark_cap = info.xpath(".//td[contains(@class,'right')]/text()").extract_first()
                    if mark_cap:
                        market_cap = re.sub(r'/\xa0+|,', '', mark_cap)
                        market_cap_units = unit_splitter(market_cap)
                        item['market_cap'] = market_cap_units[0]
                    else:
                        item['market_cap'] = None

                    yield item

            except ValueError as err:
                logging.warning("ValueError error: {0}".format(err))
                print(vars(item))

            except TypeError as err:
                logging.warning("TypeError error: {0}".format(err))
                print(vars(item))

            except:
                logging.warning("Item skipped due to unknown error")
                print(vars(item))

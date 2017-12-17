import scrapy
from invest_scrape.items import InvestingScraperItem
from invest_scrape.spiders.shared.spider_functions import *
import json
from scrapy.selector import Selector
import re
import logging


class InvestScrape(scrapy.Spider):
    name = "invest_scrape"

    custom_settings = {
        'ITEM_PIPELINES': {'invest_scrape.pipelines.InvestingScraperPipeline': 300}
    }
    # Define where the spider begins
    start_urls = ["https://www.investing.com/economic-calendar/"]

    def parse(self, response):
        """
        Automatically called to handle each of the requests for the start_urls.

        Sends a POST to the calendar with desired filters.

        :param response: The GET response from the start url
        :return: response from POST and passes it to economic_calendar()
        """

        yield scrapy.FormRequest("https://www.investing.com/economic-calendar/Service/getCalendarFilteredData",
                                 formdata={
                                     'country[]': ['29', '25', '54', '145', '47', '34', '174', '163', '32', '70', '6',
                                                   '27', '37', '122', '15','78','113', '107', '55', '24', '121', '59',
                                                   '89', '72', '71', '22', '17', '51', '39', '93', '106','14', '48',
                                                   '66', '33', '23', '10', '119', '35', '92', '102', '57','94', '97',
                                                   '68', '96', '103', '111', '42', '109', '188', '7', '139', '247',
                                                   '105', '172', '21', '43', '20', '60', '87', '44', '193', '125', '45',
                                                   '53', '38', '170', '100', '56', '80', '52', '238', '36', '90', '112',
                                                   '110', '11', '26', '162', '9', '12', '46', '85', '41', '202', '63',
                                                   '123', '61', '143', '4', '5', '138', '178', '84', '75'],
                                     'timeZone': '55',  # GMT Time
                                     'timeFilter': 'timeRemain',
                                     'currentTab': 'thisWeek',
                                     'submitFilters': '1',
                                     'limit_from': '0',
                                 },
                                 callback=self.economic_calendar,
                                 headers={'X-Requested-With': 'XMLHttpRequest'}
                                 )

    def economic_calendar(self, response):
        """
        Extract desired information from the response and send it down the pipeline.

        :param response: Information retrieved from FormRequest() in parse()
        :return: InvestingScraperItem instance to pipeline
        """

        item = InvestingScraperItem()
        data = response.body.decode('utf-8')
        data = json.loads(data)

        # Extract fields from html using xpath()
        containers = Selector(text=data['data']).xpath("//tr[contains(@class,'js-event-item')]")
        print(len(containers))
        for info in containers:

            # item = InvestingScraperItem()  # Enable this when debugging (and comment out above one)
            # this will refresh the class on each iteration. Therefore missing items of the class will not show when
            # printed in the except statement below and may be the where the error is coming from.

            try:

                item['id'] = int(re.sub(r'eventRowId_', '', info.xpath(".//@id").extract_first()))
                item['date'] = info.xpath(".//@data-event-datetime").extract_first()
                item['currency'] = info.xpath(".//td[contains(@class,'left flagCur noWrap')]/text()").extract_first().strip()

                # Convert High, Moderate, Low to 1,2,3
                importance = info.xpath(".//td[contains(@class,'left textNum sentiment noWrap')]/@title").extract_first()
                level = re.search(r'(Low)|(High)|(Moderate)', importance)
                if level.group() == 'Low':
                    item['importance'] = 1
                elif level.group() == 'Moderate':
                    item['importance'] = 2
                elif level.group() == 'High':
                    item['importance'] = 3
                else:
                    item['importance'] = None

                item['event'] = info.xpath(".//a[contains(@target,'_blank')]/text()").extract_first().strip()

                # r'\xa0|,' === search for "\xa0" and\or "," and remove it
                # Separate units from integer
                actual = re.sub(r'\xa0|,', '', info.xpath(".//td[starts-with(@id, 'eventActual_')]/text()").extract_first())
                actual_units = unit_splitter(actual)
                item['actual'] = actual_units[0]

                forecast = re.sub(r'\xa0|,', '',info.xpath(".//td[starts-with(@id, 'eventForecast_')]/text()").extract_first())
                forecast_units = unit_splitter(forecast)
                item['forecast'] = forecast_units[0]

                previous = re.sub(r'\xa0|,', '',info.xpath(".//td[starts-with(@id, 'eventPrevious_')]/span/text()").extract_first())
                previous_units = unit_splitter(previous)
                item['previous'] = previous_units[0]

                if (actual_units[1] == '%') or (forecast_units[1] == '%') or (previous_units[1] == '%'):
                    item['unit'] = '%'
                else:
                    item['unit'] = ''

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

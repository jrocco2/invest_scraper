import scrapy
from invest_scrape.items import EarningScraperItem
import json
from scrapy.selector import Selector
import re
from datetime import datetime


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
                                     'currentTab': 'today',
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
            id_check = info.xpath(".//@_p_pid").extract_first()  # Check for valid id or don't create item
            if info.xpath(".//td[contains(@class, 'theDay')]"):
                date = info.xpath(".//td[contains(@class, 'theDay')]/text()").extract_first()
                date = datetime.strptime(date, "%A, %B %d, %Y").strftime("%Y/%m/%d %H:%M:%S")
            elif id_check:
                item['id'] = id_check
                item['date'] = date
                item['country'] = info.xpath(".//td[contains(@class, 'flag')]/span/@title").extract_first()
                item['company'] = info.xpath(".//td[contains(@class, 'earnCalCompany')]/span/text()").extract_first()
                item['short_code'] = info.xpath(".//td[contains(@class, 'earnCalCompany')]/a/text()").extract_first()
                item['market_cap'] = info.xpath(".//td[contains(@class,'right')]/text()").extract_first()
                # Where 1 = Before Market Open, 2 = During Market, 3 = After Market Close
                item['market_time'] = info.xpath(".//@data-value").extract_first()

                eps_actual = info.xpath(".//td[contains(@class,'eps_actual')]/text()").extract_first()
                item['eps_actual'] = eps_actual

                forecasts = info.xpath(".//td[contains(@class,'leftStrong')]/text()").extract()
                eps_forecast = re.sub(r'/\xa0\xa0', '', forecasts[0])  # Remove non-breaking spaces
                item['eps_forecast'] = eps_forecast

                rev_actual = info.xpath(".//td[contains(@class,'rev_actual')]/text()").extract_first()
                rev_actual_units = self.unit_splitter(rev_actual)
                item['rev_actual'] = rev_actual_units[0]
                item['rev_actual_units'] = rev_actual_units[1]

                rev_forecast = re.sub(r'/\xa0\xa0', '', forecasts[1])  # Remove non-breaking spaces
                rev_forecast_units = self.unit_splitter(rev_forecast)
                item['rev_forecast'] = rev_forecast_units[0]
                item['rev_forecast_units'] = rev_forecast_units[1]

                yield item

    def unit_splitter(self, number):
        """
        When given a string, separate the numbers from their suffix's
        """
        unit = re.search('([A-Za-z]+)|(%)', number)  # Check for units or %
        if unit:  # If units are found
            reg = re.compile(unit.group())  # Create regex to search unit
            return [re.sub(reg, '', number), unit.group()]
        else:
            return [number, '']

import scrapy
from invest_scrape.items import InvestingScraperItem
import json
from scrapy.selector import Selector
import re
#from datetime import date, datetime, timedelta


class InvestScrape(scrapy.Spider):
    name = "invest_scrape"

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
                                     'timeZone': '55',
                                     'timeFilter': 'timeRemain',
                                     'currentTab': 'yesterday',
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

                item['id'] = int(info.xpath(".//@event_attr_id").extract_first())
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

                # Separate units from integer
                actual = re.sub(r'\xa0', '', info.xpath(".//td[starts-with(@id, 'eventActual_')]/text()").extract_first())
                actual_unit = re.search('([A-Za-z]+)|(%)', actual)
                if actual_unit:
                    reg = re.compile(actual_unit.group())
                    item['actual'] = re.sub(reg, '', actual)
                    item['actual_unit'] = actual_unit.group()
                else:
                    item['actual'] = actual
                    item['actual_unit'] = ''

                forecast = re.sub(r'\xa0', '',info.xpath(".//td[starts-with(@id, 'eventForecast_')]/text()").extract_first())
                forecast_unit = re.search('([A-Za-z]+)|(%)', forecast)
                if forecast_unit:
                    reg = re.compile(forecast_unit.group())
                    item['forecast'] = re.sub(reg, '', forecast)
                    item['forecast_unit'] = forecast_unit.group()
                else:
                    item['forecast'] = forecast
                    item['forecast_unit'] = ''

                previous = re.sub(r'\xa0', '',info.xpath(".//td[starts-with(@id, 'eventPrevious_')]/span/text()").extract_first())
                previous_unit = re.search('([A-Za-z]+)|(%)', previous)
                if previous_unit:
                    reg = re.compile(previous_unit.group())
                    item['previous'] = re.sub(reg, '', previous)
                    item['previous_unit'] = previous_unit.group()
                else:
                    item['previous'] = actual
                    item['previous_unit'] = ''

                yield item

    # def generate_dates(self, start_date, end_date):
    #     """
    #     Generates all the dates in a specified range
    #
    #     :param start_date: starting date in this form: date(2011, 10, 10)
    #     :param end_date: ending date in this form: date(2011, 10, 12)
    #     :return: a list of dates that can be used to access website data
    #     """
    #     # TODO: Fix static dates
    #
    #     def perdelta(start, end, delta):
    #         curr = start
    #         while curr <= end:
    #             yield curr
    #             curr += delta
    #     dates = []
    #     for result in perdelta(start_date, end_date, timedelta(days=1)):
    #         dates.append(result)
    #
    #     return dates
    #
    # def form_data(self, dates):
    #     formdata = {
    #         'country[]': ['29', '25', '54', '145', '47', '34', '174', '163', '32', '70', '6', '27', '37', '122', '15',
    #                       '78',
    #                       '113', '107', '55', '24', '121', '59', '89', '72', '71', '22', '17', '51', '39', '93', '106',
    #                       '14', '48', '66', '33', '23', '10', '119', '35', '92', '102', '57', '94', '97', '68', '96',
    #                       '103',
    #                       '111', '42', '109', '188', '7', '139', '247', '105', '172', '21', '43', '20', '60', '87',
    #                       '44',
    #                       '193', '125', '45', '53', '38', '170', '100', '56', '80', '52', '238', '36', '90', '112',
    #                       '110',
    #                       '11', '26', '162', '9', '12', '46', '85', '41', '202', '63', '123', '61', '143', '4', '5',
    #                       '138',
    #                       '178', '84', '75'],
    #         'timeZone': '31',
    #         'timeFilter': 'timeRemain',
    #         'dateFrom': str(dates),
    #         'dateTo': str(dates),
    #         'submitFilters': '1',
    #         'limit_from': '0',
    #     }
    #
    #     return formdata
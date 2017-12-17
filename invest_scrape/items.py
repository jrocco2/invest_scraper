import scrapy


class InvestingScraperItem(scrapy.Item):
    """
    Scraper item for economic calendar
    """
    id = scrapy.Field()
    date = scrapy.Field()
    currency = scrapy.Field()
    importance = scrapy.Field()
    event = scrapy.Field()
    actual = scrapy.Field()
    forecast = scrapy.Field()
    previous = scrapy.Field()
    unit = scrapy.Field()

    def __str__(self):
        """
        Overload the print method to avoid printing too many details in the log
        """
        return ""


class EarningScraperItem(scrapy.Item):
    """
    Scraper item for earnings calendar
    """
    id = scrapy.Field()
    date = scrapy.Field()
    country = scrapy.Field()
    company = scrapy.Field()
    short_code = scrapy.Field()
    eps_actual = scrapy.Field()  # Earnings Per Share
    eps_forecast = scrapy.Field()
    rev_actual = scrapy.Field()
    rev_forecast = scrapy.Field()
    market_cap = scrapy.Field()
    market_time = scrapy.Field()  # Where 1 = Before Market Open, 2 = During Market, 3 = After Market Close

    def __str__(self):
        """
        Overload the print method to avoid printing too many details in the log
        """
        return ""


class NewsScraperItem(scrapy.Item):
    """
    Scraper item for earnings calendar
    """
    id = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()

    def __str__(self):
        """
        Overload the print method to avoid printing too many details in the log
        """
        return ""
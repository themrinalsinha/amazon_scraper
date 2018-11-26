from requests       import get
from lxml.html      import fromstring
from fake_useragent import UserAgent

class AmazonScraper(object):
    def __init__(self, asin):
        self.asin   = asin
        self.html   = None
        self.status = self.product_info()

    def page_source(self):
        return get('https://amazon.com/dp/{}'.format(self.asin), headers={'User-Agent':UserAgent().random})

    def product_info(self):
        response = self.page_source()
        if response.status_code is 200:
            self.html = fromstring(response.text)
            return True
        return False

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

    def details(self):
        if self.status is True and self.html is not None:
            return {'title': (self.html.xpath('//*[@id="productTitle"]/text()') or [''])[0].strip(),
                    'category': ([' '.join(x.strip() for x in  self.html.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]//li//text()'))] or [''])[0].strip(),
                    'price': {'current':  (self.html.xpath('//*[@id="priceblock_ourprice"]/text()') or [''])[0].strip(),
                              'original': (self.html.xpath('//*[text()= "List Price:"]/following-sibling::td/span[1]/text()') or [''])[0].strip(),
                              'saved':    (self.html.xpath('//*[@id="regularprice_savings"]/td[2]/text()') or [''])[0].strip()},
                    'rating': (self.html.xpath('//*[@id="averageCustomerReviews"]/span[1]/span/@title') or [''])[0].strip(),
                    'availability': (self.html.xpath('//*[@id="availability"]/span/text()') or [''])[0].strip()}

if __name__ == '__main__':
    x = AmazonScraper('B06XD3LXXK').details()
    print(x)

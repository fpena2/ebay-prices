from statistics import median
from numpy import average
from bs4 import BeautifulSoup as BS
import requests


class eBay():
    def __init__(self, page) -> None:
        self.page = page
        self.html = BS(requests.get(url=page).text, 'html.parser')
        self.box = {}

    def process(self):
        for ultag in self.html.find_all('ul', {'id': 'ListViewInner'}):
            for litag in ultag.find_all('li'):
                try:
                    title = litag.find_all('h3', {'class': 'lvtitle'})[0].text
                    model = title.split()[2]
                    price = litag.find_all(
                        'li', {'class': 'lvprice prc'})[0].text
                    price = float(price.strip().replace('$', ''))

                    if model not in self.box.keys():
                        self.box[model] = []
                    self.box[model].append(price)

                except Exception as e:
                    pass

    def print(self):
        print("Quantity,Model,Min,Median,Average,Max")
        for model in self.box:
            values = self.box[model]
            if(len(values) > 1):
                print("{},{},{},{},{},{}".format(len(values), model, min(values), median(
                    values), average(values), max(values)))


# Example
page = "https://www.ebay.com/sch/PC-Laptops-Netbooks/177/m.html?Category=177&_ssn=greencitizen&sellerName=greencitizen&_sop=1&_from=R40&_nkw=thinkpad&LH_Complete=1&LH_Sold=1&rt=nc"
a = eBay(page)
a.process()
a.print()

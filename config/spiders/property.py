import scrapy
from bs4 import BeautifulSoup

class PropertySpider(scrapy.Spider):
    name = 'property'
    allowed_domains = ['delta.ir']
    start_urls = ['https://delta.ir/sitemap/mainCitySeachSiteMap.xml']

    links = []

    # def start_requests(self):
    #     yield scrapy.Request(url="https://delta.ir/sitemap/mainCitySeachSiteMap.xml", callback=self.parse, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"})

    def parse(self, response):
        xml_text = response.text

        soup = BeautifulSoup(xml_text)
        sitemapTags = soup.find_all("url")

        for sitemap in sitemapTags:
            self.links.append(sitemap.findNext("loc").text)

        # yield {"res":self.links}
        for link in self.links:
            yield scrapy.Request(url = link,callback= self.parse_link)
    

    def parse_link(self,response):
        is_not_found = response.xpath('//h3[@class="mrg30B lnheight-220"]')

        if not is_not_found :
            properties = response.xpath('//div[@class="col-md-6 pad0L col-box  sell-box  "]')
            city = response.xpath('//i[@class="chevron down icon"]/following-sibling::node()').get()

            for property in properties:
                image = property.xpath('.//descendant::a[@class="more-detail"]/img/@src').get()
                publish_date = property.xpath('.//descendant::div[@class="item-date"]/text()').get()

                # details 
                result_box = property.xpath('.//descendant::div[@class="search-results-info-boxes"]/a')
                link = result_box.xpath('.//@href').get()
                title = result_box.xpath('.//h2/text()').get()
                area = result_box.xpath('.//div[@class="search-list-item"]/span[1]/text()').get()
                room_count = result_box.xpath('.//div[@class="search-list-item"]/span[3]/text()').get()
                creation_date = result_box.xpath('.//div[@class="search-list-item"]/span[5]/text()').get()
                price = result_box.xpath('.//div[@class="search-list-price"]/span/text()').get()

                yield {
                    "city" : city.strip(),
                    "title" : title.strip(),
                    "price" : price.strip(),
                    "room_count" : room_count.strip(),
                    "area" : area.strip(),
                    "creation_date" : creation_date.strip(),
                    "publish_date" : publish_date.strip(),
                    "image" : image.strip(),
                    "link" : link.strip(),
                }
            
            next_page = response.xpath('//a[@id="lnkmore"]/@href').get()

            if next_page :
                yield scrapy.Request(url=next_page,method=self.parse_link)
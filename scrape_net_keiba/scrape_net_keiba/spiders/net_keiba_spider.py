import scrapy
from scrapy_splash import SplashRequest

from scrape_net_keiba.items import ScrapeNetKeibaItem


class NetKeibaSpiderSpider(scrapy.Spider):
    name = 'net_keiba_spider'
    allowed_domains = ['race.netkeiba.com']

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return {
                html = splash:html()
            }
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://race.netkeiba.com/top/?rf=navi',
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': self.script})

    def parse(self, response):
        use_domain = 'https://race.netkeiba.com'
        # レース後だとshutuba.htmlではなくて、result.htmlに遷移する(HTMLのclass名が少し違うから取れなくなったら確認)
        detail_links = response.xpath('//li[contains(@class, "RaceList_DataItem")]/a[1]/@href').re('..(.+)')

        item = ScrapeNetKeibaItem()

        for link in detail_links:
            if 'result' in link:
                link = link.replace('result', 'shutuba')

            link = use_domain + ''.join(link)

            request = scrapy.Request(link, self.parse_race_title)
            request.meta['item'] = item
            yield request

    def parse_race_title(self, response):
        item = response.meta['item']
        # item['']
        item['uma_id'] = response.xpath('//span[@class="HorseName"]/a/@href').re('\d+')
        item['race_title'] = response.xpath('//div[@class="RaceName"]/text()').re('.+')
        item['waku_number'] = response.xpath('//tr[@class="HorseList"]/td[1]/span/text()').re('.+')
        item['uma_number'] = response.xpath('//tr[@class="HorseList"]/td[2]/text()').re('.+')
        item['uma_name'] = response.xpath('//span[@class="HorseName"]/a/text()').re('.+')
        item['uma_nenrei'] = response.xpath('//td[@class="Barei Txt_C"]/text()').re('.+')
        item['kinryo'] = response.xpath('//td[@class="Txt_C"]/text()').re('.+')
        item['jocky'] = response.xpath('//td[@class="Jockey"]/a/text()').re('(\S+)')
        item['area'] = response.xpath('//td[@class="Trainer"]/span/text()').re('.+')
        item['trainer'] = response.xpath('//td[@class="Trainer"]/a/text()').re('.+')

        horse_data = [item['uma_number'], item['uma_name'], item['uma_nenrei'], item['kinryo'], item['jocky'],
                      item['area'], item['trainer']]

        # データの転置処理
        horse_data = list(map(list, zip(*horse_data)))
        horse_data.insert(0, item['race_title'])

        # モデルに食わせたいからレースごとにcsvに落とし込めるとベスト
        with open('scraped_data.txt', 'a', newline='\n')as f:
            for d in horse_data:
                f.write('%s\n' % d)

        yield item

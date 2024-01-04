import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    time.sleep(1)
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)
    thumbnail_url = selector.css('.entry-thumbnail a::attr(href)')

    urls = []

    for url in thumbnail_url.getall():
        urls.append(url)

    return urls


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page_url = selector.css('.next.page-numbers::attr(href)').get()

    if next_page_url:
        return next_page_url
    else:
        return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)

    data_news = {}

    data_news['url'] = selector.css('link[rel="canonical"]::attr(href)').get()
    data_news['title'] = selector.css('h1.entry-title::text').get().strip()
    data_news['timestamp'] = selector.css('li.meta-date::text').get()
    data_news['writer'] = (
        selector.css('h5.title-author span.fn a::text').get().strip()
    )

    reading_time_text = (
        selector.css('li.meta-reading-time::text').get().strip()
    )
    data_news['reading_time'] = (
        int(reading_time_text.split()[0]) if reading_time_text else ''
    )

    summary_elements = selector.xpath("(//p)[1]//text()").extract()
    data_news["summary"] = ''.join(summary_elements).strip(" \xa0")

    data_news['category'] = selector.css('span.label::text').get()

    return data_news


# Requisito 5
def get_tech_news(amount):
    url = 'https://blog.betrybe.com/'
    html_content = fetch(url)
    updates = scrape_updates(html_content)
    next_page_link = scrape_next_page_link(html_content)
    news = []

    while len(updates) < amount:
        html_content = fetch(next_page_link)
        updates.extend(scrape_updates(html_content))
        next_page_link = scrape_next_page_link(html_content)

    updates = updates[:amount]

    for update in updates:
        page_of_new = fetch(update)
        new_content = scrape_news(page_of_new)
        news.append(new_content)

    create_news(news)
    return news

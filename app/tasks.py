import os

from celery import Celery
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import cloudscraper

load_dotenv()
celery_app = Celery('tasks', broker=os.getenv('BROKER_URL'), backend=os.getenv('BACKEND_URL'))
amazon_url = "https://www.amazon.com/s?k="


@celery_app.task(bind=True)
def amazon_search(self, query: str):
    print(f'searching {query}\n')
    scraper = cloudscraper.create_scraper()  # create a cloudscraper instance
    response = scraper.get(amazon_url + query)  # request the url
    if response.status_code != 200:
        return f'Error {response.status_code} retrieving {query}.'

    soup = BeautifulSoup(response.content, 'html.parser')  # parse the html
    try:
        result_divs = soup.find_all('div', attrs={'data-component-type': 's-search-result'})  # find all result divs
    except AttributeError:
        return f'Error retrieving results for {query}.'

    result_list = []
    # for each result div, find the title, link, image, and price and add it to the result list
    for result in result_divs:
        try:
            a_component = result.find('a', attrs={
                'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            link = a_component['href']
            try:
                title_component = a_component.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
                title = title_component.get_text().strip()
            except AttributeError:
                title = 'N/A'
        except AttributeError:
            link = 'N/A'
            title = 'N/A'

        try:
            img_component = result.find('img', attrs={'class': 's-image'})
            image = img_component['src']
        except AttributeError:
            image = 'N/A'

        try:
            price_component = result.find('span', attrs={'class': 'a-offscreen'})
            price = price_component.get_text().strip()
        except AttributeError:
            price = 'N/A'

        result_list.append({'title': title, 'link': link, 'image': image, 'price': price})

    # send result to backend / database
    return result_list


celery_app.tasks.register(amazon_search)

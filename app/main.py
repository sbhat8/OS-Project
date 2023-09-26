from fastapi import FastAPI

from app.tasks import amazon_search
from bs4 import BeautifulSoup
import cloudscraper


app = FastAPI()

amazon_url = "https://www.amazon.com/s?k="


@app.get("/async/scrape/amazon/{query}")
async def async_scrape(query: str):
    task = amazon_search.delay(query)
    return {"message": "Started scraping in the background", "task_id": task.id}


@app.get("/scrape/amazon/{query}")
async def scrape(query: str):
    print(f'searching {query}\n')
    scraper = cloudscraper.create_scraper()
    response = scraper.get(amazon_url + query)
    if response.status_code != 200:
        return f'Error {response.status_code} retrieving {query}.'

    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    result_divs = soup.find_all('div', attrs={'data-component-type': 's-search-result'})
    result_list = []
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

    return result_list


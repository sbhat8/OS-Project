# OS-Project

## Description
Currently, the crawler is able to take a query as parameter and search https://amazon.com for search results and product details. The crawler is able to extract the following information from the search results and product details pages:
- Product title
- Product link
- Product price
- Product rating

## Requirements
Beyond the requirements in `requirements.txt`, you will need to install RabbitMQ as a message broker.
Go to this link to download and install RabbitMQ: https://www.rabbitmq.com/download.html

## Key commands

### To run the development server
```
pip install -r requirements.txt
```
```
uvicorn main:app --reload
```
Then, go to http://localhost:8000/docs to view the API documentation and test the API.

### To start celery workers
```
celery -A app.tasks worker --loglevel=info --concurrency=2 -E -P eventlet
```
This starts 2 workers. The number of workers can be changed by changing the `--concurrency` flag.

### To start flower monitoring
```
celery --broker=amqp://guest:guest@localhost:5672// flower
```
Then, go to http://localhost:5555 to view the flower dashboard.

### To run the crawler
Go to http://localhost:8000/docs and click on the `/async/scrape/amazon/{query}` endpoint. 
Then, click on the `Try it out` button and enter a query in the `query` field. Click on the `Execute` button to start the crawler.
As the crawler runs, you can go to http://localhost:5555 to view the flower dashboard and monitor the progress of the crawler and see results.

If you would like to run the crawler without using celery workers (without concurrency), you can use the `/scrape/amazon/{query}` endpoint instead.
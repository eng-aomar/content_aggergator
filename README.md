# content_aggergator
A content Aggregator website using python flask


A content aggregator fetches information from various places online and gathers all of that information in one place. Therefore, you don’t have to visit multiple sites to get the latest info: one website is enough.

With the content aggregator, all of the latest information can be gotten from one site that aggregates all the content. People can see the posts that interest them and can decide to find out more about them without traipsing all over the internet.

Python libraries used to build my content aggregator

Requests: HTTP library for Python, built for human beings.
Beautiful Soup: Python library for quick turnaround projects like screen-scraping.
PyMongo :is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python.
SendGrid : for email sending
BluePrint : Functional Structuring of files
Concurent.futures: to achive faster execution time using multithreading. 

#Technical Details

The main objective of this project idea is to aggregate content. First, you need to know what sites you’ll want the Content Aggregator to get content from. Then, you can use libraries such as requests for sending HTTP requests and BeautifulSoup to parse and scrape the necessary content from the sites.

Your application can implement its content aggregation as a background process. Libraries such as celery or apscheduler can help with that. You can try out apscheduler. It’s great for small background processes.

After scraping content from various sites, you’ll need to save it somewhere. So, you’ll use a database to save the scraped content.

<h1>pynews</h1>

- [Installation](#installation)
- [API Key](#api-key)
- [Worflow](#worflow)
  - [Initialization](#initialization)
  - [Searching News articles](#searching-news-articles)
    - [SearchEverything](#searcheverything)
    - [SearchHeadlines](#searchheadlines)
  - [Pagination](#pagination)
  - [Error handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

Hello folks !

![anya_gif](https://media.tenor.com/G13lUO8AyLIAAAAC/spy-x-family-spy-family.gif)

`pynews` is a Python library that provides a simplified and convenient way to interact with the NewsAPI service. It encapsulates the complexities of making API requests and handling responses, allowing developers to easily integrate news data into their applications.

# Installation

If you want to clone this project and add more features, do as follow:

```bash
$ py -m venv venv
$ source venv/bin/activate # venv/Scripts/activate on Windows
(venv) $ pip install .[dev]
```

# API Key

Before you can start using the wrapper, you need to obtain an API key from the NewsAPI website. Visit https://newsapi.org and sign up for an account to obtain your API key.

# Worflow

## Initialization

To initialize `pynews` client, create an instance of `Client` class as shown below:

```python
from pynews.client import Client

# Normal method
client: Client = Client(api_key="fake_api_key")

# Context Manager method
async with Client(api_key="fake_api_key") as client:
    # do something with client
    pass
```

Replace `fake_api_key` with your actual NewsAPI API key.

## Searching News articles

`pynews` provides two main classes, SearchEverything and SearchHeadlines, for querying news articles. 

### SearchEverything

To search for news articles using the `SearchEverything` class, use the `search_everything` method as shown below:

```python
from pynews import Client
from pynews.models import SearchEverything, NewsResponse

client: Client = Client(api_key="fake_api_key")
search: SearchEverything = SearchEverything(
    q="bitcoin",
    from_date="2021-08-01",
    to_date="2021-08-10",
    language="en",
    sort_by="relevancy",
    page=1,
    page_size=20,
)
res: NewsResponse = await client.get_everything(search)

for article in res.articles:
    print(article.title)
```

### SearchHeadlines

To search for news headlines using the `SearchHeadlines` class, use the `search_headlines` method as shown below:

```python
from pynews import Client
from pynews.models import SearchHeadlines, NewsResponse

client: Client = Client(api_key="fake_api_key")
search: SearchHeadlines = SearchHeadlines(
    q="bitcoin",
    country="us",
    category="business",
    page=1,
    page_size=20,
)
res: NewsResponse = await client.get_headlines(search)

for article in res.articles:
    print(article.title)
```

## Pagination

If you need to retrieve a large number of articles, you can use the pagination feature provided by the wrapper.<br>
Both the SearchEverything and SearchHeadlines classes support pagination by specifying the page_size and page parameters:

```python	
from pynews.models import SearchEverything

search: SearchEverything = SearchEverything(query='Bitcoin', page_size=20, page=2)
```

This will retrieve the second page of articles related to the query 'Bitcoin', with each page containing 20 articles.<br>
You can iterate over the pages to retrieve all the articles.

## Error handling

If an error occurs while making an API request, the wrapper will raise an exception. You can catch the exception and handle it appropriately.

```python
from pynews import Client
from pynews.models import SearchHeadlines
from pynews.utils.exceptions import NewsAPIError

try:
    client: Client = Client(api_key="fake_api_key")
    search: SearchHeadlines = SearchHeadlines(
        q="bitcoin",
        country="us",
        category="business",
        page=1,
        page_size=20,
    )
    res: NewsResponse = await client.get_everything(search)
except NewsAPIError as e:
    print(f"An error occurred: {e}")
```

# Contributing

Contributions to `pynews` are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the project's GitHub repository.<br>
Before submitting a pull request, make sure to run the tests and ensure that your changes do not break the existing functionality. Add tests for any new features or fixes you introduce.

# License

`pynews` is open-source software released under the [MIT License](https://opensource.org/license/mit/). Feel free to use, modify, and distribute it according to the terms of the license.

# Acknowledgements

This project was developed by [jordan95v](https://github.com/jordan95v).<br>
I would like to thank the NewsAPI team for providing a powerful and comprehensive news service, making it easier for developers to integrate news data into their applications.

<h1>Thanks you for reading me and using <b>pynews</b>!</h1>

![goodbye_gif](https://media.tenor.com/5UrK7rSTuscAAAAd/goodbye-bye-bye.gif)


# EmailScrapper

Python code to scrap emails from company websites using company names.


## Prerequisites

Google API Key and Google Custom Search ID

To configure the environment, add a `.env` in the root directory of your
project:

```
.
├── .env
└── email_scrapper.py
```

The syntax of `.env` files supported is similar to that of Bash:

```bash
GOOGLE_API_KEY=XXXXXXX
GOOGLE_CSE_ID=XXXXXXX
```

Follow this guide to setup [Google Search API](https://linuxhint.com/google_search_api_python/).


## Usage

Execute below command to start scrapping for emails::

   $ python email_scrapper.py

Execute below command if you want to disable SSL renegotiation error

   $ export OPENSSL_CONF=/path/to/custom/openssl.cnf && python email_scrapper.py


## Features

- Scraps from best matched company website using googlesearch
- Company name input can be provided from csv file
- Output generated in standar csv format
- Good for finding privacy contacts
- Uses Google Search API for searching for sites


## Authors

- [Tushar Velingkar](https://github.com/tvelingkar)


## Tech Stack

**Core:** Python, Googlesearch, Pandas


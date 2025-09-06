# PropertyFinder

PropertyFinder is a professional web scraping project designed to extract real estate listings and property data from ["https://www.onthemarket.com"] websites. The project leverages Python and Scrapy to automate data collection for analysis, research, or integration into other applications.

## Features

- Scrapes property listings including price, location, features, and more
- Outputs data in CSV format for easy analysis
- Modular and extensible Scrapy architecture
- Customizable spiders and pipelines

## Project Structure

```
PropertyFinder/
│
├── propertyfinder/             # Main Scrapy project package
│   ├── spiders/                # Scrapy spiders
│   │   └── property_finder.py  # Main spider
│   ├── items.py                # Data models
│   ├── pipelines.py            # Data processing pipelines
│   ├── middlewares.py          # Custom middlewares
│   └── settings.py             # Project settings
├── output.csv                  # Example output file
├── scrapy.cfg                  # Scrapy configuration
└── README.md                   # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- [Scrapy](https://scrapy.org/)

### Installation

1. **Clone the repository:**
	```sh
	https://github.com/sankesh16/PropertyFinder.git
	cd PropertyFinder
	```

2. **Install dependencies:**
	```sh
	pip install scrapy
	```

### Usage

Run the main spider to start scraping:

```sh
scrapy crawl property_finder -o output.csv
```

This command will execute the spider and save the scraped data to `output.csv`.

## Customization

- **Spiders:** Add or modify spiders in the `propertyfinder/spiders/` directory to target different propertyfinder domains or listing types.
- **Pipelines:** Adjust `pipelines.py` to process or clean data as needed.
- **Settings:** Configure crawling behavior in `settings.py`.

## Output

The scraped data is saved in CSV format, making it easy to import into Excel, databases, or analytics tools.



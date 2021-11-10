# HKHairSalon Crawler / Spider
It's a Crawler / Spider for crawling company data on [HKHairSalon](https://hkhairsalon.com/), it written in Python with Scrapy.

## Installation guide for packages

You should be install the [Scrapy](https://scrapy.org/) first, other packages (e.g. csv, datetime) should be installed by default.

You can check all the packages by the following command:
```sh 
pip3 list
```

Outputs: 
```sh
Package            Version
------------------ ---------
Scrapy             2.5.0
...                ...
```

If `Scrapy` is not on the list, you need to install it by:
```sh
pip3 install scrapy
```

### Required packages

Required Package|
----------------|
csv             |
datetime        |
scrapy          |

### Development Environment
Tools   | Version
--------|--------
Python  | 3.9.6

## Run the cralwer
You can run the crawler by following command, it will crawl the HK Hair Salon with default type **1** which *is __髮型師__*:
```sh
scrapy crawl hairsalon_spider
```

However, you can pass any type (e.g. 1 for 髮型師, 2 for 髮型屋) to it with the `-a` custom arugment flag (e.g. `-a type={type}`)
```sh
scrapy crawl hairsalon_spider -a {type=TYPE_TO_BE_SEARCH}
```

## Output files
The crawler will generate the result csv files with filename format `hkhairsalon_YYYYMMDD_HHmmss.csv` when each crawl.

## Development Roadmap
- **Search**: Search by Type     (Under development)
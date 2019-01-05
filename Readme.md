# Email Crawler
This project mines websites to find email addresses.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
In order to manually install __Email Crawler__ you'll need Python2.x installed on your system, as well as the Python package manager, pip. You can check if you have these already installed from the command line:
```bash
$ python --version
Python 2.7.2
$ pip --version
pip 10.0.1
```

If pip is installed in your system then you must have installed some libraries of Python2 .
```bash
$ sudo pip install sqlalchemy
$ sudo pip install -U setuptools
```

### Installing
For installing this project you just need to download the source files.

### Running
Go into project directory and run command below

```bash
$ python2 email_crawler.py "keyword" 10
```
"keyword" - String that will be searched on Google

10 - The number of websites that will be chosen from search results on Google for cwawling.

#### Get Crawled emails
```bash
$ python2 email_crawler.py --emails
```
or
```bash
$ python2 email_crawler.py -e
```

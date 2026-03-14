# Scrapy Login Scraper

A Python web scraper that authenticates into a login-protected website and extracts structured data.

## Features
- Handles session-based login with automatic CSRF token extraction
- Scrapes paginated content across 10 pages (100+ records)
- Custom data pipeline for cleaning, deduplication and validation
- Outputs structured JSON

## Tech Stack
Python · Scrapy · CSS Selectors · JSON

## How To Run
pip install scrapy
scrapy crawl login_quotes

Btw - delete quotes.db and logged_in_quotes.csv and quotes_clean.json because the codes in the pipeline will create them. 

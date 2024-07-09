import csv
import requests
import wikipediaapi
from flask import Flask, request, render_template
import threading
import time
import os.path


app = Flask(__name__)
wiki = wikipediaapi.Wikipedia('en')
CACHE_FILE = 'cache.csv'
path = './cache.csv'


def load_cache():
    if (not os.path.isfile(path)):

        with open(CACHE_FILE, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['visited_urls', ''])

    try:
        with open(CACHE_FILE, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            cache = dict(reader)
        return cache
    except FileNotFoundError:
        return {}


def save_cache(cache):

    with open(CACHE_FILE, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(cache.items())


cache = load_cache()
visited_urls = list(cache['visited_urls'])


@app.route('/')
def wiki_route():
    page_link = request.args.get('link')
    if not page_link:
        return 'Please provide a Wikipedia page link as http://localhost:5000/?link= wikipedia-page-link '
    page_name = page_link.split('/')[-1]
    visited_urls.append(page_link)
    cache['visited_urls'] = str(visited_urls)
    if page_name in cache:
        return cache[page_name]
    else:
        try:
            page = wiki.page(page_name)
            if page.exists():
                text = page.text
                cache[page_name] = text
                save_cache(cache)
                return text
            else:
                return f'The page "{page_name}" does not exist.'
        except requests.exceptions.RequestException as e:
            return f'Error: {e}'


@app.route('/visited')
def visited_route():
    return visited_urls


if __name__ == '__main__':
    app.run()

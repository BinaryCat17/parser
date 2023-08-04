import context as _
import urllib.request
import time
import urllib.request
import re
from bs4 import BeautifulSoup

def process_page(l, html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1', class_='article__header__title-in js-slide-title')
    if not title:
        print('Error')
        return
    
    with open(f'workspace/resources/news/html/{title.text.strip()}.html', 'w') as f:
        print(soup.prettify(), file=f)


    article_text = soup.find('div', class_='article__text')
    article_overview = soup.find('div', class_='article__text__overview')
    article_authors = soup.find('div', class_='article__authors')
    article_date = soup.find('time', class_='article__header__date')

    author_names = []
    if article_authors is not None:
        for a in article_authors.find_all('span', class_='article__authors__author__name'):
            author_names.append(a.text)
        
    texts = article_text.find_all('p') or article_text.find_all('ul')


    with open(f'workspace/resources/news/text/{title.text.strip()}.txt', 'w') as f:
        print(f'Дата: {article_date.attrs["content"]}', file=f)
        print(f'СМИ: РБК', file=f)

        if article_overview is not None:
            print(article_overview.text.strip(), file=f)
    
        for t in texts:
            if t.parent == article_text:
                if t.text.count('\n') < 3:
                    print(t.text, file=f)

        if len(author_names) > 0:
            print('Авторы: ', end='', file=f)
            for n in author_names:
                print(n, end='', file=f)
            print(file=f)
        else:
            print('Авторы: Не указаны', file=f)


def process_news_list(i, html):
    soup = BeautifulSoup(html, 'html.parser')
    with open(f'workspace/resources/pages/html/{i}.html', 'w') as f:
        print(soup.prettify(), file=f)
        for l in soup.find_all('a', class_='\\"item__link'):
            with urllib.request.urlopen(l.attrs['href'][2:-2]) as p:
                phtml = p.read().decode('utf-8')
                process_page(l.attrs['href'][2:-2], phtml)


def list_news(category):
 for i in range(0, 1000, 12):
    url = f"https://www.rbc.ru/v10/ajax/get-news-by-filters/?category={category}&offset={i}&limit=12"
    with urllib.request.urlopen(url) as f:
        html = f.read().decode('utf-8')
        process_news_list(i, html)
    time.sleep(0.2)


def run():
    list_news('politics')


if __name__ == '__main__':
    run()
import os
import string
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.nature.com'
page_cnt = int(input())
searching_category = input()
url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'

for page_num in range(1, page_cnt + 1):
    response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'}, params={'page': page_num})
    folder_name = f'Page_{page_num}'
    if response:
        os.mkdir(folder_name)

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            article_type = article.find('span', {'class': 'c-meta__type'}).text
            if article_type == searching_category:
                article_link = base_url + article.find('a', {'data-track-action': 'view article'}).get('href')

                response = requests.get(article_link)
                soup = BeautifulSoup(response.content, 'html.parser')

                article_title = soup.find('title').text
                article_content = soup.find('article').find('p', class_='article__teaser').text

                article_title_words = article_title.split()
                for index, word in enumerate(article_title_words):
                    for punctuation in string.punctuation:
                        if punctuation in word:
                            new_word = word.replace(punctuation, '')
                            article_title_words[index] = new_word

                article_title = "_".join(article_title_words)

                with open(f'{folder_name}/{article_title}.txt', 'w', encoding='utf-8') as f:
                    f.write(article_content)

    else:
        print(f'The URL returned {response.status_code}!')
print('Saved all articles.')

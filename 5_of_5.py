import requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import json
import string
import os


def get_movie(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    # # soup.find('title')
    # # p = soup.find('script', {'type':'application/ld+json'})
    # pp = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
    # print(pp['name'])
    # # print(pp['description'])
    # name = soup.find('title').contents
    info = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
    name = info['name']
    # desc = info['trailer']['description']
    wat = (soup.find("div", {"class": "summary_text"}))
    desc = wat.get_text(strip=True)
    # description = soup.find('div', {'class': "summary_text"}).contents
    answer = {"title": name, "description": desc}
    return answer


def get_write_content(url, r):
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    page_content = requests.get(url).content
    source_file = open("source.html", "wb")
    try:
        if r:
            source_file.write(page_content)
            print("Content saved")
        else:
            print("The URL returned %s" % r.status_code)
    except:
        print("wat The URL returned %s" % r.status_code)
    source_file.close()


def save_content(tag_content, N):
    # saves content to txt file
    # article_title %.txt

    article_name_with_punc_and_spaces = str(tag_content.find("a").next)  # .text.strip()?
    article_name_with_spaces = article_name_with_punc_and_spaces.translate(str.maketrans('', '', string.punctuation))
    trans = str.maketrans({' ': '_', '_': ' '})
    article_name = article_name_with_spaces.translate(trans)
    article_link = "https://www.nature.com" + tag_content.find("div", {"class": "c-card__body u-display-flex u-flex-direction-column"}).a.get('href')
    filename = "Page_" + str(N)
    os.makedirs(filename, exist_ok=True)
    article_content_file = open(article_name + ".txt", "w", encoding='UTF-8')
    page_content = requests.get(article_link).content
    html_page_content = BeautifulSoup(page_content, 'html.parser')
    body = html_page_content.find('div', class_='article-item__body').text.strip()  # article_soup.find("article").text.strip()
    article_content_file.write(body)
    # Replace the whitespaces with underscores
    # remove punctuation marks in the filename
    # (str.maketrans &&& string.punctuation ).
    # strip all trailing whitespaces in the article body and title.
    # soup.find('div', class_='article__body').text.strip()
    article_content_file.close()
    return article_name, article_content_file


#
# def article_name_extractor(tag_content):
#     return tag_content.find("a").next


if __name__ == "__main__":
    url = "https://www.nature.com/nature/articles"  # input()
    N = int(input())
    Article_type = input()
    page_content = requests.get(url).content
    html_page_content = BeautifulSoup(page_content, 'html.parser')
    possible_articles = html_page_content.find_all('article')
    counter = 0
    for result_set in possible_articles:
        if Article_type == result_set.find_all("span", {"class": "c-meta__type"})[0].next:
            save_content(result_set, N)
            counter = counter + 1
            if counter == N:
                print("saved ", N, "articles")
                break

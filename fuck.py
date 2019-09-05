import requests
from bs4 import BeautifulSoup
from Article import Article
from Util import setArticleHead

search_url = "http://zhtnbzz.yiigle.com/search.jspx?q=%E6%AF%8D%E4%B9%89%E6%98%8E"
res = requests.get(search_url)
html = res.text
bs = BeautifulSoup(html, 'lxml')
page_url = bs.select('div.result_list a[href^="http://zhtnbzz.yiigle.com/CN"]')
url_list = []
article_list = []
for link in page_url:
    href = link.get("href")
    detail = requests.get(href)
    if detail.status_code == 200:
        newArticle = Article()
        detail_text = detail.text
        bs = BeautifulSoup(detail_text, 'lxml')
        article_title = [bs.select("div.main_title")[0].get_text()]
        newArticle.setTitle(article_title)

        # print("length of fuck: %d" % (len(fuck)))
        authors = bs.select("div.article_authors span")
        # 添加作者信息
        for author in authors:
            # print(author.string)
            newArticle.setAuthor(author.string)
        article_list.append(newArticle)

        article_abstract_mid = bs.select("div.article_abstract_mid div.sec")
        setArticleHead(article_abstract_mid, newArticle, bs)
        # print(newArticle)

    else:
        print("Error in url")
        print(detail.url)

print("length: %d" % (len(article_list)))

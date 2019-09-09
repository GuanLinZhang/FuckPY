import requests
from bs4 import BeautifulSoup
import Article

base_query_url = "http://zhtnbzz.yiigle.com/search.jspx?q="
requestParam = "%E6%AF%8D%E4%B9%89%E6%98%8E"
fuck = Article.getArticlesByPages(base_query_url, requestParam)
print(len(fuck))
for m in fuck:
    print(m)

import time

import requests
from pymongo.errors import BulkWriteError

import mongoDB
from bs4 import BeautifulSoup


class Article:
    def __init__(self, title='', authors=None, summary='', target='', result='', method='', conclusion=''):
        if authors is None:
            authors = []
        self.title = title
        self.authors = authors
        self.summary = summary
        self.target = target
        self.result = result
        self.method = method
        self.conclusion = conclusion

    def setTitle(self, title):
        self.title = title

    def setAuthors(self, authors):
        self.authors = authors

    def setAuthor(self, author):
        self.authors.append(author)

    def setSummary(self, summary):
        self.summary = summary

    def setTarget(self, target):
        self.target = target

    def setResult(self, result):
        self.result = result

    def setMethod(self, method):
        self.method = method

    def setConclusion(self, conclusion):
        self.conclusion = conclusion

    def __str__(self):
        return "文章: {\n 标题: %s\n 作者: %s\n 总结: %s\n 目的: %s\n 结果: %s\n 方法: %s\n " \
               "结论: %s\n} " % \
               (self.title, self.authors, self.summary, self.target, self.result, self.method, self.conclusion)


def getLargestPageNumber(bs):
    """
    获取所查找最大页码
    :param bs: BeautifulSoup实例
    :return: 返回最大页码
    """
    return bs.select("select option")[-1].get_text()


def getAllArticles(encodedRequestParam):
    """
    根据查询字符串查找全部文章 包含跳转下一页操作
    :param encodedRequestParam: 查询字符串编码后的请求参数值
    :return: 返回全部文章列表
    """

    base_search_url = "http://zhtnbzz.yiigle.com/search.jspx?q="
    # 拼接查询字符串
    search_url = base_search_url + encodedRequestParam
    # 设置请求头 并发送请求
    host = 'zhtnbzz.yiigle.com'
    # 设置user-agent
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko)' \
                 ' Chrome/76.0.3809.132 Safari/537.36'
    # 发送GET请求,并取得HTML文本
    first_page_text = requests.get(search_url,
                                   headers={'Host': host,
                                            'User-Agent': user_agent},
                                   allow_redirects=False).text
    # 声明BeautifulSoup实例
    bs = BeautifulSoup(first_page_text, 'lxml')
    # 声明文章List
    article_list = []
    # 追加首页文章列表到List
    article_list.extend(getSinglePageArticles(first_page_text))
    # 获取最大页码
    lg_num = int(getLargestPageNumber(bs))
    # 判断如大于1页,则访问下一页并请求数据
    if lg_num > 1:
        count = 2
        # 获取1 - lg_num
        page_count = range(1, lg_num)
        for index in page_count:
            # 拼接查询下一页字符串URL
            next_url = "http://zhtnbzz.yiigle.com/search_{}.jspx?q={}".format(count, encodedRequestParam)
            count += 1
            # 获取下一页HTML文本
            next_page_text = requests.get(next_url).text
            single_page_articleList = getSinglePageArticles(next_page_text)
            # 持久化到MongoDB
            db = mongoDB.conn()
            t_article = db.Articles
            try:
                t_article.insert_many(article_list)
            except BulkWriteError as bwe:
                print(bwe.details)
            # 追加到已有结果List
            article_list.extend(single_page_articleList)
            # 延迟5s
            time.sleep(3)
            # 追加到结果List

    return article_list


def getSinglePageArticles(page_text):
    """
    获取单页文章列表数据
    :param page_text:  单页文章列表html
    :return: 返回单页文章列表
    """
    # 初始化bs实例
    bs = BeautifulSoup(page_text, 'lxml')
    article_list = []
    getLargestPageNumber(bs)
    # 获得列表内所有的URL列表
    link_list = bs.select('div.result_list a[href^="http://zhtnbzz.yiigle.com/CN"]')

    for link in link_list:
        # 拿到链接地址
        href = link.get("href")
        # 发送GET请求 拿到HTML页
        page = requests.get(href)
        # 请求成功
        if page.status_code == 200:
            newArticle = setArticle(page.text)
            article_list.append(newArticle)
        else:
            print("Error in url")
            print(page.url)

    return article_list


def setArticle(article_text):
    # print("page: %s" % page.get_text()
    bs = BeautifulSoup(article_text, 'lxml')
    # 声明Article实例
    newArticle = Article()
    # 设置文章标题
    setArticleTitle(bs, newArticle)
    # 设置文章作者
    setArticleAuthors(bs, newArticle)
    # 设置文章摘要
    setArticleAbstract(bs, newArticle)
    # 返回新创建的Article实例

    print(newArticle)
    return vars(newArticle)


def setArticleTitle(bs, newArticle):
    # 获取文章标题
    article_title = bs.select("div.main_title")[0].get_text().replace('\n', '').replace('\t', '')
    # 设置文章标题
    newArticle.setTitle(article_title)


def setArticleAuthors(bs, newArticle):
    # 添加作者信息
    authors_span = bs.select("div.article_authors span")
    article_authors = []
    for author_span in authors_span:
        article_authors.append(author_span.get_text())

    newArticle.setAuthors(article_authors)


def setArticleAbstract(bs, newArticle):
    # 获取文章摘要列表
    abstract_sections = bs.select("div.article_abstract_mid div.sec")
    # 遍历所有<div class=sections>元素
    # 如存在span子元素,则根据title设置对应的文本
    # 否则 则表明sections中只有单一段落存在
    for sec in abstract_sections:
        span = sec.span
        if span is not None:
            title = span.string
            para = span.next_sibling

            if title == "目的":
                newArticle.setTarget(para.get_text())
            elif title == "方法":
                newArticle.setMethod(para.get_text())
            elif title == "结果":
                newArticle.setResult(para.get_text())
            elif title == "结论":
                newArticle.setConclusion(para.get_text())
        else:
            summary = sec.p.get_text()
            newArticle.setSummary(summary)

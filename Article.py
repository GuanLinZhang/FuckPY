import requests
from bs4 import BeautifulSoup
from selenium import webdriver


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


def getArticlesByPages(base_search_url, encodedRequestParam):
    search_url = base_search_url + encodedRequestParam
    first_page_text = requests.get(search_url).text
    bs = BeautifulSoup(first_page_text, 'lxml')

    article_list = []
    article_list.extend(getArticlesBySinglePage(first_page_text))

    lg_num = int(getLargestPageNumber(bs))
    if lg_num > 1:
        count = 2
        page_count = range(1, lg_num)
        for index in page_count:
            next_url = "http://zhtnbzz.yiigle.com/search_{}.jspx?q={}".format(count, encodedRequestParam)
            count += 1
            next_page_text = requests.get(next_url).text

            article_list.extend(getArticlesBySinglePage(next_page_text))

    return article_list


def getArticlesBySinglePage(page_text):
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
    #
    # # print(article_list)
    # # print("len: %d" % len(article_list))
    # for article in article_list:
    #     print(article)
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
    return newArticle


def setArticleTitle(bs, newArticle):
    # 获取文章标题
    article_title = bs.select("div.main_title")[0].string.replace('\n', '')
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

    # print(article)

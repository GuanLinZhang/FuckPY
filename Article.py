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

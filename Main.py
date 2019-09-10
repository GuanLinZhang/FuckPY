import urllib.parse

import Article

word = input('请输入文题/作者/关键字\n')
#
requestParam = urllib.parse.quote(word)

fuck = Article.getAllArticles(requestParam)
for m in fuck:
    print(m)
print("共有: {}条数据", len(fuck))

def setArticleHead(sections, article, bs):
    for sec in sections:
        setBeanByTitle(sec, article)
    print(article)


def setBeanByTitle(sec, article):
    span = sec.span
    # print(sec)
    if span is not None:
        title = span.string
        # print(title.string)
        para = span.next_sibling
        # if content.i:
        #     print(content.i)
        if para.i is not None:
            # print(para.i)
            getFormattedParagraph(para)
        if title == "目的":
            article.setTarget(para.string)
        elif title == "方法":
            article.setMethod(getFormattedParagraph(para))
        elif title == "结果":
            article.setResult(getFormattedParagraph(para))
        elif title == "结论":
            article.setConclusion(para.string)
    else:
        summary = sec.p.string
        # print("summary" + summary)
        article.setSummary(summary)


def getFormattedParagraph(para):
    # print(p)
    if para.i:
        # print("para.i: %s" % para.i)
        iconList = para.findAll('i')
        for icon in iconList:
            icon.unwrap()

        print(para)

from pygooglenews import GoogleNews
from dateutil import parser as date_parser
from Config_WTTJ import get_list, get_companie_name, update_news, verif_news

gn = GoogleNews(lang='fr', country='FR')


def get_news(search_term):
    stories = []
    search = gn.search(search_term)
    newsitem = search['entries']
    for item in newsitem:
        # print(item)
        story = {'title': item.title,
                 'link': item.link,
                 'published': date_parser.parse(item.published),
                 'source': item.source['title']}
        stories.append(story)
        print(story)
    return stories


L = get_list()
for i in range(0, len(L)):
    name = get_companie_name(L[i]['url'])
    if name is not None:
        news = get_news(name)
        for new in news:
            if not verif_news(new):
                new.update({"name": name, "url_linkedin": L[i]['url']})
                update_news(new)

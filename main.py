from selenium import webdriver
import pymongo
from time import sleep
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from difflib import SequenceMatcher


from Config_WTTJ import get_list, get_companie_name , update_jobs , update_companie , verif_companie,verif_post
from wttj import get_url, get_informations_companie, get_information_post, get_url_posts

L = get_list()
print(L.index({'url': "https://www.linkedin.com/company/1292855/"}))

for i in range(762, len(L)):
    print(L[i]['url'])
    isScraped = verif_companie(L[i]['url'])
    print('is scraped: ', isScraped)
    if not isScraped:
        name = get_companie_name(L[i]['url'])
        if name is not None:
            h = get_url(name)
        if h != "":
            k = {"name": name, "url_linkedin": L[i]['url']}
            g = get_informations_companie(h)
            k.update(g)
            update_companie(k)
            print(k)
            n = {"name": name, "url_linkedin": L[i]['url']}
            listp = get_url_posts(h)
            print(listp)
            for clé, valeur in listp.items():
                print(clé, valeur)
                j = get_information_post(clé, valeur)
                j.update(n)
                print(j)
                update_jobs(j)
        else:
            print(name,':lentreprise nexiste pas')

# L = get_list()
# for i in L:
#     print(i['url'])
#     isScraped = verif_companie(i['url'])
#     print('is scraped: ', isScraped)
#     if not isScraped:
#         name = get_companie_name(i['url'])
#         if name != None:
#             h = get_url(name)
#         if h != "":
#             k = {"name": name, "url_linkedin": i['url']}
#             g = get_informations_companie(h)
#             k.update(g)
#             update_companie(k)
#             print(k)
#             n = {"name": name, "url_linkedin": i['url']}
#             listp = get_url_posts(h)
#             print(listp)
#             for clé, valeur in listp.items():
#                 print(clé, valeur)
#                 j = get_information_post(clé, valeur)
#                 j.update(n)
#                 print(j)
#                 update_jobs(j)
#         else:
#             print(name ,':lentreprise nexiste pas')
    # elif isScraped:
    #     name = get_companie_name(i['url'])
    #     h = get_url(name)
    #     n = {"name": name, "url_linkedin": i['url']}
    #     listp = get_url_posts(h)
    #     print(listp)
    #     for clé, valeur in listp.items():
    #         result = verif_post(clé)
    #         if (result is None) or (result is not None and result['posting_date'] != valeur):
    #             j = get_information_post(clé, valeur)
    #             j.update(n)
    #             print(j)
    #             update_jobs(j)


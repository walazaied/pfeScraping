from pymongo import MongoClient

try:
    client = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = client['db']
company_profiles = db.company_profiles
jobs_wttj = db.jobs_wttj
scraped_companies_wttj = db.scraped_companies_wttj
news = db.news
Funding = db.Funding


def verif_companie(url):
    result1 = db.scraped_companies_wttj.find_one({"name": get_companie_name(url)})
    result2 = db.scraped_companies_wttj.find_one({"url_linkedin": url})
    if (result1 is None) and (result2 is None):
        return False
    else:
        return True


def verif_post(url):
    result = db.jobs_wttj.find_one({"url_post": url})
    return result


def get_list():
    companies_url = db.company_profiles.find({}, {"_id": 0, "url": 1})
    n = db.company_profiles.count_documents({})
    L = []
    for i in range(0, n):
        L.append(companies_url.next())
    return L


def get_companie_name(url):
    companie_name = db.company_profiles.find_one({"url": url}, {"_id": 0, "overview.name": 1})
    return companie_name['overview']['name']


def update_jobs(document):
    db.jobs_wttj.insert_one(document)


def update_news(document):
    db.news.insert_one(document)


def update_funding(document):
    db.Funding.insert_one(document)


def update_companie(document):
    db.scraped_companies_wttj.insert_one(document)


def verif_news(document):
    result = db.news.find_one({"title": document['title']})
    return result


def verif_Funding(url):
    result1 = db.Funding.find_one({"name": get_companie_name(url)})
    result2 = db.Funding.find_one({"url_linkedin": url})
    if (result1 is None) and (result2 is None):
        return False
    else:
        return True


def get_infos(name):
    r = db.company_profiles.find_one({"overview.name": name})
    if "website" in r['overview']:
        website = r['overview']['website']
        return website
    else:
        return ""


def get_titles_news():
    news = db.news.find({}, {"_id": 0, "title": 1})
    n = db.news.count_documents({})
    L = []
    for i in range(0, n):
        L.append((((news.next())['title']).split(" - "))[0])
    return L


import datetime as dt
from difflib import SequenceMatcher
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from jobclassifier import get_result_classification

options = Options()
options.add_argument("enable-automation")
options.add_argument("disable-infobars")
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)


def get_url(companie):
    url = "https://www.welcometothejungle.com/fr/companies?query=" + companie + "&page=1&aroundQuery="
    driver.get(url)
    sleep(30)
    string = driver.find_element_by_css_selector('section[class="hdl9e2-6 MJQFe"]').find_element_by_css_selector('h2')
    result = str(string.text)
    href = ""
    if result[0] != '0':
        comp = driver.find_element_by_css_selector('li[class="ais-Hits-list-item"]').find_element_by_css_selector(
            'span[class="ais-Highlight sc-1s0dgt4-13 guUpAr"]')
        name = comp.text
        seq = SequenceMatcher(None, companie.lower(), name.lower())
        if seq.ratio() > 0.85:
            link = driver.find_element_by_css_selector('li[class="ais-Hits-list-item"]').find_element_by_css_selector(
                'a')
            href = link.get_attribute('href')

    return href


def get_technologies(URL):
    url = URL + "/tech"
    driver.get(url)
    sleep(15)
    L = driver.find_elements_by_css_selector('div[class="sc-1h14x9p-1 zLvUp"]')
    dic = {}
    j = 0
    for i in L:
        S = []
        j = j + 1
        sleep(3)
        try:
            type_tech = i.find_element_by_css_selector('h4[class="sc-1h14x9p-3 hYgNVJ"]').text
            t = i.find_elements_by_css_selector('h5[class="sc-1tnit22-4 kmPPYC"]')
            p = i.find_elements_by_css_selector('span[class="sc-1tnit22-7 eCXgvk"]')
            for tech in t:
                S.append(tech.text)
            dic[type_tech] = S
        except:
            sleep(3)
        if j <= (len(L) - 3):
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'i[class="sc-kmASHI ijAtcs"]'))
                )
                element.click()

            except:
                driver.quit()

    return dic

    # sleep(10)
    # L = driver.find_elements_by_css_selector('div[class="sc-1h14x9p-1 zLvUp"]')
    # for i in L:
    #     pourcentage = []
    #     s = i.find_elements_by_css_selector('span[class="sc-1tnit22-7 eCXgvk"]')
    #     for p in s:
    #         pourcentage.append(p.text)
    #     print(pourcentage)


def get_informations_companie(URL):
    driver.get(URL)
    sleep(15)
    general_info = {}

    try:
        website = driver.find_element_by_css_selector('ul[class="sc-1qc42fc-4 iZuMaX"]').find_element_by_css_selector(
            'a').get_attribute('href')
    except:
        website = ""
    try:
        domaine = driver.find_element_by_css_selector('ul[class="sc-1qc42fc-4 iZuMaX"]').find_element_by_css_selector(
            'span[class="sc-1qc42fc-2 inlzGd"]').text
    except:
        domaine = ""
    try:
        localisation = driver.find_element_by_css_selector(
            'ul[class="sc-1qc42fc-4 iZuMaX"]').find_element_by_css_selector(
            'span[class="sc-1qc42fc-2 bzTNsD"]').text
    except :
        localisation = ""
    try:
        d = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="sc-11obzva-1 sc-2zd334-2 hWHArS hOKwfe"]'))
        )
        description = d.text
    except:
        description=''

    try:
        info = driver.find_element_by_css_selector('ul[class="sc-1n18lhk-0 kyXqKa"]').find_elements_by_css_selector(
        'li[class="sc-1n18lhk-1 gNjfoM"]')

        for i in info:
            a = i.find_element_by_css_selector('h4[class="sc-1n18lhk-2 kuSzGH"]').find_element_by_css_selector('span').text
            b = i.find_element_by_css_selector('span[class="sc-1n18lhk-3 bWFoBD"]').text
            general_info[a] = b
    except:
        pass

    overview = {"url_wttj": URL,
                "website": website,
                "secteur": domaine,
                "location": localisation,
                "description": description}
    overview.update(general_info)
    overview["technologies"] = get_technologies(URL)
    overview["scraped_time"] = dt.datetime.now()
    return overview


def get_url_posts(URL):
    url = URL + "/jobs"
    driver.get(url)
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h3[class="sc-1mxdn37-4 fRYaBz"]'))
        )
        job_number_response = element.text
        job_number = int(job_number_response[0: job_number_response.find(" ")])
    except:
        job_number = 0
    exact_page_nb = job_number / 30
    min_page_nb = job_number // 30

    if exact_page_nb > min_page_nb:
        page_nb = min_page_nb + 2
    elif exact_page_nb == min_page_nb:
        page_nb = min_page_nb + 1

    offers = {}
    for i in range(1, page_nb):
        sleep(6)
        results = driver.find_element_by_css_selector(
            'div[origin="company-jobs-results"]').find_elements_by_css_selector('div[class="sc-7dlxn3-5 djGVHr"]')
        for res in results:
            a = res.find_element_by_css_selector('a').get_attribute('href')
            time = res.find_element_by_css_selector('time').get_attribute('datetime')
            offers[a] = time
        try:
            element = driver.find_element_by_css_selector('div[class="ais-Pagination"]').find_element_by_css_selector(
                'li[class="ais-Pagination-item ais-Pagination-item--nextPage"]')
            button = element.find_element_by_css_selector('a')
            button.click()
        except:
            pass
    return offers


def get_information_post(href, date_posting):
    driver.get(href)
    sleep(10)
    post = driver.find_element_by_css_selector('h1[class="sc-12bzhsi-3 fhlSDH"]').text
    post_class = get_result_classification(post)
    d = driver.find_element_by_css_selector('section[data-t="lzbv24"]').find_element_by_css_selector(
        'div[class="sc-11obzva-1 hWHArS"]')
    description_post = d.text

    dic = {"url_post": href, "post": post, "post_class": post_class, "description_post": description_post}
    try:
        elements = WebDriverWait(driver, 6).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class="sc-1qc42fc-0 dCLcWq"]'))
        )

    except:
        driver.quit()
    try:
        for info in elements:
            a = info.find_element_by_css_selector('span[class="sc-1qc42fc-3 jkVkMU"]').find_element_by_css_selector(
                'i').get_attribute('name')
            b = info.find_element_by_css_selector('span[class="sc-1qc42fc-2 bzTNsD"]').text
            if a == 'education_level' and ('Bac' or 'Master' or 'Doctorat') not in b:
                a = 'experience'
            dic[a] = b
    except:
        pass

    dic['posting_date'] = date_posting
    dic["scraping_date"] = dt.datetime.now()

    if 'contract' in dic:
        del dic['contract']
    if 'salary' in dic:
        del dic['salary']
    if 'clock' in dic:
        del dic['clock']
    if 'write' in dic:
        del dic['write']

    return dic

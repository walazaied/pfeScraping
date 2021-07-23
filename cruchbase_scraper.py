from selenium import webdriver
from difflib import SequenceMatcher
from selenium.webdriver.chrome.options import Options
from time import sleep
from Config_WTTJ import get_infos, get_list, get_companie_name, update_funding, verif_Funding

options = Options()
options.add_argument("enable-automation")
options.add_argument("disable-infobars")
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)


def get_url(companie):
    w = get_infos(companie)
    url = 'https://www.crunchbase.com/textsearch?q=' + companie
    driver.get(url)
    LINKS = []
    try:
        sleep(4)
        links = driver.find_element_by_css_selector(
            'div[class="body-wrapper"]').find_elements_by_css_selector(
            'a[role="link"]')

        for link in links:
            LINKS.append(link.get_attribute('href'))

        for LINK in LINKS:
            driver.get(LINK)
            sleep(3)
            try:
                website = driver.find_element_by_css_selector('a[class="component--field-formatter layout-row '
                                                          'layout-align-start-end link-accent '
                                                          'ng-star-inserted"]').get_attribute('href')
            except:
                website = ""

            seq = SequenceMatcher(None, website, w)
            if seq.ratio() > 0.80:
                return LINK

        return ""
    except:
        return ""

def get_company_financials(url):
    URL = url + '/company_financials'
    driver.get(URL)
    sleep(3)
    dic = {}
    Highlights = {}
    Fundings = ""
    for item in driver.find_elements_by_css_selector('div[class="spacer ng-star-inserted"]'):
        label = item.find_element_by_css_selector('label-with-info').text
        valeur = item.find_element_by_css_selector('field-formatter').text
        Highlights[label] = valeur
    print('Overview  :', Highlights)
    dic['Overview'] = Highlights
    try:
        Fundingss = driver.find_elements_by_css_selector('div[class="one-of-many-section ng-star-inserted"]')
        F = Fundingss[1].find_elements_by_css_selector("phrase-list-card")
        for f in F:
            Fundings= Fundings + str(f.text)
            dic['Fundings'] = Fundings
    except:
        pass
    tables = driver.find_elements_by_css_selector('row-card[class="ng-star-inserted"]')
    for table in tables:
        sleep(5)
        title = table.find_element_by_css_selector('h2[class="section-title"]').text
        th = []
        for i in table.find_elements_by_css_selector('th'):
            th.append(i.text[0:-2])
        Funding_Rounds = []
        for tr in table.find_elements_by_css_selector('tr[class="ng-star-inserted"]'):
            row_dic = {}
            i = 0
            for td in tr.find_elements_by_css_selector('td[class="ng-star-inserted"]'):
                row_dic[th[i]] = td.text
                i = i + 1
            Funding_Rounds.append(row_dic)
        print(title, ':', Funding_Rounds)
        dic[title] = Funding_Rounds
    return dic
    driver.quit()


if __name__ == '__main__':

    L = get_list()
    for i in range(5800, len(L)):
        name = get_companie_name(L[i]['url'])
        if name is not None and verif_Funding(L[i]['url']) is False:
            url = (get_url(name))
            if url != "":
                print(url)
                F = get_company_financials(url)
                if (F is not None) and ("Funding Rounds" in F or "Investors " in F or "Investments" in F ):
                    F.update({"name": name, "url_linkedin": L[i]['url'], "url": url + "/company_financials"})
                    update_funding(F)

import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dbf_reader import queries
from xlsx_writer import write_to_file

WIKIPEDIA_URL = "https://sv.wikipedia.org/wiki/Portal:Huvudsida"
BROWSER_DRIVER_PATH = "C:/Program Files (x86)/chromedriver.exe"
WIKI_PAGE_REGEX_PATTERN = r"\/wiki\/"

driver = webdriver.Chrome(BROWSER_DRIVER_PATH)

def next_query(query):
    searchbar = driver.find_element_by_id("searchInput")
    searchbar.send_keys(query)
    searchbar.send_keys(Keys.RETURN)


def is_on_wiki_page():
    return bool(re.search(WIKI_PAGE_REGEX_PATTERN, driver.current_url))


def go_to_wiki_page():
    parent = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "mw-search-result-heading"))
    )
    link = parent.find_element_by_tag_name("a")
    sleep(1)
    link.click()


def go_to_geohack_page():
    link = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.external.text"))
    )
    sleep(1)
    link.click()


def get_text(el):
    return el.text


def get_lat_lng():
    WebDriverWait(driver, 8).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "th#Coordi"), "Koordinater")
    )
    parent = driver.find_element_by_css_selector("span.geo")
    lat_lng = list(map(get_text, parent.find_elements_by_tag_name("span")))
    return lat_lng


def get_name_from_query(query):
    words_list = query.split(" ")
    words_list.pop()

    if len(words_list) > 1:
        return " ".join(words_list)

    return words_list[0]


def scrape():
    driver.implicitly_wait(3)
    driver.get(WIKIPEDIA_URL)

    for query in queries:
        print(f"current query: {query}")
        next_query(query)

        if not is_on_wiki_page():
            go_to_wiki_page()

        go_to_geohack_page()
        lat, lng = get_lat_lng()
        name = get_name_from_query(query)

        write_to_file(name, lat, lng)

        driver.back()


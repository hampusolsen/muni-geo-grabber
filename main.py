from web_scraper import scrape
from xlsx_writer import save_file

try:
    scrape()
finally:
    save_file()

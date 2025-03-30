
from recipe_scrapers import scrape_me


#the main method that takes the URL and scrapes it, returns the recipe JSON
def scrape(urlp):
    scraper = scrape_me(urlp)
    return scraper.to_json()




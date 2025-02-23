from recipe_scrapers import scrape_me

scraper = scrape_me("https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/")
scraper.title()
scraper.instructions()
print(scraper.to_json())
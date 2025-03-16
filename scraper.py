
from recipe_scrapers import scrape_me


#the main method that takes the URL and scrapes it, returns the recipe JSON
def scrape(urlp):
    print("inside scrape")
    scraper = scrape_me(urlp)
    print("scraper")
    print(scraper)
    return scraper.to_json()


#writes passed text into file with filename that is passed
def write_text_to_file(text, filename):
    f = open(filename, 'w')
    f.write(text)
    f.close()


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts) 
    return u" ".join(t.strip() for t in visible_texts)


def extract_ingredients(text):
    #Currently following regex is used to extract ingredients text:
    #(?<=Ingredients)?▢.*(?=Instructions)
    #it can be tested at https://regex101.com/
    #it's a bad regex, because it will not work for other websites. 
    ingredients_text = re.search(r"(?<=Ingredients)?▢.*(?=Instructions)", text).group(0)
    ingredients_list = re.split("▢ ", ingredients_text)
    ingredients_list = [ingredient.strip() for ingredient in ingredients_list if ingredient.strip()]

    return ingredients_list


def extract_title(text):
    title_text = re.search(r"(?<=Recipe Index\s\s\|\s\s)(.*?)(?=\sRobyn)", text).group(0)
    title_text = title_text[title_text.index("Recipe") + 8:]

    return title_text

def extract_preptime(text):
    preptime_text = re.search(r"(?<=Prep Time:\s)(.*?)(?=\s\sminutes)", text).group(0)

    return preptime_text

def extract_cooktime(text):
    cooktime_text = re.search(r"(?<=Cook Time:\s)(.*?)(?=\s\sminutes)", text).group(0)

    return cooktime_text

def extract_totaltime(text):
    totaltime_text = re.search(r"(?<=Total Time:\s)(.*?)(?=\s\sminutes)", text).group(0)

    return totaltime_text

def extract_servings(text):
    servings_text = re.search(r"(?<=Servings:\s)(.*?)(?=\s\s\s\sIngredients|\s\s\s\sEquipment)", text).group(0)

    return servings_text

def extract_instructions(text):
    instructions_patterns = ["(?<=Step-by-Step Instructions\s\s).*?(?=\s\s\s)",
     "(?<=Steps for Making and Baking the Cookies\s\s).*?(How)"]
    item = 0
    failed = True
    instructions_list = [""]

    while failed and item < len(instructions_patterns):
        try:
            instructions_text = re.search(instructions_patterns[item], text).group(0)
            instructions_list = re.split("\s\s", instructions_text)
            failed = False
        except:
            item += 1
            failed = True

    return instructions_list



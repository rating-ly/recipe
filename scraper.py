

from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import re, json


#the main method that takes the URL and scrapes it, returns the recipe JSON
def scrape(url):
    print("scrpaping:", url)
    header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'} 

    request=Request(url,None,header)
    response = urlopen(request)

    html = response.read()
    #extract visible text from the web page (this will remove the HTML, JavaScript
    #and other content that cannot be read by the user)
    visible_text = text_from_html(html)
    #write_text_to_file(visible_text, 'temp_output.txt')
    ingredients_list = extract_ingredients(visible_text)

    title_text = extract_title(visible_text)
    preptime_text = extract_preptime(visible_text)
    cooktime_text = extract_cooktime(visible_text)
    totaltime_text = extract_totaltime(visible_text)
    servings_text = extract_servings(visible_text)

    recipe_dictionary = {}
    recipe_dictionary['ingredients'] = ingredients_list
    recipe_dictionary['title'] = title_text
    recipe_dictionary['prep time'] = preptime_text
    recipe_dictionary['cook time'] = cooktime_text
    recipe_dictionary['total time'] = totaltime_text
    recipe_dictionary['servings'] = servings_text

    instructions_list = extract_instructions(visible_text)

    recipe_dictionary['instructions'] = instructions_list

    recipe_json = json.dumps(recipe_dictionary, indent=4)

    #write_text_to_file(recipe_json, 'recipe_output.json')
    return recipe_json


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





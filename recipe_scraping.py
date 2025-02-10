

from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import re, json

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
 
    instructions_text = re.search("(?<=Step-by-Step Instructions\s\s).*?(?=\s\s\s)", text).group(0)
    instructions_list = re.split("\s\s", instructions_text)

    return instructions_list


#fetch the content of the URL

#https://addapinch.com/the-best-chocolate-cake-recipe-ever/
#https://addapinch.com/best-chocolate-chip-cookies-recipe/
#https://addapinch.com/skillet-mac-cheese-recipe/
#https://addapinch.com/blueberry-muffins/
req =  Request('https://addapinch.com/the-best-chocolate-cake-recipe-ever/', headers={'User-Agent': 'Mozilla/5.0'})
#read the underlying source code of the web page
html = urlopen(req).read()

#extract visible text from the web page (this will remove the HTML, JavaScript
#and other content that cannot be read by the user)
visible_text = text_from_html(html)
write_text_to_file(visible_text, 'temp_output.txt')
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

write_text_to_file(recipe_json, 'recipe_output.json')
print(recipe_json)

'''
following work needs to be done now:

(Jenny) 1. The Ingredients have empty first item and empty spaces around the strings, 
those need to be cleaned up


2. Similar to Ingredients, following items also needs to be extracted and added to:
(Jenny) 2.a Title, in this case - The Best Chocolate Cake Recipe {Ever}
(Jenny) 2.b Prep time, Cook time, total time, servings
(Zain) 2.c Cooking Instructions
(Zain) 2.d Equipment
(Zain) 2.e Notes

(Jenny & Zain)3. Once done with items assigned to you, test your code on 3 more recipes from the same website 
and try to fix the issues you see. You can use following recipes:

    3.a https://addapinch.com/best-chocolate-chip-cookies-recipe/
    3.b https://addapinch.com/skillet-mac-cheese-recipe/
    3.c https://addapinch.com/blueberry-muffins/


(Jenny & Zain) 4. Next week, we will try to run your code using recipes from other websites and discuss
Find 5 recipes from other websites (not addapinch.com) that we can use


'''




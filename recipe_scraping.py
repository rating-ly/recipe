

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
    ingredients_text = re.search("(?<=Ingredients)?▢.*(?=Instructions)", text).group(0)
    ingredients_list = re.split("▢", ingredients_text)

    return ingredients_list


#fetch the content of the URL
req =  Request('https://addapinch.com/the-best-chocolate-cake-recipe-ever/', headers={'User-Agent': 'Mozilla/5.0'})
#read the underlying source code of the web page
html = urlopen(req).read()

#extract visible text from the web page (this will remove the HTML, JavaScript
#and other content that cannot be read by the user)
visible_text = text_from_html(html)
write_text_to_file(visible_text, 'temp_output.txt')
ingredients_list = extract_ingredients(visible_text)

recipe_dictionary = {}
recipe_dictionary['ingredients'] = ingredients_list

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




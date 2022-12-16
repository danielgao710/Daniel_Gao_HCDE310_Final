import urllib.request, urllib.error, urllib.parse, json, webbrowser
import requests

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request." )
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

base_url = "https://api.spoonacular.com/recipes/findByIngredients"
key = "e6c7b9feff674a01abba8e92dc3d9a22"
def get_recipes(apiKey = "e6c7b9feff674a01abba8e92dc3d9a22", ingredients = "apples,flour,sugar", number=10):
    parameters = {"apiKey": apiKey, "ingredients": ingredients, "number": number}
    headers = {"User_Agent": "Chrome"}
    response = requests.get(base_url, params=parameters, headers=headers)
    result = json.loads(response.text)
    return result
#recipes = get_recipes(number = 2)
#print(pretty(recipes))

class Recipe():
    def __init__(self, list):
        self.id = list["id"]
        self.image = list["image"]
        self.missedIngredientCount = list["missedIngredientCount"]
        missedingredients = list["missedIngredients"][0]["name"]
        for ingredient in list["missedIngredients"][1:]:
            missedingredients += ", " + ingredient["name"]
        self.missedIngredients = missedingredients
        self.title = list["title"]

    def make_photo_url(self):
        return "https://spoonacular.com/recipes/{id}/ingredientWidget.png".format(id=self.id)

    def __str__(self):
        return "title: " + str(self.title) + "\n" + \
                "id: " + str(self.id) + "\n" + \
               "missedIngredientCount: " + str(self.missedIngredientCount) + "\n" + \
               "missedIngredients: " + str(self.missedIngredients) + "\n" + \
               "image: " + str(self.image)

def sort_list(recipes):
    result = []
    for recipe in recipes:
        result.append(Recipe(recipe))
    return sorted(result, key=lambda x: x.missedIngredientCount, reverse=False)

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('index.html')

@app.route("/recipes", methods = ["GET"])
def get():
    ings = request.args.get("ingredients")
    if ings:
        recipes = get_recipes(ingredients=ings)
        recipeslist = sort_list(recipes)
        return render_template('recipes.html', recipes=recipeslist)
    else:
        return render_template('index.html', prompt="Can not process the ingredients. Please try again.")

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

































#def main_handler():
#    app.logger.info("In MainHandler")
#    return render_template('index.html', page_title="Greeting Form")

#if __name__ == "__main__":
#    app.run(host="localhost",port=8080, debug=True)


#random_joke = "food/jokes/random"
#find = "recipes/findByIngredients"
#randomFind = "recipes/random"
#@app.route('/')
#def search_page():
#    joke_response = str(requests.request("GET", url + random_joke).json()['text'])
#    return render_template('search.html', joke=joke_response)
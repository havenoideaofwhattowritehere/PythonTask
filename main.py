from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify
import requests
import json

def parse():
    html = requests.get('https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html').text
    soup = BeautifulSoup(html, "html.parser")
    urls = soup.find_all('a', class_='cmp-category__item-link')
    items = []
    for url in urls:
        try:
            link = "https://www.mcdonalds.com" + url.get("href")

            item_html = requests.get(link).text
            item_soup = BeautifulSoup(item_html, "html.parser")
            item_name = item_soup.find('span', class_= 'cmp-product-details-main__heading-title').text
            item_description = item_soup.find('span', class_= 'body').text
            item_nutritions = item_soup.find('div', class_='cmp-nutrition-summary cmp-nutrition-summary--primary')
            data = json.loads(item_nutritions.get('data-nutrition-ids'))
            for i in enumerate(data):
                item_calories = data[0]['identifier']
                item_fats = data[1]['identifier']
                item_carbs = data[2]['identifier']
                item_proteins = data[3]['identifier']
            item_secondary_nutritions = item_soup.find('div', class_='cmp-nutrition-summary cmp-nutrition-summary--nutrition-table')
            secondary_data = json.loads(item_secondary_nutritions.get('data-nutrition-ids'))

            for i in enumerate(secondary_data, 1):
                item_unsaturated_fats = secondary_data[1]['identifier']
                item_sugar = secondary_data[2]['identifier']
                item_salt = secondary_data[3]['identifier']
                item_portion = secondary_data[4]['identifier']

            items.append(
                {
                    'Name': item_name,
                    'Description': item_description,
                    'Calories': item_calories,
                    'Fats': item_fats,
                    'Carbs': item_carbs,
                    'Proteins': item_proteins,
                    'Unsaturated fats': item_unsaturated_fats,
                    'Sugar': item_sugar,
                    'Salt': item_salt,
                    'Portion': item_portion
                }
            )
        except:
            pass
    json_list = json.dumps(items)
    return json_list

app = Flask(__name__)

@app.route('/all_products')
def getProducts():
    return jsonify(parse())

@app.route('/products/<product_name>')
def getProduct(product_name):
    items = json.loads(parse())
    for item in items:
        if product_name in item.values():
            return jsonify(item)

@app.route('/products/<product_name>/<product_field>')
def getField(product_name, product_field):
    items = json.loads(parse())
    for item in items:
        if product_name in item.values() and product_field in item.keys():
            return jsonify(item)

if __name__ == '__main__':
    app.run()
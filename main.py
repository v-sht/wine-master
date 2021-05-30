from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import pandas
import collections

time_now = datetime.datetime.now()
current_age = time_now.year - 1920

if current_age % 10 == 1:
    word_for_year = 'год'
elif (current_age % 10 in (2, 3, 4) and
      current_age not in (100, 111, 112, 113, 114)):
    word_for_year = 'года'
else:
    word_for_year = 'лет'


excel_data_df = pandas.read_excel(
    'price.xlsx',
    na_values='nan',
    keep_default_na=False)

drinks = excel_data_df.to_dict(orient='records')

grouped_drinks = collections.defaultdict(list)

for drink in drinks:
    grouped_drinks[drink.get('Категория')].append(drink)


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    age=current_age,
    year=word_for_year,
    grouped_drinks=sorted(grouped_drinks.items())
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

from flask import render_template, request, Blueprint

import sys
path_lib = "../lib"
sys.path.append(path_lib)

from VirtualScraper import headers

main = Blueprint("main", __name__)


@main.route('/')
@main.route('/home')
def home():
    print("home")
    #url_leboncoin = 'https://www.leboncoin.fr/annonces/offres/ile_de_france/'
    #page_add_leboncoin = '&page='  # '&page=2'
    #scraper = LebonCoin_Scraper(url_leboncoin, page_add_leboncoin)

    #scraper.get_full_list_appt()
    #return str(announces)
    return render_template("home.html",title="about", announces= str(headers))
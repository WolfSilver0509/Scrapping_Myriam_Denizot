import requests
from bs4 import BeautifulSoup as bs

import unidecode

import csv
# lib pour les csv
import urllib.request

from .Image import get_link_image

def etape1(url_page_produit):
    # On crée une reponse qui va recuperer l'url si tout est ok (200 )
    response = requests.get(url_page_produit)
    soup = bs(response.text, 'lxml')

    if response.ok:
        product_page_url = url_page_produit
        table = soup.findAll('td')
        title = soup.find('h1').text
        universal_product_code = table[0].text
        price_including_tax = table[2].text.replace('£', '').replace('Â', '')
        price_excluding_tax = table[3].text.replace('£', '').replace('Â', '')
        number_available = table[5].text.removeprefix('In stock (').removesuffix('available)')
        # number_available = (str(table[5]).text).removeprefix('In stock (').removesuffix('available)')
        # number_available = str((table[5]).text).removeprefix('In stock (').removesuffix('available)')
        # number_available = str(table[5]).removeprefix('<td>In stock (').removesuffix('available)</td>')
        # --- diff teste effectuer valide mais fonctionne sur pycharm ici version 3.8 trop oldd ----
        product_description_unicode = soup.select_one('article > p').text
        product_description = unidecode.unidecode(product_description_unicode)
        category = soup.find('ul', class_="breadcrumb").findAll('a')[2].text
        review_rating = soup.find('p', class_='star-rating').get('class').pop()
        image = soup.find('div', class_="item active").find('img')

        book = {"product_page_url": product_page_url,
                "title": title,
                "product_description": product_description,
                "universal_product_code": universal_product_code,
                "price_including_tax": price_including_tax,
                "price_excluding_tax": price_excluding_tax,
                "category": category,
                "review_rating": review_rating,
                "image": image,
                "number_available": number_available}
        # "number_available":number_available}

        # print(book)

    print("🎯 Le lien de la page du livre est :", product_page_url)
    print("📕 Le titre du livre est :", title)
    print("📖 La déscription du livre est :", product_description)
    print("🔎 Le code Universel de produit :", universal_product_code)
    print("💰 Le prix en incluant les taxes :", price_including_tax)
    print("💸 Le prix en excluant les taxes :", price_excluding_tax)
    print("💸 La catégories du livre est :", category)
    print("📊 La note du livre :", review_rating, " ⭐")
    print("📷 L'image du livre ' :", image['src']),
    print("📷 Le stock disponible du livre :", number_available)

    # Créer une liste pour les en-têtes
    def csv_createur():
        en_tete = ['product_page_url',
                   'title',
                   'product_description',
                   'universal_product_code',
                   'price_including_tax',
                   'price_excluding_tax',
                   'category',
                   'review_rating',
                   'image',
                   'number_available']
        # Créer un nouveau fichier pour écrire dans le fichier appelé « data.csv »

        with open('Livre1/data_' + category + '.csv', 'w') as fichier_csv:
            # Créer un objet writer (écriture) avec ce fichier
            writer = csv.writer(fichier_csv, delimiter=';')
            writer.writerow(en_tete)
            writer.writerow([product_page_url,
                             title,
                             product_description,
                             universal_product_code,
                             price_including_tax,
                             price_excluding_tax,
                             category,
                             review_rating,
                             image['src'],
                             number_available])

    print(csv_createur())
    print(" 💾 Votre fichier CSV viens d'être crée. Vous pouvez le télécharger !")

    """ def get_link_image(soup):
        target_lnk_img = soup.find('div', class_="item active").find('img')['src']
        base_url = "https://books.toscrape.com/"
        complete_lnk = base_url + target_lnk_img
        complete_lnk = complete_lnk
        return complete_lnk.replace("../../", '')"""

    image_url = get_link_image(soup, 1)
    filename = "Livre1/" + title + ".jpg"
    urllib.request.urlretrieve(image_url, filename)


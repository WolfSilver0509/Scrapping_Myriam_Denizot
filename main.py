# ----------------------- Début du programme --------------------
Scrapping_begin = ("""
      ___           ___           ___           ___           ___         ___                     ___           ___                    ___          _____    
     /  /\         /  /\         /  /\         /  /\         /  /\       /  /\      ___          /__/\         /  /\                  /__/\        /  /::\   
    /  /:/_       /  /:/        /  /::\       /  /::\       /  /::\     /  /::\    /  /\         \  \:\       /  /:/_                |  |::\      /  /:/\:\  
   /  /:/ /\     /  /:/        /  /:/\:\     /  /:/\:\     /  /:/\:\   /  /:/\:\  /  /:/          \  \:\     /  /:/ /\               |  |:|:\    /  /:/  \:\ 
  /  /:/ /::\   /  /:/  ___   /  /:/~/:/    /  /:/~/::\   /  /:/~/:/  /  /:/~/:/ /__/::\      _____\__\:\   /  /:/_/::\            __|__|:|\:\  /__/:/ \__\:|
 /__/:/ /:/\:\ /__/:/  /  /\ /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/  /__/:/ /:/  \__\/\:\__  /__/::::::::\ /__/:/__\/\:\          /__/::::| \:\ \  \:\ /  /:/
 \  \:\/:/~/:/ \  \:\ /  /:/ \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/   \  \:\/:/      \  \:\/\ \  \:\~~\~~\/ \  \:\ /~~/:/          \  \:\~~\__\/  \  \:\  /:/ 
  \  \::/ /:/   \  \:\  /:/   \  \::/~~~~   \  \::/       \  \::/     \  \::/        \__\::/  \  \:\  ~~~   \  \:\  /:/            \  \:\         \  \:\/:/  
   \__\/ /:/     \  \:\/:/     \  \:\        \  \:\        \  \:\      \  \:\        /__/:/    \  \:\        \  \:\/:/              \  \:\         \  \::/   
     /__/:/       \  \::/       \  \:\        \  \:\        \  \:\      \  \:\       \__\/      \  \:\        \  \::/                \  \:\         \__\/    
     \__\/         \__\/         \__\/         \__\/         \__\/       \__\/                   \__\/         \__\/                  \__\/                
""")

print(Scrapping_begin)

# ----------------------------------------------------------------------
# Import des librairies
import requests
from bs4 import BeautifulSoup as bs

import os
# os création de dossier
# importation de l'image



from fonctions.Etape_1 import etape1


from fonctions.Etape_2 import info_extract
from fonctions.Etape_2 import etape2
from fonctions.Etape_3 import get_url_category
from fonctions.Etape_3 import get_all_links_book_to_category
from fonctions.Etape_3 import info_extract

#from fonctions.Etape_3 import etape3
# rentrer l'url d'une page produit dans "l'URL"
url_page_produit = ' http://books.toscrape.com/catalogue/sharp-objects_997/index.html'

# création du dossier en locale auto
if not os.path.isdir('Livre1'):
    os.system('mkdir Livre1')

if not os.path.isdir('Horror'):
    os.system('mkdir Horror')

if not os.path.isdir('category'):
    os.system('mkdir category')


# Récupération de l'URL de la catégorie Horror
url_horror = "https://books.toscrape.com/catalogue/category/books/horror_31/index.html"

url = "https://books.toscrape.com/"
reponse = requests.get(url)
page = reponse.content
soup = bs(page, "html.parser")

links_catgs = []
nom_catgs = []

# permet d'aller récupérer les liens des catégories
for ul in soup.find_all('ul', class_='nav nav-list'):
    for li in ul.find_all('li'):
        a = li.find('a')
        link = a['href']
        links_catgs.append("https://books.toscrape.com/" + link)
        category = a.text
        nom_catgs.append(category.replace("\n", "").replace(" ", ""))
# # suppression du premier lien et du premier nom de la liste ( book qui n'est pas une catégories )
del links_catgs[0]
del nom_catgs[0]

# création des dossiers avec le nom des catégories au complet
for category in nom_catgs:
    str(category)
    if not os.path.isdir('category/' + category):
        os.system('mkdir category\\' + category)

def etape3(links_catgs):
    for link in links_catgs:
        main_page = requests.get(link)
        # création de l'objet Soup
        soup_page = bs(main_page.text, "lxml")
        index_page = soup_page.find(class_="current")
        nb_page = 1
        if index_page:
            nb_page = index_page.text.rsplit('of', 1).pop()
            print(nb_page)
        for n in range(1, int(nb_page)+1):
            if n == 1:
                url_category = link
            else:
                url_category = link.replace("index.html", "page-" + str(n) + '.html')
            print(url_category)
            all_links_category = get_all_links_book_to_category(get_url_category(url_category))

            info_extract(all_links_category, n > 1)



question_1 = input("🕯️ Voulez-vous accéder à la page produit d'un livre ?🕯️ [o/N] ")
question_1 = question_1.strip().lower()
# .strip()supprime tous les caractères à droite et à gauche
# La méthode lower() renvoie la chaîne en minuscules
if question_1.startswith('o'):
    print(etape1(url_page_produit))
    print(" ⚠️  ⚠️ Pour accéder au autres démonstrations de scrapping , veuillez relancer l'exécution du scrypte Python. ⚠️  ⚠️ ")


elif question_1.startswith('n') or question_1 == '':
    question_2 = input(" 🏮Voulez-vous accéder à tous les livres de la catégorie horror ?🏮 [o/N] ")
    question_2 = question_2.strip().lower()
    # Rajouter la deuxiéme question pour la partie 2
    if question_2.startswith('o'):
        print(etape2(url_horror))
        print(" ⚠️  ⚠️ Pour accéder au autres démonstrations de scrapping , veuillez relancer l'exécution du scrypte Python. ⚠️  ⚠️ ")
    elif question_2.startswith('n') or question_2 == '':
        question_3 = input(" 💡 Voulez-vous accéder à tous les livres de toutes les catégories du site ? 🧲 [o/N] ")
        question_3 = question_3.strip().lower()
        if question_3.startswith('o'):
            print(etape3(links_catgs))
        elif question_3.startswith('n') or question_3 == '':
            print("Au revoir")
            print(
                " ⚠️  ⚠️ Pour accéder au autres démonstrations de scrapping , veuillez relancer l'exécution du scrypte Python. ⚠️  ⚠️ ")

        else:
            print("Répondez par 'o' ou 'n'")

    else:
        print("Répondez par 'o' ou 'n'")
else:
    print("Répondez par 'o' ou 'n'")

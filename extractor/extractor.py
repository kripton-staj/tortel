import json
import re

from bs4 import BeautifulSoup


def extract_title(soup):
    return soup.title.text.replace('\\n', '').\
        replace('\\t', '').replace('\\r', '')


def extract_description(soup):
    description = ""
    try:
        script_tag = soup.find_all(
            'script', {'type': 'application/ld+json'})
        for script in script_tag:
            script_str = script.string
            script = script_str.replace('\\n', ''). \
                replace('\\t', '').replace('\\r', '').replace('\\', '')
            json_script = json.loads(script)
            if json_script['@type'] == ('Product' or 'product'):
                description = json_script['description']

    except TypeError as t:
        print(t)
    except ValueError as v:
        print(v)
    except KeyError as k:
        print(k)

    if not description:
        class_names = [{"id": "product_omschrijving"},
                       {"class": "product data content"},
                       {"class": "std product-description"},
                       {"class": "description_short"},
                       {"class": "product-info-bottom"},
                       {"id": "product-description-content"},
                       {"id": "description-callback"},
                       {"class": "cms-content hide@md-down"},
                       {"class": "fg-box bpx0 bpy1 bsx3 bsy1 mpx0 mpy1 msx3 msy1 spx0 spy1 ssx3 ssy1"},
                       {"class": "productdescription"},
                       {"class": "description body-font-size"},
                       {"class": "product-information__wrapper"},
                       {"class": "std product-info"},
                       {"class": "productDescription__short-description"},
                       {"itemprop": "description"},
                       {"id": "itemLongDescription"},
                       {"class": "product-description p-lg-5"},
                       {"class": "pd-info__usp-list"},
                       {"class": "product-description"},
                       {"class": "product-info__text"},
                       {"id": "product-page"},
                       {"class": "f-productDetails-table"},
                       {"id": "tab-description"},
                       {"class": "mxd-page-section"},
                       {"class": "product-collateral"},
                       {"class": "content mb-5"}]

        for class_name in class_names:
            class_tag = soup.findAll(attrs=class_name)
            if class_tag:
                for content in class_tag:
                    description += content.text + " "
                description = description.replace('\\n', ''). \
                    replace('\\t', '').replace('\\r', '')
                description = " ".join(description.split())
                description = re.sub(r'[^\x00-\x7F]+', ' ', str(description)).\
                    encode('ascii', 'ignore').decode('unicode_escape').strip()
                break

    return description


def extract_product_text(html):
    soup = BeautifulSoup(html, "lxml")
    title = extract_title(soup)
    description = extract_description(soup)
    product_text = str(title) + " " + str(description)
    return product_text

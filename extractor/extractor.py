import json


def extract_title(soup):
    return soup.title.text.replace('\\n', '').\
        replace('\\t', '').replace('\\r', '')


def extract_description(soup):
    description = ""

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
                   {"class": "product-collateral"}]

    for class_name in class_names:
        description = soup.find(attrs=class_name)
        if description:
            description = description.get_text(strip=True)
            description = description.replace('\\n', '').\
                replace('\\t', '').replace('\\r', '')
            description = " ".join(description.split())
            break

    if not description:
        try:
            script_tag = soup.find_all(
                'script', {'type': 'application/ld+json'})
            for script in script_tag:
                script_str = script.string
                script = script_str.replace('\\n', '').\
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

    return description


def extract_breadcrumbs(soup):
    breadcrumbs = []
    brd_array = [{"class": "breadcrumbs__link"}, {"class": "breadcrumb"},
                 {"id": "breadcrumb"}, {"id": "breadcrumbs"},
                 {"id": "crumbar-content"}, {"class": "breadcrumbs"},
                 {"class": "c-breadcrumb"}, {"class": "nav nav-tabs"},
                 {"class": "woocommerce-breadcrumb"},
                 {"class": "Breadcrumb-module__root___2XZI0 col-6-m ProductDetailPage-module__breadcrumb___SVrjj"},
                 {"class": "f-productHeader js-articleHeader"}]

    for brd in brd_array:
        breadcrumbs_list = soup.find(attrs=brd)
        if breadcrumbs_list:
            for a in breadcrumbs_list.find_all('a', href=True):
                breadcrumbs.append(str(a['href']))
            break

    return breadcrumbs


def extract_specifications(soup):
    specification = ""
    spec_class_names = [{"class": "specifications"}, {"class": "specificaties"},
                        {"id": "description-collapse"},
                        {"id": "product-attribute-specs-table"},
                        {"id": "product-specs-content"},
                        {"class": "fg-box bpx0 bpy2 bsx3 bsy1 mpx0 mpy2 msx3 msy1 spx0 spy2 ssx3 ssy1"},
                        {"id": "product-specifications"},
                        {"class": "mobile-tab first body-font-size"},
                        {"id": "eigenschappen"},
                        {"class": "expert_review_products_shortdesc_left d-block d-lg-none"},
                        {"id": "specifications"},
                        {"class": "col-12 px-0 px-lg-4 my-2 product-attributes"},
                        {"class": "feature-benefit__text-wrap"},
                        {"class": "product__specs"},
                        {"class": "slot slot--seperated slot--seperated--has-more-content js_slot-specifications"},
                        {"class": "v-card__text pa-2 product-specifications__text"},
                        {"class": "std"}, {"id": "Characteristics"}]

    for class_name in spec_class_names:
        specification = soup.find(attrs=class_name)
        if specification:
            specification = specification.get_text(strip=True)
            specification = specification.replace('\\n', '').\
                replace('\\t', '').replace('\\r', '')
            specification = " ".join(specification.split())
            break

    return specification

def extract_title(soup):
    return soup.title.text.replace('\\n', '').replace('\\t', '').replace('\\r', '')


def extract_description(soup):
    description = ""

    class_names = [{"id": "product_omschrijving"}, {"class": "product data content"},
                   {"class": "std product-description"}, {"class": "description_short"},
                   {"class": "product-info-bottom"}, {"id": "product-description-content"},
                   {"id": "description-callback"}, {"class": "cms-content hide@md-down"},
                   {"class": "fg-box bpx0 bpy1 bsx3 bsy1 mpx0 mpy1 msx3 msy1 spx0 spy1 ssx3 ssy1"},
                   {"class": "productdescription"}, {"class": "description body-font-size"},
                   {"class": "product-information__wrapper"},  {"class": "std product-info"},
                   {"class": "productDescription__short-description"}, {"itemprop": "description"},
                   {"id": "itemLongDescription"}, {"class": "product-description p-lg-5"},
                   {"class": "pd-info__usp-list"}]

    for class_name in class_names:
        description = soup.find(attrs=class_name)
        if description:
            description = description.get_text(strip=True)
            description = description.replace('\\n', '').replace('\\t', '').replace('\\r', '')
            break
    try:
        description = " ".join(description.split())
    except AttributeError as a:
        print(a)

    return description


def extract_breadcrumbs(soup):
    breadcrumbs = []
    brd_array = [{"class": "breadcrumbs__link"}, {"class": "breadcrumb"}, {"id": "breadcrumb"},
                 {"id": "breadcrumbs"}, {"id": "crumbar-content"}, {"class": "breadcrumbs"},
                 {"class": "c-breadcrumb"}, {"class": "nav nav-tabs"}]

    for brd in brd_array:
        breadcrumbs = soup.find(attrs=brd)
        if breadcrumbs:
            breadcrumbs = breadcrumbs.get_text(strip=True)
            breadcrumbs = breadcrumbs.replace('\\n', '').replace('\\t', '').replace('\\r', '')
            break
    try:
        breadcrumbs = " ".join(breadcrumbs.split())
    except AttributeError as a:
        print(a)

    return breadcrumbs


def extract_specifications(soup):
    specification = ""
    spec_class_names = [{"class": "specifications"}, {"class": "specificaties"}, {"id": "description-collapse"},
                        {"id": "product-attribute-specs-table"}, {"id": "product-specs-content"},
                        {"class": "fg-box bpx0 bpy2 bsx3 bsy1 mpx0 mpy2 msx3 msy1 spx0 spy2 ssx3 ssy1"},
                        {"id": "product-specifications"}, {"class": "mobile-tab first body-font-size"},
                        {"id": "eigenschappen"}, {"class": "expert_review_products_shortdesc_left d-block d-lg-none"},
                        {"id": "specifications"}, {"class": "col-12 px-0 px-lg-4 my-2 product-attributes"},
                        {"class": "feature-benefit__text-wrap"}]

    for class_name in spec_class_names:
        specification = soup.find(attrs=class_name)
        if specification:
            specification = specification.get_text(strip=True)
            specification = specification.replace('\\n', '').replace('\\t', '').replace('\\r', '')
            break
    try:
        specification = " ".join(specification.split())
    except AttributeError as a:
        print(a)

    return specification

import json


def extract_title(response):
    title = response.xpath('//title/text()')
    return title


def extract_description(response):
    description = ""
    """"
    desc_data = response.xpath("//script[contains(., 'description')]/text()")
    for data in desc_data:
        if not data:
            continue
        else:
            try:
                # cant load json data
                data_dict = json.loads(data)
    """
    return description


def extract_breadcrumbs(response):    # WP
    breadcrumbs = []

    brd_array = ['//nav[@class="breadcrumbs-nav"]//a/@href', '//div[@class="fluid-grid__item fluid"]//a/@href',
                 '//nav//ol[@class="breadcrumbs"]//li//a/@href']

    for brd in brd_array:
        breadcrumbs = response.xpath(brd)
        if breadcrumbs:
            break

    return breadcrumbs
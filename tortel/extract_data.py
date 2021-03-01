import extraction
import requests
import psycopg2


def read_file():
    with open("url_list.txt", "r") as f:
        newlist = [line.rstrip() for line in f.readlines()]

    return newlist


def extract_title(new_list):
    extracted_titles = []

    for url in new_list:
        html = requests.get(url).text
        extracted = extraction.Extractor().extract(html, source_url=url)
        extracted_titles.append(extracted.title)

    return extracted_titles


url_list = read_file()
extracted_titles = extract_title(url_list)

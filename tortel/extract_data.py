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

def insert_database(url_list, extracted_titles):

    conn = psycopg2.connect(database="tortel", user="postgres",
                            password="gizliparola", host="127.0.0.1", port="5432")
    print("Database opened successfully")

    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS TORTEL")

    sql = '''CREATE TABLE TORTEL(
       URL TEXT NOT NULL,
       TITLE TEXT NOT NULL
    )'''

    cursor.execute(sql)
    postgres_insert_query = """INSERT INTO TORTEL(URL, TITLE) VALUES (%s, %s)"""

    for i,j in zip(url_list, extracted_titles):
        record_to_insert = (i,j)
        cursor.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    conn.close()

url_list = read_file()
extracted_titles = extract_title(url_list)
insert_database(url_list, extracted_titles)

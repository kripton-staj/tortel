# tortel
Product similarity detection with NLP

### requirements  :  
* Python 3.9
* Postgresql 10.15

### installation:

1. **git clone https://github.com/kripton-staj/tortel.git**
   
   **cd tortel/**

   
2. install packages in 'requirements.txt' with

     **pip install "package_name"**


3. Open a terminal, go to your PostgreSQL server and type
**CREATE DATABASE product;**
   

4. Edit your DATABASE_URI info in 'config.py'


5. Run the below command in the top level directory spider tortel/spider.
   
   This command will write the html to the database for read it from there later.
      
   ```
   scrapy crawl spider
   ```


6. Run the below command to extracting data from web pages written into product_body table.

   ```
   python3 Extractor/utils.py
   ```


7. Run the below command to check product similarity with NLP
    
   ```
   python3 product_similarity/product_similarity.py
   ```






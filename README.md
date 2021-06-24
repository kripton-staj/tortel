# tortel
Product similarity detection with NLP

![tortel](https://user-images.githubusercontent.com/3041416/123288171-9a9ae400-d50f-11eb-9640-2bde965a817f.png)


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
   

4. Edit your DATABASE_URI info in common/config.py



5. Run the script in tortel/scripts directory.
   
   Example call for the script:
    ```
    python scripts/load_initial_data.py -f results.json
    ```
    ***NOTE***: JSON file must contains **'url'** and **'ean'** keys.

    {  
    "ean": "ean_code"
      
    "url": "url_name"

     }


6. Run the below command in the top level directory spider tortel/spider.
   
   This command will write the html to the database for read it from there later.
      
   ```
   scrapy crawl tortel_spider
   ```


7. Run the below command to extracting data from web pages written into product_page table.

   ```
   python3 extractor/main.py
   ```


8. Run the below command to check product similarity and accuracy ratio
    
   ```
   python3 scripts/accuracy_calculator.py
   ```


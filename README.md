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


5. Run **scrapy crawl spider** in the top level directory spider. This command will write the html to the database for read it from there later.


6. ***python3*** utils.py







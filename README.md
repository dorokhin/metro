# metro project

Adds metro stations (cities and lines too) from HH api to local database

### Before run script:
 * load sql (create tables) from `init.sql`
 ```shell script
 psql -h localhost -d database_name -U username -f init.sql 
```
 * install requirements:
```shell script
pip install -r requirements.txt
```
### Data structure
```json
{
   "id":"2",
   "name":"Санкт-Петербург",
   "url":"https://api.hh.ru/metro/2",
   "lines":[
      {
         "id":"14",
         "hex_color":"D6083B",
         "name":"Кировско-Выборгская",
         "stations":[
            {
               "id":"14.190",
               "name":"Девяткино",
               "lat":60.050182,
               "lng":30.443045,
               "order":0
            }
         ]
      }
   ]
}
```

### Message on success execution

```
Total cities added: 2
Total metro lines added: 24
Total metro stations added: 357
```

### Screenshots

![alt text](https://github.com/dorokhin/metro/blob/main/img/screenshot_database_1.png?raw=true)
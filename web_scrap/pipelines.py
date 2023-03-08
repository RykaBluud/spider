# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class WebScrapPipeline:
    def process_item(self, item, spider):
        return item

import mysql.connector

class MysqlDemoPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'machinedata.mysql.database.azure.com',
            user = 'DmitrijsDer',
            password = '22331516Das',
            database = 'machinedata'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS machinelist(
            id int NOT NULL auto_increment, 
            name text,
            manufacturer text,
            model text,
            location text,
            price text,
            year text,
            mileage VARCHAR(255),
            machine_condition text,
            image text,
            url text,
            main_category text,
            sub_category text,
            created_at text,
            PRIMARY KEY (id)
        )
        """)        


        



    def process_item(self, item, spider):

        ## Define insert statement
         self.cur.execute(""" insert into machinelist (name, manufacturer, model, location, price, year, mileage, machine_condition, image, url, main_category, sub_category, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item["name"],
            str(item["manufacturer"]),
            item["model"],
            item["location"],
            item["price"],
            str(item["year"]),
            str(item["mileage"]),
            item["machine_condition"],
            str(item["image"]),
            str(item["url"]),
            str(item["main_category"]),
            str(item["sub_category"]),
            str(item["created_at"])
           
         ))
         self.conn.commit()

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
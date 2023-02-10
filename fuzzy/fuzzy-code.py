import csv
import datetime
import json
import requests
import sqlite3
import traceback
from sqlite3 import connect


def insert_data(task):
    cursor.execute("CREATE TABLE IF NOT EXISTS product_stocks(id integer PRIMARY KEY, time NOT NULL, product_id TEXT, variant_id TEXT, stock_id TEXT, supply TEXT);")
    cursor.execute("INSERT INTO product_stocks(time,product_id,variant_id,stock_id,supply) VALUES (?,?,?,?,?) ", task)
    connection.commit()

time_now = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

for target in range(1,3): #[-2, -3] target -2 -3
    try:
        ok = True
        #line = str(target) line is equal to target in for loop
        response = requests.get(
            f"https://dummy.server/products/example?id={target}" #line #get value id=-1 and id=-2 --> but database creates id from 1 and up
        )
        response_content = response.json() #IT MUST BE JSON
        with open("tmp.txt", 'w') as f: #WB is for Photos
            f.write(response_content)

        if "bundle" not in response_content["type"]:
            print("product loaded")
            connection = connect("database.sqlite")
            cursor = connection.cursor()
            product_supply =  [stock["quantity"] for supply in response_content["details"]["supply"] for stock in supply["stock_data"] if stock["stock_id"] == 1]
            time_now = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            task = (time_now, response_content["id"], supply["variant_id"], 1, product_supply)
            insert_data(task)

        if "bundle" in response_content["type"]:
            print("bundle loaded")
            products = [p["id"] for p in response_content["type"]["bundle"]["bundle_items"]]
            print(f"products {len(products)}")
            id = response_content["id"]
            all = []
            supply = 0
            for p in products:
                r = requests.get(
                    f"https://dummy.server/products/example?id={p}"
                )
                resp_content = r.json() #IT MUST BE JSON
                with open("tmp.txt", 'w') as f:
                    f.write(resp_content)
                for s in resp_content["details"]["supply"]:
                    print(s)
                    for stoc in s["stock_data"]:
                        if stoc["stock_id"] == 1:
                            supply += stoc["quantity"]
                all.append(supply)
            product_supply = min(all)

            connection = sqlite3.connect("baza_d.db")
            cursor = connection.cursor()
            task = (time_now, id, "NULL", 1, product_supply)
            insert_data(task)

    except:
        print(traceback.format_exc())
        ok = False
    if ok:
        print("ok")
    else:
        print("error")
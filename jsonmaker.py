import json
import pymysql


connect = pymysql.connect(host='localhost', user='hi', password='asd123', db='new_schema',charset='utf8mb4')
cur = connect.cursor()

query="select distinct 판매업소 from new_schema.asd;"
cur.execute(query)
connect.commit()

datas = cur.fetchall()

info={}
info['jijum']=[]
for data in datas:
    with open("jijum.json", "w", encoding='utf-8') as json_file:
        info['jijum'].append({"판매업소":data[0]})
        json.dump(info, json_file,ensure_ascii=False)





        




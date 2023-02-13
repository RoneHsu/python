from pymongo import MongoClient
import urllib.parse
import datetime

###############################################################################
#                       股票機器人 Python基礎教學 【pymongo教學】                      #
###############################################################################

# Authentication Database認證資料庫
Authdb='howard-good31'
stockDB='mydb'
currencyDB = 'users'
dbname = 'howard-good31'

##### 資料庫連接 #####
def constructor():
    client = MongoClient('mongodb://banana:asd85815@ac-coeypj2-shard-00-00.tvz10x3.mongodb.net:27017,ac-coeypj2-shard-00-01.tvz10x3.mongodb.net:27017,ac-coeypj2-shard-00-02.tvz10x3.mongodb.net:27017/?ssl=true&replicaSet=atlas-etu4k6-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client[Authdb]
    return db

def constructor_stock(): 
    client = MongoClient("mongodb://banana:asd85815@ac-coeypj2-shard-00-00.tvz10x3.mongodb.net:27017,ac-coeypj2-shard-00-01.tvz10x3.mongodb.net:27017,ac-coeypj2-shard-00-02.tvz10x3.mongodb.net:27017/?ssl=true&replicaSet=atlas-etu4k6-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client[stockDB]
    return db
def constructor_currency():
    client = MongoClient("mongodb://banana:asd85815@ac-coeypj2-shard-00-00.tvz10x3.mongodb.net:27017,ac-coeypj2-shard-00-01.tvz10x3.mongodb.net:27017,ac-coeypj2-shard-00-02.tvz10x3.mongodb.net:27017/?ssl=true&replicaSet=atlas-etu4k6-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client[currencyDB]
    return db
#   -----------    新增使用者的股票       -------------
def write_my_stock(userID, user_name, stockNumber, condition , target_price):
    db=constructor_stock()
    collect = db[user_name]
    is_exit = collect.find_one({"favorite_stock": stockNumber})
    if is_exit != None :
        content = update_my_stock(user_name, stockNumber, condition , target_price)
        return content
    else:
        collect.insert_one({
                "userID": userID,
                "favorite_stock": stockNumber,
                "condition" :  condition,
                "price" : target_price,
                "tag": "stock",
                "date_info": datetime.datetime.now()
            })
        return f"{stockNumber}已新增至您的股票清單"
#----------------------------更新暫存的股票名稱--------------------------
def update_my_stock(user_name,  stockNumber, condition , target_price):
    db=constructor_stock()
    collect = db[user_name]
    collect.update_many({"favorite_stock": stockNumber }, {'$set': {'condition':condition , "price": target_price}})
    content = f"股票{stockNumber}更新成功"
    return content

#----------------------------儲存使用者的股票--------------------------
def write_user_stock_fountion(stock, bs, price):  
    db=constructor()
    collect = db['mystock']
    collect.insert({"stock": stock,
                    "data": 'care_stock',
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.datetime.utcnow()
                    })
# ----------------  秀出使用者的股票條件       ----------------
def show_stock_setting(user_name, userID):
    db = constructor_stock()
    collect = db[user_name]
    dataList = list(collect.find({"userID": userID}))
    if dataList == []: return "您的股票清單為空，請透過指令新增股票至清單中"
    content = "您清單中的選股條件為: \n"
    for i in range(len(dataList)):
        content += f'{dataList[i]["favorite_stock"]} {dataList[i]["condition"]} {dataList[i]["price"]}\n'
    return content
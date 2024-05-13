from pymongo import MongoClient
import json
import os

def get_config(key):
    # config_file = "/home/prasaanth2k/welcome_bot_sna/src/config.json"
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_file, "r") as file:
        config = json.loads(file.read())
    if key in config:
        return config[key]
    else:
        raise Exception("Key {} is not found in config.json".format(key))
connection_string = get_config("mongodb_connection_string")
client = MongoClient(
    f"{connection_string}"
)
db = client.mystudents
collection = db.students
class Userbase:
    def add_user_details(self,full_name:str,group_id:int,user_id:int,user_name:str,is_bot:bool,location:str,profile_link:str,phone_number:int,epoctime:int):
        existing_user = collection.find_one({"user_id": user_id})
        group_name = get_config('group_id').get(str(group_id))
        if existing_user:
            try:
                collection.update_one(
                    {"user_id": user_id},
                    {"$set": {f"groups.{group_id}": group_name}}
                )
                print("[*] Data Updated Successfully")
            except Exception as e:
                print(f"[*] Error updating data: {e}")
        else:
            # Insert a new document
            user_data = {
                "id": 1,
                "full_name": full_name,
                "groups": {f"{group_id}": f"{group_name}"},
                "user_id": user_id,
                "user_name": user_name,
                "epoctime": epoctime,
                "is_bot":is_bot,
                "location":location,
                "profile_link": profile_link,
                "phone_number":phone_number
            }
            try:
                ack = collection.insert_one(user_data)
                if ack.acknowledged:
                    print("[*] Data Inserted Successfully")
                else:
                    print("[*] Unable to insert data")
            except Exception as e:
                print(f"[*] Error inserting data: {e}")
    def group_id_get(self,user_name:str):
        try:
            ack = collection.find_one({}, sort=[('_id', -1)])
            groups = ack.get('groups', {})
            last_updated_group = groups.get(max(groups.keys()), None)
            print("[*] Fetched Successfully Data")
            return last_updated_group
        except MongoClient as e:
            print("[*] Error to Fecth data{e}")
    def update_if_triggerd(self,user_id):
        try:
            ack = collection.find_one({"user_id":user_id})
            if ack:
                collection.update_one({"user_id":user_id},{"$set":{"triggered":True}})
                print("[*] User triggerd")
            else:
                print("[*] Not triggerd")
        except:
            print("[*] Unable to fetch")
    def only_in_group(self,full_name:str,group_id:int,user_id:int,user_name:str,is_bot:bool,location:str,profile_link:str,phone_number:int,epoctime:int):
        existing_user = collection.find_one({"user_id": user_id})
        group_name = get_config('group_id').get(str(group_id))
        if existing_user:
            try:
                collection.update_one(
                    {"user_id": user_id},
                    {"$set": {f"groups.{group_id}": group_name}}
                )
                print("[*] Data Updated Successfully")
            except Exception as e:
                print(f"[*] Error updating data: {e}")
        else:
            # Insert a new document
            user_data = {
                "id": 1,
                "full_name": full_name,
                "groups": {f"{group_id}": f"{group_name}"},
                "user_id": user_id,
                "user_name": user_name,
                "epoctime": epoctime,
                "triggerd":True,
                "is_bot":is_bot,
                "location":location,
                "profile_link": profile_link,
                "phone_number":phone_number
            }
            try:
                ack = collection.insert_one(user_data)
                if ack.acknowledged:
                    print("[*] Data Inserted Successfully")
                else:
                    print("[*] Unable to insert data")
            except Exception as e:
                print(f"[*] Error inserting data: {e}")
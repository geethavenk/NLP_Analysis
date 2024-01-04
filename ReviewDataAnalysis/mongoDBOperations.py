import json

import pymongo
import pandas as pd


class MongoDBOps:
    def __init__(self, username, pwd):
        try:
            self.username = username
            self.pwd = pwd
            self.connection_url = f"mongodb+srv://{self.username}:{self.pwd}@cluster0.qbjonjw.mongodb.net/?retryWrites=true&w=majority"
        except Exception as e:
            raise Exception(f"__init__: could not set-up connection - {str(e)}")

    def get_mongo_client(self):
        try:
            client = pymongo.MongoClient(self.connection_url)
            return client
        except Exception as e:
            raise Exception(f"get_mongo_client: could not create a mongo client - {str(e)}")

    def close_mongo_client(self, client):
        """This function closes the mongo client"""
        try:
            client.close()
        except Exception as e:
            raise Exception(f"close_mongo_client: could not close mongo client - {str(e)}")

    def is_db_present(self, db_name):
        try:
            client = self.get_mongo_client()
            if db_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"is_db_present: Failed checking if db is present or not - {str(e)}")

    def create_db(self, db_name):
        try:
            db_exists = self.is_db_present(db_name=db_name)
            if not db_exists:
                client = self.get_mongo_client()
                db = client[db_name]
                return db
            else:
                return "DB already exists"
        except Exception as e:
            raise Exception(f"create_db: Failed to create db {db_name} - {str(e)}")

    def drop_db(self, db_name):
        try:
            db_exists = self.is_db_present(db_name)
            if db_exists:
                client = self.get_mongo_client()
                client.drop_database(db_name)
                client.close()
                return True
            else:
                return "DB does not exist"
        except Exception as e:
            raise Exception(f"drop_db: Failed to delete db {db_name} - {str(e)}")

    def get_db(self, db_name):
        try:
            client = self.get_mongo_client()
            return client[db_name]
        except Exception as e:
            raise Exception(f"get_db: Failed to get db {db_name} - {str(e)}")

    def is_collection_present(self, collection_name, db_name):
        try:
            client = self.get_mongo_client()
            print(client)
            db_status = self.is_db_present(db_name=db_name)
            if db_status:
                db = client[db_name]
                if collection_name in db.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(f"is_collection_present: Failed to check if collection is present - {str(e)}")

    def create_collection(self, collection_name, db_name):
        try:
            collection_name_status = self.is_collection_present(collection_name=collection_name, db_name=db_name)
            if not collection_name_status:
                db = self.get_db(db_name=db_name)
                collection = db[collection_name]
                return collection
        except Exception as e:
            raise Exception(f"create_collection: Failed to create collection {collection_name} - {str(e)}")

    def get_collection(self, collection_name, db_name):
        try:
            db=self.get_db(db_name)
            return db[collection_name]
        except Exception as e:
            raise Exception(f"get_collection: Failed to get collection {collection_name} - {str(e)}")

    def drop_collection(self, collection_name, db_name):
        try:
            collection_name_status = self.is_collection_present(collection_name=collection_name, db_name=db_name)
            if collection_name_status:
                collection = self.get_collection(collection_name=collection_name, db_name=db_name)
                collection.drop()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"drop_collection: Failed to drop collection {collection_name} - {str(e)}")

    def insert_record(self, db_name, collection_name, record):
        try:
            collection = self.get_collection(collection_name=collection_name, db_name=db_name)
            collection.insert_one(record)
            return f"rows inserted"
        except Exception as e:
            raise Exception(f"insert_record: Failed to insert record - {str(e)}")

    def insert_records(self, db_name, collection_name, records):
        try:
            collection = self.get_collection(collection_name=collection_name, db_name=db_name)
            collection.insert_many(records)
            return f"rows inserted"
        except Exception as e:
            raise Exception(f"insert_records: Failed to insert records - {str(e)}")

    def delete_record(self, db_name, collection_name, query):
        try:
            collection_name_status = self.is_collection_present(collection_name=collection_name, db_name=db_name)
            if collection_name_status:
                collection = self.get_collection(collection_name=collection_name, db_name=db_name)
                collection.delete_one(query)
                return f"1 row deleted"
        except Exception as e:
            raise Exception(f"delete_records: Failed to delete record - {str(e)}")

    def delete_records(self, db_name, collection_name, query):
        try:
            collection_name_status = self.is_collection_present(collection_name=collection_name, db_name=db_name)
            if collection_name_status:
                collection = self.get_collection(collection_name=collection_name, db_name=db_name)
                collection.delete_many(query)
                return f"Multiple rows deleted"
        except Exception as e:
            raise Exception(f"delete_records: Failed to delete records - {str(e)}")

    def find_records(self, db_name, collection_name):
        try:
            collection_name_status = self.is_collection_present(collection_name=collection_name, db_name=db_name)
            if collection_name_status:
                collection = self.get_collection(collection_name=collection_name, db_name=db_name)
                find_records = collection.find()
                return find_records
        except Exception as e:
            raise Exception(f"find_records: Failed to find records - {str(e)}")


    def get_dataframe_collection(self, db_name, collection_name):
        try:
            all_records=self.find_records(db_name=db_name, collection_name=collection_name)
            df = pd.DataFrame(all_records)
            return df
        except Exception as e:
            raise Exception(f"get_dataframe_collection: Failed to get dataframe - {str(e)}")

    def df_to_collection(self, db_name, collection_name, df):
        try:
            collection_name_status = self.is_collection_present(collection_name=collection_name, db_name=db_name)
            df_dict = json.loads(df.T.to_json()).values()
            if collection_name_status:
                self.insert_records(db_name=db_name, collection_name=collection_name, records=df_dict)
                return f"Inserted the data from df"
            else:
                self.create_db(db_name=db_name)
                self.create_collection(collection_name=collection_name, db_name=db_name)
                self.insert_records(db_name=db_name, collection_name=collection_name, records=df_dict)
                return f"Inserted the data from df"
        except Exception as e:
            raise Exception(f"df_to_collection: Failed to insert data from dataframe into collection - {str(e)}")


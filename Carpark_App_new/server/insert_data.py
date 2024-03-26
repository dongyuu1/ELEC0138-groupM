import string
from datetime import datetime, timedelta
from .db_operations import *
from .crypt_utils import UserCryptOperator as UCO
import pandas as pd
import random
import os

first_name_list = ["James", "John", "Robert", "Michael", "William",
                    "David", "Richard", "Joseph", "Thomas", "Charles",
                    "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
                    "Donald", "Steven", "Paul", "Andrew", "Joshua"]

last_name_list = ["Smith", "Johnson", "Williams", "Brown", "Jones",
                    "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                    "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

street_name_list = [ "Main Street", "High Street", "Park Avenue", "Oak Lane", "Pine Street",
    "Maple Avenue", "Cedar Lane", "Elm Street", "Walnut Street", "Sunset Boulevard",
    "Lakeview Drive", "Riverside Drive", "Hillcrest Road", "Forest Drive", "Orchard Road",
    "Willow Lane", "Springfield Road", "Meadow Lane", "Broadway", "Cherry Lane"]


def insert():
    df = pd.read_csv("./Carpark_App_new/server/CLEANED_Parking_Bays_20240222.csv").drop(["Restriction Type"], axis=1)
    db = DBOperator("localhost", "root", "8d63tszp", "elec0138")
    """
    for _, row in df.iterrows():
        db.create_parking_lot(row["Unique Identifier"], row["Postcode"].replace(" ", ""),
        row["Road Name"].replace("'", "\\'"), row["Parking Spaces"], row["Non-diesel Tariff"], row["Diesel Tariff"])
    """
    for i in range(100):
        first_name = random.sample(first_name_list, k=1)[0]
        last_name = random.sample(last_name_list, k=1)[0]
        username = last_name + "".join(random.sample(string.ascii_letters+string.digits, 5))
        password = "".join(random.sample(string.ascii_letters+string.digits, 10))
        time = datetime.now() - timedelta(days=random.randint(10000, 20000))
        time = time.strftime('%Y-%m-%d')
        email = "".join(random.sample(string.ascii_letters+string.digits, 10))+"@gmail.com"
        address = random.sample(street_name_list, k=1)[0].replace("'", "\\'")
        postcode = "".join(random.sample(string.ascii_letters+string.digits, 6))

        crypt = UCO(key_dir="./Carpark_App_new/client/user_keys/", username=username)
        crypt.create_asy_keys_for_user()
        db_pub_key = db.get_pub_key()
        [first_name, last_name, password, email, address, postcode] = crypt.asy_encrypt_data_list(
            [first_name, last_name, password, email, address, postcode], db_pub_key)
        user_pub_key = crypt.get_pub_key()

        sym_key = db.create_user(first_name, last_name, username, password,
                                 time, email, address, postcode, user_pub_key, init_balance=1000)

        sym_key = crypt.asy_data_decryption(sym_key, decode=False)
        crypt.store_sym_key(sym_key)

    uid_list = [i for i in range(1, 100)]
    pid_list = df["Unique Identifier"].to_list()
    for i in range(400):
        uid = random.sample(uid_list, k=1)[0]
        pid = random.sample(pid_list, k=1)[0]
        start_time = datetime.now() - timedelta(days=random.randint(1, 2))
        end_time = start_time + timedelta(seconds=random.randint(10000, 100000))
        start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        number_plate = "".join(random.sample(string.ascii_letters+string.digits, 7))
        db.post_parking(uid, pid, start_time, end_time, number_plate)

if __name__ == "__main__":
    insert()

import string
from datetime import datetime, timedelta
from db_operations import *
import pandas as pd
import random

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
    df = pd.read_csv("CLEANED_Parking_Bays_20240222.csv").drop(["Restriction Type"], axis=1)
    db = DBOperator("localhost", "root", "8d63tszp", "elec0138")

    for _, row in df.iterrows():
        db.create_parking_lot(row["Unique Identifier"], row["Postcode"].replace(" ", ""),
        row["Road Name"].replace("'", "\\'"), row["Parking Spaces"], row["Non-diesel Tariff"], row["Diesel Tariff"])

    for i in range(400):
        first_name = random.sample(first_name_list, k=1)[0]
        last_name = random.sample(last_name_list, k=1)[0]
        username = "".join(random.sample(string.ascii_letters+string.digits, 10))
        password = "".join(random.sample(string.ascii_letters+string.digits, 10))
        time = datetime.now() - timedelta(days=random.randint(10000, 20000))
        time = time.strftime('%Y-%m-%d')
        email = "".join(random.sample(string.ascii_letters+string.digits, 10))+"@gmail.com"
        street_name = random.sample(street_name_list, k=1)[0].replace("'", "\\'")
        postcode = "".join(random.sample(string.ascii_letters+string.digits, 6))
        db.create_user(first_name, last_name, username,password, time, email, street_name, postcode)

    uid_list = [i for i in range(1007, 1404)]
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
import mysql.connector
from datetime import datetime

from typing import Tuple


class DBOperator:
    def __init__(self,
                 host: str,
                 user: str,
                 password: str,
                 database: str):
        """
          Initialize the connection to the database
          :param host: The IP address of the host
          :param user: The user name of the database
          :param password: The password of the database
          :param database: The name of the database used
          :return: A connection instance
          """
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Successfully connected to the database")
        except Exception as err:
            print(err)

        self.connection = connection

    def modify_query(self,
                     query: str):
        """
        Execute queries related to modifying the database, including insertion, deletion, alternation
        :param query: The query string
        :return: A status indicating whether the execution is successful
        """
        status = False
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            status = True
        except mysql.connector.Error as err:
            print(err)
        return status

    def read_query(self,
                   query: str):
        """
        Execute queries related to fetching information from the database
        :param query: The query string
        :return: The result of information retrieved
        """
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def get_user_details(self,
                         user_name: str,
                         password: str or None = None):
        """
        Get the details of a user given user_name and password
        :param user_name:  Username
        :param password: Password of the user
        :return: User details: [(u_id, first_name, last_name, user_name, password, date_of_birth,
                                email, address, billing_address, balance)]
        """
        if password is None:
            query = "Select * from user where user_name='{}'".format(user_name)
        else:
            query = "Select * from user where user_name='{}' and password='{}';".format(user_name, password)

        results = self.read_query(query)

        return results

    def get_user_details_by_id(self,
                               u_id: int):
        """
        Get the details of a user given u_id
        :param u_id: User id
        :return: User details: [(u_id, first_name, last_name, user_name, password, date_of_birth,
                                email, address, billing_address, balance)]
        """
        query = "Select * from user where u_id = {}".format(u_id)
        results = self.read_query(query)
        print(results)
        return results

    def get_parking_history_of_user(self,
                                    u_id: int,
                                    time_scope: Tuple[str or None, str or None] = None):
        """
        Get parking history of a user
        :param u_id: User id
        :param time_scope: The time scope of the history data to be retrieved.
                           The tuple includes a beginning datetime string and an end datetime string
        :return: Parking history of the user: [(h_id, start_time, end_time, stay_period, number_plate,
                                                postcode, street_name)]
        """
        # If time_scope is not specified, retrieve the entire history data
        if time_scope is None:
            query = "select h_id, start_time, end_time, stay_period, number_plate, postcode, street_name " \
                    "from history left join parking on history.p_id = parking.p_id where u_id={}".format(u_id)

        # If beginning time is not specified, retrieve all the history data earlier than end time
        elif time_scope[0] is None and time_scope[1] is not None:
            query = "select h_id, start_time, end_time, stay_period, number_plate, postcode, street_name " \
                    "from history left join parking on history.p_id = parking.p_id where u_id={} and " \
                    "start_time <= '{}'".format(u_id, time_scope[1])

        # If end time is not specified, retrieve all the history data later than beginning time
        elif time_scope[1] is None and time_scope[0] is not None:
            query = "select h_id, start_time, end_time, stay_period, number_plate, postcode, street_name " \
                    "from history left join parking on history.p_id = parking.p_id where u_id={} and " \
                    "start_time >= '{}'".format(u_id, time_scope[0])

        else:
            query = "select h_id, start_time, end_time, stay_period, number_plate, postcode, street_name " \
                    "from history left join parking on history.p_id = parking.p_id where u_id={} and " \
                    "start_time >= '{}' and start_time <= '{}'".format(u_id, time_scope[0], time_scope[1])

        results = self.read_query(query)
        return results

    def is_parking_full(self,
                        p_id: int):
        """
        Query if a parking lot is full based on p_id
        :param p_id: Parking lot id
        :return: The boolean value indicting whether the parking not is full or not.
        """
        max_occupy_query = "select max_p from parking where p_id = {}".format(p_id)
        current_occupy_query = "select count(*) from history where p_id = {} and now()<end_time".format(p_id)

        max_occupy = self.read_query(max_occupy_query)[0][0]
        current_occupy = self.read_query(current_occupy_query)[0][0]

        return False if current_occupy < max_occupy else True

    def create_user(self,
                    first_name: str,
                    last_name: str,
                    user_name: str,
                    password: str,
                    date_of_birth: str,
                    email: str,
                    address: str,
                    billing_address: str,
                    ):
        """
        Create a new user
        :param first_name: User's first name
        :param last_name: User's last name
        :param user_name: User's username
        :param password:  User's password
        :param date_of_birth: User's date of birth
        :param email: User's email
        :param address: User's address
        :param billing_address: User's billing address
        :return: None
        """
        query = "Insert into user (first_name, last_name, user_name, password, date_of_birth, email, address, " \
                "billing_address, balance) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 0)" \
            .format(first_name, last_name, user_name, password, date_of_birth, email, address, billing_address)
        duplicate_users = self.get_user_details(user_name)
        if len(duplicate_users) > 0:
            print("Failed to create a new user. Duplicated user name found.")
        else:
            if self.modify_query(query):
                print("User created successfully")

    def create_parking_lot(self,
                           postcode: str,
                           street_name: str,
                           max_p: int,
                           price: float,
                           latitude: float,
                           longitude: float):
        """
        Create a new parking lot
        :param postcode: Passcode of the parking lot's position
        :param street_name: Name of street the parking lot is located in
        :param max_p: Maximum number of cars the parking lot con contain
        :param price: Price (per hour) of the parking lot
        :param latitude: Latitude of the parking lot
        :param longitude: Longitude of the parking lot
        :return: The boolean status indicating whether the creation is successful
        """
        query = "Insert into parking (postcode, street_name, max_p, price, latitude, longitude) values " \
                "('{}', '{}', {}, {}, {}, {})".format(postcode, street_name, max_p, price, latitude, longitude)
        if self.modify_query(query):
            print("Parking lot created successfully")
            return True
        else:
            print("Parking lot registration failed")
            return False

    def post_parking(self,
                     u_id: int,
                     p_id: int,
                     start_time: str,
                     end_time: str,
                     number_plate: str):
        """
        Post a parking activity in the history table
        :param u_id: User id
        :param p_id: Parking lot id
        :param start_time: Start time of the parking
        :param end_time: End time of the parking
        :param number_plate: Number plate of the car
        :return: The boolean status indicating whether the parking registration is successful
        """
        start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        time_diff = int(end_time_obj.timestamp() - start_time_obj.timestamp())
        query = "Insert into history (u_id, p_id, start_time, end_time, stay_period, number_plate) values " \
                "({}, {}, '{}', '{}', {}, '{}')".format(u_id, p_id, start_time, end_time, time_diff, number_plate)
        price_query = "Select price from parking where p_id = {}".format(p_id)
        balance_query = "Select balance from user where u_id = {}".format(u_id)
        price = self.read_query(price_query)[0][0]
        balance = self.read_query(balance_query)[0][0]
        total_price = price * (time_diff / 3600)
        print(balance)
        if self.is_parking_full(p_id):
            print("The parking lot is full")
            return False

        if balance < total_price:
            print("User's balance is not enough")
            return False

        if self.modify_query(query):
            balance -= total_price
            print(balance)
            if self.update_balance(u_id, balance):
                print("Parking posted successfully")
                return True

        return False

    def update_balance(self,
                       u_id: int,
                       balance: float):
        """
        Update the balance of a user
        :param u_id: User id
        :param balance: The value of the new balance
        :return: The boolean status indicating whether the update is successful
        """
        update_query = "update user set balance = {} where u_id = {}".format(balance, u_id)

        if self.modify_query(update_query):
            return True
        else:
            return False

    def top_up(self,
               u_id: int,
               amount: float):
        """
        Top up the balance of a user
        :param u_id: User id
        :param amount: Amount of money
        :return: The boolean status indicating whether the update is successful
        """
        user_info = self.get_user_details_by_id(u_id)
        user_balance = user_info[0][9]
        print(user_balance)
        new_balance = user_balance + amount
        top_up_query = "update user set balance={} where u_id={}".format(new_balance, u_id)
        if self.modify_query(top_up_query):
            return True
        else:
            return False

    def delete_history_of_a_user(self,
                                 u_id: int,
                                 time_scope: Tuple[str or None, str or None] = None):
        """
        Get parking history of a user
        :param u_id: User id
        :param time_scope: The time scope of the history data to be deleted.
                           The tuple includes a beginning datetime string and an end datetime string
        :return: None
        """
        # If time_scope is not specified, delete the entire history data
        if time_scope is None:
            query = "delete from history where u_id={}".format(u_id)

        # If beginning time is not specified, delete all the history data earlier than end time
        elif time_scope[0] is None and time_scope[1] is not None:
            query = "delete from history where u_id={} and start_time <= '{}'".format(u_id, time_scope[1])

        # If end time is not specified, delete all the history data later than beginning time
        elif time_scope[1] is None and time_scope[0] is not None:
            query = "delete from history where u_id={} and start_time >= '{}'".format(u_id, time_scope[0])

        else:
            query = "delete from history where u_id={} and start_time >= '{}' and start_time <= '{}'" \
                .format(u_id, time_scope[0], time_scope[1])

        if self.modify_query(query):
            print("History deleted successfully")

    def close_connection(self):
        """
        Close the database conenction
        :return: None
        """
        self.connection.close()


if __name__ == '__main__':

    db = DBOperator("localhost", "root", "password", "elec0138")
    # db.top_up(1, 100)
    # results = db.get_user_details('hbbzwdy', '8d63tszp')
    # print(results)
    # db.create_user("Lin1", "Wang1", "linwang11", "123456", "2002-03-17", "abc1@163.com", "asdasd", "asdasd")
    # db.create_parking_lot("N1C4DD", "Gordan street1", 120, 1.1, 8.4, 9.6)
    # db.post_parking(1, 2, '2024-02-21 09:18:11', '2024-02-22 11:12:12', '123233')
    # results = db.get_parking_history_of_user(1, ('2024-02-21 08:18:10', '2024-02-21 08:18:11'))
    # print(results)
    # print(db.is_parking_full(2))
    # db.delete_history_of_a_user(1, ('2024-02-21 08:18:10', '2024-02-21 08:18:11'))add
    pass
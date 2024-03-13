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
                                email, street_name, account_balance, postcode)]
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
        :return: User details: [((u_id, first_name, last_name, user_name, password, date_of_birth,
                                email, street_name, account_balance, postcode)]
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
            query = "select h_id, start_time, end_time, stay_period, total_cost, number_plate, p_postcode, " \
                    "p_street_name from history left join parking on history.p_id = parking.p_id where u_id={}"\
                    .format(u_id)

        # If beginning time is not specified, retrieve all the history data earlier than end time
        elif time_scope[0] is None and time_scope[1] is not None:
            query = "select h_id, start_time, end_time, stay_period, total_cost, number_plate, p_postcode, " \
                    "p_street_name from history left join parking on history.p_id = parking.p_id where u_id={} and " \
                    "start_time <= '{}'".format(u_id, time_scope[1])

        # If end time is not specified, retrieve all the history data later than beginning time
        elif time_scope[1] is None and time_scope[0] is not None:
            query = "select h_id, start_time, end_time, stay_period, total_cost, number_plate, p_postcode, " \
                    "p_street_name from history left join parking on history.p_id = parking.p_id where u_id={} and " \
                    "start_time >= '{}'".format(u_id, time_scope[0])

        else:
            query = "select h_id, start_time, end_time, stay_period, total_cost, number_plate, p_postcode," \
                    " p_street_name from history left join parking on history.p_id = parking.p_id where u_id={} and " \
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
        max_occupy_query = "select parking_spaces from parking where p_id = {}".format(p_id)
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
                    street_name: str,
                    postcode: str
                    ):
        """
        Create a new user
        :param first_name: User's first name
        :param last_name: User's last name
        :param user_name: User's username
        :param password:  User's password
        :param date_of_birth: User's date of birth
        :param email: User's email
        :param street_name: User's address
        :param postcode: Postcode of the address
        :return: None
        """
        query = "Insert into user (first_name, last_name, user_name, password, date_of_birth, email, street_name, " \
                "postcode, account_balance) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 0)" \
            .format(first_name, last_name, user_name, password, date_of_birth, email, street_name, postcode)
        duplicate_users = self.get_user_details(user_name)
        if len(duplicate_users) > 0:
            print("Failed to create a new user. Duplicated user name found.")
        else:
            if self.modify_query(query):
                print("User created successfully")

    def create_parking_lot(self,
                           p_id,
                           postcode: str,
                           street_name: str,
                           parking_spaces: int,
                           non_diesel_tariff: float,
                           diesel_tariff: float,
                           ):
        """
        Create a new parking lot
        :param p_id: Unique identifier of a parking lot
        :param postcode: Passcode of the parking lot's position
        :param street_name: Name of street the parking lot is located in
        :param parking_spaces: Maximum number of cars the parking lot con contain
        :param non_diesel_tariff: Price (per hour) for non_diesel cars
        :param diesel_tariff: Price (per hour) for diesel cars
        :return: The boolean status indicating whether the creation is successful
        """
        query = "Insert into parking (p_id, p_postcode, p_street_name, parking_spaces, " \
                "non_diesel_tariff, diesel_tariff) values ({}, '{}', '{}', {}, {}, {})".\
                format(p_id, postcode, street_name, parking_spaces, non_diesel_tariff, diesel_tariff)
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

        price_query = "Select non_diesel_tariff from parking where p_id = {}".format(p_id)
        balance_query = "Select account_balance from user where u_id = {}".format(u_id)
        price = self.read_query(price_query)[0][0]
        balance = self.read_query(balance_query)[0][0]
        total_cost = price * (time_diff / 3600)
        print(balance)
        if self.is_parking_full(p_id):
            print("The parking lot is full")
            return False

        if balance < total_cost:
            print("User's balance is not enough")
            return False

        query = "Insert into history (u_id, p_id, start_time, end_time, stay_period, number_plate, total_cost) values" \
                " ({}, {}, '{}', '{}', {}, '{}', {})".format(u_id, p_id, start_time, end_time, time_diff, number_plate,
                                                         total_cost)
        if self.modify_query(query):
            balance -= total_cost
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
        update_query = "update user set account_balance = {} where u_id = {}".format(balance, u_id)

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
        user_balance = user_info[0][8]
        print(user_balance)
        new_balance = user_balance + amount
        top_up_query = "update user set account_balance={} where u_id={}".format(new_balance, u_id)
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

    db = DBOperator("localhost", "root", "8d63tszp", "elec0138")
    # db.top_up(1, 100)
    # results = db.get_user_details('hbbzwdy', '8d63tszp')
    # print(results)
    # db.create_user("Lin1", "Wang1", "linwang12", "123457", "2002-03-17", "abc1@163.com", "asdasd", "N3C4CC")
    # db.create_parking_lot(123455, "N1C4DH", "Gordan street11", 20, 1.8, 3.6)
    # db.post_parking(1, 2, '2024-02-22 09:18:11', '2024-02-24 11:12:12', '123233')
    # results = db.get_parking_history_of_user(1, ('2024-02-21 08:18:10', '2024-02-24 08:18:11'))
    # print(results)
    # print(db.is_parking_full(2))
    # db.delete_history_of_a_user(1, ('2024-02-21 08:18:10', '2024-02-21 08:18:11'))

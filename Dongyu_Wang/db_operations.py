import mysql.connector
from datetime import datetime

from typing import Tuple


def init_db_connection(host: str,
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
    return connection


def modify_query(connection,
                 query: str):
    """
    Execute queries related to modifying the database, including insertion, deletion, alternation
    :param connection: The database connection instance
    :param query: The query string
    :return: A status indicating whether the execution is successful
    """
    status = False
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        status = True
    except mysql.connector.Error as err:
        print(err)
    return status


def read_query(connection,
               query: str):
    """
    Execute queries related to fetching information from the database
    :param connection: The database connection instance
    :param query: The query string
    :return: The result of information retrieved
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(err)


def get_user_details(connection,
                     user_name,
                     password=None):
    """
    Get the details of a user given user_name and password
    :param connection: Connection instance
    :param user_name:  Username
    :param password: Password of the user
    :return: User details: [(u_id, first_name, last_name, user_name, password, date_of_birth,
                            email, address, billing_address)]
    """
    if password is None:
        query = "Select * from user where user_name='{}'".format(user_name)
    else:
        query = "Select * from user where user_name='{}' and password='{}';".format(user_name, password)

    results = read_query(connection, query)

    return results


def get_parking_history_of_user(connection,
                                u_id: int,
                                time_scope: Tuple[str or None, str or None] = None):
    """
    Get parking history of a user
    :param connection: Connection instance
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
                "from history left join parking on history.p_id = parking.p_id where u_id={} and "\
                "start_time <= '{}'".format(u_id, time_scope[1])

    # If end time is not specified, retrieve all the history data later than beginning time
    elif time_scope[1] is None and time_scope[0] is not None:
        query = "select h_id, start_time, end_time, stay_period, number_plate, postcode, street_name " \
                "from history left join parking on history.p_id = parking.p_id where u_id={} and "\
                "start_time >= '{}'".format(u_id, time_scope[0])

    else:
        query = "select h_id, start_time, end_time, stay_period, number_plate, postcode, street_name " \
                "from history left join parking on history.p_id = parking.p_id where u_id={} and " \
                "start_time >= '{}' and start_time <= '{}'".format(u_id, time_scope[0], time_scope[1])

    results = read_query(connection, query)
    return results


def create_user(connection,
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
    :param connection: Connection instance
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
            "billing_address) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')" \
        .format(first_name, last_name, user_name, password, date_of_birth, email, address, billing_address)
    duplicate_users = get_user_details(connection, user_name)
    if len(duplicate_users) > 0:
        print("Failed to create a new user. Duplicated user name found.")
    else:
        if modify_query(connection, query):
            print("User created successfully")


def create_parking_lot(connection,
                       postcode: str,
                       street_name: str):
    """
    Create a new parking lot
    :param connection: Connection instance
    :param postcode: Passcode of the parking lot's position
    :param street_name: Name of street the parking lot is located in
    :return: None
    """
    query = "Insert into parking (postcode, street_name) values ('{}', '{}')".format(postcode, street_name)
    if modify_query(connection, query):
        print("Parking lot created successfully")


def post_parking(connection,
                 u_id: int,
                 p_id: int,
                 start_time: str,
                 end_time: str,
                 number_plate: str):
    """
    Post a parking activity in the history table
    :param connection: Connection instance
    :param u_id: User id
    :param p_id: Parking lot id
    :param start_time: Start time of the parking
    :param end_time: End time of the parking
    :param number_plate: Number plate of the car
    :return: None
    """
    start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    time_diff = int(end_time_obj.timestamp() - start_time_obj.timestamp())
    print(time_diff)
    query = "Insert into history (u_id, p_id, start_time, end_time, stay_period, number_plate) values " \
            "({}, {}, '{}', '{}', {}, '{}')".format(u_id, p_id, start_time, end_time, time_diff, number_plate)
    if modify_query(connection, query):
        print("Parking posted successfully")


def delete_history_of_a_user(connection,
                             u_id: int,
                             time_scope: Tuple[str or None, str or None] = None):
    """
    Get parking history of a user
    :param connection: Connection instance
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
        query = "delete from history where u_id={} and start_time >= '{}' and start_time <= '{}'"\
                .format(u_id, time_scope[0], time_scope[1])

    if modify_query(connection, query):
        print("History deleted successfully")



if __name__ == '__main__':
    # db_connection = init_db_connection('localhost', 'root', 'password', 'elec0138')
    # results = get_user_details(db_connection, 'hbbzwdy', '8d63tszp')
    # print(results)
    # create_user(db_connection, "Lin", "Wang", "linwang1", "123456", "2002-03-17", "abc1@163.com", "asdasd", "asdasd")
    # create_parking_lot(db_connection, "N2C4BD", "Gordan Street")
    # post_parking(db_connection, 1, 2, '2024-02-21 08:18:11', '2024-02-21 09:12:12', '112233')
    # results = get_parking_history_of_user(db_connection, 1, ('2024-02-21 08:18:10', '2024-02-21 08:18:11'))
    # print(results)
    # delete_history_of_a_user(db_connection, 1, ('2024-02-21 08:18:10', '2024-02-21 08:18:11'))
    pass
from Carpark_App_new.client.Carpark_App import app
from Carpark_App_new.server.insert_data import insert
if __name__ == "__main__":
    # insert() is for generating simulated data for an empty database.
    # The data has already been contained in the sql file
    # insert()
    app.run(host='0.0.0.0')

from flask import Flask, render_template, request, redirect, session
from ..server.db_operations import DBOperator
from .crypt_utils import UserCryptOperator as UCO

app = Flask(__name__)
db = DBOperator("localhost", "root", "8d63tszp", "ELEC0138")
crypt = None
u_id = -1

login_attempts = {}
MAX_LOGIN_ATTEMPTS = 100


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        global crypt
        # Receive the registration data from a user
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        email = request.form['email']
        address = request.form['address']
        postcode = request.form['postcode']

        crypt = UCO(key_dir="./Carpark_App_new/client/user_keys/", username=username)
        # Generate a public/private key pair for the user
        crypt.create_asy_keys_for_user()
        # Get the public key from the database server
        db_pub_key = db.get_pub_key()
        # Encrypt the data using server's public key
        [first_name, last_name, password, email, address, postcode] = crypt.asy_encrypt_data_list(
            [first_name, last_name, password, email, address, postcode], db_pub_key)
        user_pub_key = crypt.get_pub_key()
        # Send the encrypted data and user's public key to the server, and receive user's encrypted symmetric key
        sym_key = db.create_user(first_name, last_name, username, password,
                                        dob, email, address, postcode, user_pub_key)
        # Decrypt the symmetric key using user's private key
        sym_key = crypt.asy_data_decryption(sym_key, decode=False)
        # Store the symmetric key
        crypt.store_sym_key(sym_key)

        crypt = None
        return redirect('/')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global u_id
    global crypt
    ip_address = request.remote_addr
    if ip_address in login_attempts:
        if login_attempts[ip_address] >= MAX_LOGIN_ATTEMPTS:
            return "Maximum login attempts exceeded."
    else:
        login_attempts[ip_address] = 0
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        crypt = UCO(key_dir="./Carpark_App_new/client/user_keys/", username=username)
        # Load the user's symmetric key
        sym_key = crypt.load_sym_key()

        if sym_key is None:
            login_attempts[ip_address] += 1
            return "User keys not found"

        # Encrypt the password using the symmetric key
        password = crypt.sym_data_encryption(password, sym_key)
        # Send username and password to the server, and receive user's encrypted data
        user_details = db.get_user_details(username, password)[0]

        if not user_details:
            login_attempts[ip_address] += 1
            return "Invalid username or password!"

        user_details = list(user_details)
        # Which columns are encrypted
        entryped_index = [1, 2, 4, 6, 7, 9]
        print("The encrypted user details:")
        print(user_details)
        # Decrypt the data using the symmetric key
        for i in entryped_index:
            user_details[i] = crypt.sym_data_decryption(user_details[i], sym_key)
        print("The decrypted user details:")
        print(user_details)

        u_id = user_details[0]
        return redirect('/parking_register')
    return render_template('login.html')

@app.route('/parking_register', methods=['GET', 'POST'])
def parking_register():
    global u_id
    if request.method == 'POST':
        street_name = request.form['street_name']
        postcode = request.form['postcode']
        car_plate = request.form['car_plate']
        start_time = request.form['start_time'].replace("T", " ") + ":00"
        end_time = request.form['end_time'].replace("T", " ") + ":00"
        p_id = db.get_parking_lot_details(postcode)[0][0]
        db.post_parking(u_id, p_id, start_time, end_time, car_plate)
        
        return redirect('/payment_options')
        
    
    return render_template('parking_register.html')



@app.route('/payment_options')
def payment_options():
    return render_template('payment_options.html')

@app.route('/card_payment', methods=['GET', 'POST'])
def card_payment():
    if request.method == 'POST':
        cardholder_name = request.form['cardholder_name']
        card_number = request.form['card_number']
        card_expiry = request.form['expiry_date']
        card_cvv = request.form['cvv']

        return redirect('/parking_view')
    
    return render_template('card_payment.html')

@app.route('/balance_payment', methods=['GET', 'POST'])
def balance_payment():
    if request.method == 'POST':
        top_up_amount = float(request.form['top_up_amount'])

        top_up(u_id, top_up_amount)

    user_balance_data = db.get_user_details_by_id(u_id)

    if user_balance_data:
        user_balance = user_balance_data[0][8]
    else:
        user_balance = None

    return render_template('balance_payment.html', balance=user_balance)

def top_up(user_id, amount):

    user_info = db.get_user_details_by_id(user_id)
    if user_info:
        user_balance = user_info[0][8]
        new_balance = user_balance + amount
        return db.update_balance(user_id, new_balance)
    else:
        return False

@app.route('/parking_view', methods=['GET', 'POST'])
def parking_view():
    global u_id
    if request.method == 'POST':
        pass

    parking_history = db.get_parking_history_of_user(u_id)

    return render_template('parking_view.html', parking_history=parking_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
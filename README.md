# ELEC0138 Security_and_Privacy groupM
This repository contains the code and documentation for a Carpark Security and Privacy Defense project.
The final version of the code is in the 'Carpark_App_new' folder which contains the code of:
1. Python Flask Webapp
2. Website HTML script
3. Python Database operations
4. DOS & DDOS attack and defense
5. SQL injection attack and defense
6. Brute force attack and defense



## Initialization
Please run anaconda and create the environment with the following command:
```
cd path/to/ELEC0138-groupM
conda env create -f environment.yaml
conda activate ELEC_0138
```

To initialize the database, please use ELEC0138.sql in the ./Carpark_App_new/server folder.

In the mysql command line client, please run the following commands:
```
create database ELEC0138;
use ELEC0138;
source path/to/the/file/ELEC0138.sql
```

To load the keys of the simulated users in the database, please navigate to the ./Carpark_App_new/client/user_keys
folder and unzip the file unzip_it.zip.

To make sure that the username and password align with those of the mysql database, please navigate to
./Carpark_App_new/client/Carpark_App.py and adjust the paramters of the code in the 6th line:
```
db = DBOperator("localhost", "root", "8d63tszp", "ELEC0138")
```
The first parameter is the host ip address, the second one is the username of the database, the third one is the
password of the database, and the forth one is the database name. 

## Launch
To launch the Carpark App, please run:
```
python main.py
```

To perform different kinds of attacks & defenses please refer to the readme files in the folder ./Carpark_App_new
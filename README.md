csvtools-py
=========== 

reader.py
---------
Provides reading functionality through the open_csv_file() and write_csv_file() functions. WHEN GENERATING CODES/IDS FOR MEMBERS USE THE generate_unique_code() FUNCTION.
Will also generate members with just their uid, however if you want to add or update people's email or name you have to use insert.py. reader.py assumes that its only handling Uids so it will only make details for them, once again if you want to insert a new user that has no uid you have to do it manually with insert.py.
###USAGE:
reader.py [-i, --input] [-o, --output]

emailer.py
----------
insert.py
---------

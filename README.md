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
Will take a csv file, a subject line and a message and will automatically email a personalised copy of the message to everyone in the scv file.
If the message contains tags that are in the csv file as headers it will insert them into the message to personalise it. An example
is Hello {name}.
###USAGE:
emailer.py [-i, --input] [-s --subject] message is redirected from standard input eg < message.txt or <<< "Your message"

insert.py
---------
Inserts values into a csv file
###USAGE:
To insert details to an account that already exists
insert.py -u update [-n --name][-e --email][-i --input][-c --id]
To insert details of a new user
insert.py -u add [-n --name][-e --email][-i --input]
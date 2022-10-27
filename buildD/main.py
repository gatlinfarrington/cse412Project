
# once in psql:
# CREATE DATABASE CSE412;
# \c cse412
# I downloaded pycharm community edition because of the issues I was having with psycopg2
# Once in pycharm I was able to hover over the import and download there and it seems to be working
import psycopg2
import csv
#Change this line to your database name and username...
conn = conn = psycopg2.connect(database="cse412", user = "gatlinfarrington", password = "pass123", host = "127.0.0.1", port = "5432")


print("Opened Database")
cursor = conn.cursor()
#testing to make sure connection worked
print("PSQL server information")
print(conn.get_dsn_parameters(), "\n")
SelectAthleteQuery = "SELECT * FROM athlete;"
cursor.execute(SelectAthleteQuery)
record = cursor.fetchall()
print("Current Database Contents: ")
print(record)
conn.commit()

fName = ""
lName = ""
country = ""
event = ""
date = ""
banLength = ""
substance = ""
print("Building the database \n")
dopefile = 'doping.csv'
aid = 1
bid = 1
banQuery = "INSERT INTO ban (bid, substance, banlength, date, aid) VALUES ("
athleteQuery = "INSERT INTO athlete (fname, lname, country, event, aid) VALUES ('Gatlin', 'Farrington', 'USA', 'Speed Walking', 1);"
with open(dopefile, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        fName = ""
        lName = ""
        country = ""
        event = ""
        date = ""
        banLength = ""
        substance = ""
        #
        #Ahmed Abd El Raouf,�Egypt,Hammer throw,2008,Norandrosterone,2 years,
        fName = row[0].split(" ", 1)[0]
        if(len(row[0].split(" ", 1)) > 1):
            lName = row[0].split(" ", 1)[1]
        country = row[1]
        event = row[2]
        event.replace("\'", "")
        date = row[3]
        date.replace("\'", "")
        date = "".join(filter(lambda char: char != "'", date))
        if len(date) > 24:
            date = substance[0:24]
        substance = row[4]
        substance.replace("\'", "")
        substance = "".join(filter(lambda char: char != "'", substance))
        if len(substance) > 250:
            substance = substance[0:250]
        banLength = row[5]
        if len(banLength) > 250:
            banLength = banLength[0:250]
        bid += 1
        if fName == "":
            print("SAME ATHLETE NEW DOPING CASE")
            banQuery = f'INSERT INTO ban (bid, substance, banlength, date, aid) VALUES (\'{bid}\', \'{substance}\', \'{banLength}\', \'{date}\', {aid});'
            cursor.execute(banQuery)

        else:
            aid += 1
            athleteQuery = f'INSERT INTO athlete (fname, lname, country, event, aid) VALUES (\'{fName}\', \'{lName}\', \'{country}\', \'{event}\', {aid});'
            cursor.execute(athleteQuery)
            banQuery = f'INSERT INTO ban (bid, substance, banlength, date, aid) VALUES (\'{bid}\', \'{substance}\', \'{banLength}\', \'{date}\', {aid});'
            cursor.execute(banQuery)

conn.commit()
print("\n-------------------\nFINISHED\n-------------------\n")
conn.close()
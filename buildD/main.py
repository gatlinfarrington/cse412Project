
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
print(conn.get_dsn_parameters(), "\n") #Shows that the connection has happened

#DEBUG
# SelectAthleteQuery = "SELECT * FROM athlete;" 
# cursor.execute(SelectAthleteQuery) #DEBUG
# record = cursor.fetchall() 
# print("Current Database Contents: ")
# print(record)
# conn.commit()

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
#defaults, these queries will get rewritten every time so it does not matter their value here
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
        #Ahmed Abd El Raouf, Egypt,Hammer throw,2008,Norandrosterone,2 years,
        #First and last name are the same field in the csv
        fName = row[0].split(" ", 1)[0]
        if(len(row[0].split(" ", 1)) > 1): #if there is no name, or only a first this will prevent the errror
            lName = row[0].split(" ", 1)[1]
        country = row[1]
        event = row[2]
        event.replace("\'", "") #there is sometimes a ' in the strings, this will make SQL think the string is closed so we need to get rid of that
        date = row[3]
        date.replace("\'", "")
        date = "".join(filter(lambda char: char != "'", date)) #this is a better way of getting rid of the 's, sometimes the replace didn't work for some reason
        if len(date) > 24:
            date = substance[0:24]
        substance = row[4]
        substance.replace("\'", "") 
        substance = "".join(filter(lambda char: char != "'", substance))
        if len(substance) > 250: #a couple instances where there are too many characters
            substance = substance[0:250] #substring in that case
        banLength = row[5]
        if len(banLength) > 250: #a couple instances where there are too many characters
            banLength = banLength[0:250] #substring in that case
        bid += 1
        if fName == "": #if there is no first nam, that means that the same person has multiple bans
            print("SAME ATHLETE NEW DOPING CASE") #Debug
            banQuery = f'INSERT INTO ban (bid, substance, banlength, date, aid) VALUES (\'{bid}\', \'{substance}\', \'{banLength}\', \'{date}\', {aid});'
            cursor.execute(banQuery)

        else: #otherwise we are starting a new person
            aid += 1 #only when there is a new person should teh aid be incremented
            athleteQuery = f'INSERT INTO athlete (fname, lname, country, event, aid) VALUES (\'{fName}\', \'{lName}\', \'{country}\', \'{event}\', {aid});'
            cursor.execute(athleteQuery)
            banQuery = f'INSERT INTO ban (bid, substance, banlength, date, aid) VALUES (\'{bid}\', \'{substance}\', \'{banLength}\', \'{date}\', {aid});'
            cursor.execute(banQuery)

conn.commit() #send all queries into SQL
print("\n-------------------\nFINISHED\n-------------------\n")
conn.close() #close the connection
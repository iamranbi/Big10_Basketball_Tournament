import csv
import sqlite3 as sqlite

# Creates a database called big10.sqlite
def create_tournament_db():
    try:
        conn=sqlite.connect('big10.sqlite')
    except:
        print("Error: fail to create the SQLite database")
    cur=conn.cursor()
    statement='''DROP TABLE IF EXISTS 'Teams';'''
    cur.execute(statement)
    statement='''DROP TABLE IF EXISTS 'Games';'''
    cur.execute(statement)
    statement='''DROP TABLE IF EXISTS 'Rounds';'''
    cur.execute(statement)
    conn.commit()
    #creat table 'Teams'
    st_create_teams= '''
        CREATE TABLE 'Teams' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            'Seed' TEXT,
            'Name' TEXT,
            'ConfRecord' TEXT
            );
        '''
    cur.execute(st_create_teams)
    conn.commit()
    #creat table 'Games'
    st_create_games= '''
        CREATE TABLE 'Games' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            'Winner' TEXT,
            'Loser' TEXT,
            'WinnerScore' INTEGER,
            'LoserScore' INTEGER,
            'Round' TEXT,
            'Time' TEXT
            );
        '''
    cur.execute(st_create_games)
    conn.commit()
    #creat table 'Rounds'
    st_create_rounds= '''
        CREATE TABLE 'Rounds' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            'Name' TEXT,
            'Date' TEXT
            );
        '''
    cur.execute(st_create_rounds)
    conn.close()


# Populates big10.sqlite database using csv files
def populate_tournament_db():
    conn = sqlite.connect('big10.sqlite')
    cur = conn.cursor()
    #import data teams.csv
    with open('teams.csv', 'r') as csv_file1:
        f1=csv.reader(csv_file1)
        teams=list(f1)
    #import data games.csv
    with open('games.csv', 'r') as csv_file2:
        f2=csv.reader(csv_file2)
        games=list(f2)
    #import data rounds.csv
    with open('rounds.csv', 'r') as csv_file3:
        f3=csv.reader(csv_file3)
        rounds=list(f3)
    #populate table 'Teams'
    teams=teams[1:]
    for t in teams:
        insertion_teams=(None, t[0], t[1], t[2])
        st_save_teams="INSERT INTO 'Teams' VALUES (?, ?, ?, ?)"
        cur.execute(st_save_teams, insertion_teams)
    conn.commit()
    #populate table 'Games'
    games=games[1:]
    for g in games:
        insertion_games=(None, g[0], g[1], int(g[2]), int(g[3]), g[4], g[5])
        st_save_games="INSERT INTO 'Games' VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(st_save_games, insertion_games)
    st_winner_id="UPDATE Games SET Winner=(SELECT Teams.Id FROM Teams WHERE Games.Winner=Teams.Name)"
    st_loser_id="UPDATE Games SET Loser=(SELECT Teams.Id FROM Teams WHERE Games.Loser=Teams.Name)"
    cur.execute(st_winner_id)
    cur.execute(st_loser_id)
    conn.commit()
    #populate table 'Rounds'
    rounds=rounds[1:]
    for r in rounds:
        insertion_rounds=(None, r[0], r[1])
        st_save_rounds="INSERT INTO 'Rounds' VALUES (?, ?, ?)"
        cur.execute(st_save_rounds, insertion_rounds)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tournament_db()
    populate_tournament_db()

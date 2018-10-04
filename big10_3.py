
import sqlite3 as sqlite
import csv

# generate 'TVNetworks' table
conn=sqlite.connect('big10.sqlite')
cur=conn.cursor()
st_create_table= '''
    CREATE TABLE 'TVNetworks' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        'Name' TEXT,
        'Channel' TEXT
        );
    '''
cur.execute(st_create_table)
conn.commit()

# import data to table
with open('TVNetworks.csv', 'r') as csv_file1:
    f=csv.reader(csv_file1)
    a=list(f)
a=a[1:]
for r in a:
    insertion=(None, r[0], r[1])
    st_save="INSERT INTO 'TVNetworks' VALUES (?, ?, ?)"
    cur.execute(st_save, insertion)
conn.commit()

# add a column named 'Channel' to the 'Games' table
cur.execute("ALTER TABLE Games ADD COLUMN 'Channel' TEXT")
conn.commit()
conn.close()

# implement the function
def add_channel_for_round(network_name, round_name):
    conn=sqlite.connect('big10.sqlite')
    cur=conn.cursor()
    st_1="UPDATE Games SET Channel=(SELECT Channel FROM TVNetworks WHERE NAME=?) WHERE Round=(SELECT Id FROM Rounds WHERE NAME=?)"
    st_1_values=(network_name, round_name,)
    try:
        cur.execute(st_1,st_1_values)
        conn.commit()
        re='Added channel'
    except:
        re='Fail to add channel'
    conn.close()
    return re
    
# implement the function
def check_teams_for_network(network_name):
    conn=sqlite.connect('big10.sqlite')
    cur=conn.cursor()
    l=[]
    st_2="SELECT t1.Name, t2.Name FROM Games JOIN TVNetworks ON TVNetworks.Channel=Games.Channel "
    st_2+="JOIN Teams AS t1 ON t1.Id=Games.Winner JOIN Teams AS t2 ON t2.Id=Games.Loser "
    st_2+="WHERE TVNetworks.Name='"+network_name+"'"
    cur.execute(st_2)
    for i in cur:
        for j in i:
            l.append(j)
    ll=list(set(l))
    print('Teams who played on '+network_name+':')
    for z in ll:
        print(z)
    conn.close()

if __name__ == "__main__":
    ## sample
    #status=add_channel_for_round("BTN","Quarterfinals")
    #print(status)
    #check_teams_for_network("BTN")

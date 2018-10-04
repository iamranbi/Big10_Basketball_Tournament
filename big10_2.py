import sqlite3 as sqlite

# Params: game_id (ie. 1)
# Returns: A string formatted as follows with the game’s information:
# {Round Name}: ({Winner Seed}) {Winner} defeated ({Loser Seed}) {Loser}
# {Winner Score}-{Loser Score}
def get_info_for_game(game_id):
    conn=sqlite.connect('big10.sqlite')
    cur=conn.cursor()
    st1="SELECT Rounds.Name, t1.Seed, t1.Name, t2.Seed, t2.Name, Games.WinnerScore, Games.LoserScore "
    st1+="FROM Games JOIN Rounds ON Rounds.Id=Games.Round JOIN Teams AS t1 ON t1.Id=Games.Winner "
    st1+="JOIN Teams AS t2 ON t2.Id=Games.Loser WHERE Games.Id="
    st1+=str(game_id)
    cur.execute(st1)
    for row in cur:
        r=row[0]+': ('+row[1]+')'+row[2]+' defeated ('+row[3]+')'+row[4]+' '+str(row[5])+'-'+str(row[6])
    conn.close()
    return r


# Params: team_name (ie. “Michigan”)
# Returns: prints all of the round names a team won and the corresponding scores
def print_winning_rounds_for_team(team_name):
    conn=sqlite.connect('big10.sqlite')
    cur=conn.cursor()
    st2="SELECT Rounds.Name, Games.WinnerScore, Games.LoserScore FROM Games JOIN Rounds ON Rounds.Id=Games.Round "
    st2+="JOIN Teams AS t1 ON t1.Id=Games.Winner WHERE t1.Name='"+team_name+"' ORDER BY Rounds.Id"
    cur.execute(st2)
    print(team_name+' won:')
    for row in cur:
        print(row[0]+': '+str(row[1])+'-'+str(row[2]))
    conn.close()


# Update the database to include the following Championship game information:
#   Round Name: “Championship”
#   Round Date: “03-04-18”
#   Winner: “Michigan”
#   Loser: “Purdue”
#   WinnerScore: 75
#   LoserScore: 66
#   Time: “4:30pm”
def add_championship_info():
    conn=sqlite.connect('big10.sqlite')
    cur=conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Rounds WHERE Name='Championship'")
    exist_round=cur.fetchone()[0]
    if exist_round==0:
        st3_1="INSERT INTO Rounds VALUES (?,?,?)"
        st3_1_values=(None,'Championship','03-04-18')
        cur.execute(st3_1,st3_1_values)
        conn.commit()
        r='Added round. '
    else:
        r='Already Exists. '
    cur.execute("SELECT COUNT(*) FROM Games WHERE WinnerScore=75 AND LoserScore=66 AND Time='4:30pm'")
    exist_game=cur.fetchone()[0]
    if exist_game==0:
        st3_2='''
            INSERT INTO Games
            SELECT ?,t1.Id,t2.Id,?,?,Rounds.Id,?
            FROM Teams AS t1,Teams AS t2, Rounds
            WHERE t1.NAME='Michigan'
                AND t2.NAME='Purdue'
                AND Rounds.Name='Championship'
        '''
        st3_2_values=(None,75,66,'4:30pm',)
        cur.execute(st3_2,st3_2_values)
        conn.commit()
        r+='Added game.'
    else:
        r+='Failed to add game: already exists'
    conn.close()
    return r


# Params: round_id (ex. 1), date (ie. “03-05-18”), time (ie. “5:30pm”)
# Returns: update the date for the specified round and the times for each of the games in that round
def update_schedule_for_round(round_id, date, time):
    conn=sqlite.connect('big10.sqlite')
    cur=conn.cursor()
    st4_1="UPDATE Rounds SET Date=? WHERE Id=?"
    st4_1_values=(date,round_id,)
    st4_2="UPDATE Games SET Time=? WHERE Round=?"
    st4_2_values=(time,round_id,)
    try:
        cur.execute(st4_1,st4_1_values)
        cur.execute(st4_2,st4_2_values)
        conn.commit()
        r='Updated schedule.'
    except:
        r='Failed to update schedule.'
    conn.close()
    return r

if __name__ == "__main__":
    ## sample
    #game_info = get_info_for_game(1)
    #print(game_info)
    
    #print_winning_rounds_for_team("Purdue")
    
    #status = add_championship_info()
    #print(status)

    #status2 = update_schedule_for_round(5,'03-05-18','12:00pm')
    #print(status2)

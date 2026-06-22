from DataAccess.Util.LeagueDBCommandBase import LeagueDBCommandBase
from DataAccess.LeagueDatabase import LeagueDatabase;
import sqlite3

def test_LeagueDBCommandBase():
    conn = sqlite3.connect(':memory:') 
    try:
        cmd = LeagueDBCommandBase(conn)
        cmd.sendVoidCommand('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
        cmd.sendVoidCommand('INSERT INTO test (name) VALUES (?)', ('test1',))
        result = cmd.sendScalarCommand('SELECT name FROM test WHERE id = ?', (1,))
        assert result[0] == 'test1'
        results = cmd.sendQueryCommand('SELECT * FROM test')
        assert len(results) == 1
        assert results[0][1] == 'test1'
        conn.close() #destroy the database when the connection closes
    except Exception as e:
        conn.close() #destroy the database when the connection closes
        assert False, f"Exception occurred: {e}"

def test_LeagueDatabase():
    try:
        db = LeagueDatabase('',':memory:')# use in memory
        assert isinstance(db.SummonerDB, object)
        assert isinstance(db.MatchesDB, object)
        del db
    except Exception as e:
        assert False, f"Exception occurred: {e}"

def test_SummonerDB():
    try:
        db = LeagueDatabase('',':memory:')# use in memory
        db.SummonerDB.initUserToSummonerMapping()
        assert db.SummonerDB.getAllUsers() == []
        del db
    except Exception as e:
        assert False, f"Exception occurred: {e}"
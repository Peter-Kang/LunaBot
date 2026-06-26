from DataAccess.LeagueDatabase import LeagueDBCommandBase
import sqlite3

def test_LeagueDBCommandBase():
    db = LeagueDBCommandBase('',':memory:')# use in memory
    try:
        assert isinstance(db, object)
        db.sendVoidCommand("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)", ())
        db.sendScalarCommand("INSERT INTO test (name) VALUES (?)", ("test_name",))
        result = db.sendScalarCommand("SELECT name FROM test WHERE id = ?", (1,))
        assert result[0] == "test_name"
        result =db.sendQueryCommand("SELECT * FROM test", ())
        assert result[0][1] == "test_name"
        del db
    except Exception as e:
        del db
        assert False, f"Exception occurred: {e}"
    
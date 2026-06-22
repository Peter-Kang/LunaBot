from DataAccess.Util.LeagueDBCommandBase import LeagueDBCommandBase
import sqlite3

def test_LeagueDBCommandBase():
    conn = sqlite3.connect(':memory:')
    cmd = LeagueDBCommandBase(conn)
    cmd.sendVoidCommand('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
    cmd.sendVoidCommand('INSERT INTO test (name) VALUES (?)', ('test1',))
    result = cmd.sendScalarCommand('SELECT name FROM test WHERE id = ?', (1,))
    assert result[0] == 'test1'
    results = cmd.sendQueryCommand('SELECT * FROM test')
    assert len(results) == 1
    assert results[0][1] == 'test1'

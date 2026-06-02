import sqlite3

class LeagueDBCommandBase:
        
    def __init__(self, sqliteConnection:sqlite3.Connection):
        self.sqliteConnection:sqlite3.Connection = sqliteConnection

    def sendVoidCommand(self, query:str, args:tuple=()) -> None:
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query,args)
        cursor.close()
        self.sqliteConnection.commit()

    def sendScalarCommand(self, query:str, args:tuple=()) -> any:
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query,args)
        result = cursor.fetchone()
        cursor.close()
        self.sqliteConnection.commit()
        return result

    def sendQueryCommand(self, query:str, args:tuple=()) -> list[any]:
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query,args)
        result = cursor.fetchall()
        cursor.close()
        self.sqliteConnection.commit()
        return result


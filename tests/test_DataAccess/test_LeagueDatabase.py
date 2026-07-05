from DataAccess.LeagueDatabase import LeagueDatabase;

def test_LeagueDatabase():
    try:
        db = LeagueDatabase('',':memory:')# use in memory
        assert isinstance(db.SummonerDB, object)
        assert isinstance(db.MatchesDB, object)
        del db
    except Exception as e:
        assert False, f"Exception occurred: {e}"
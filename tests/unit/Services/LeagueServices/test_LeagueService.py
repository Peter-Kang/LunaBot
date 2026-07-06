import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from Services.LeagueServices.league import league
from Services.LeagueServices.API.Champions import Champions as ChampionsAPI
from Services.LeagueServices.API.Summoners import Summoners as SummonersAPI
from Services.LeagueServices.API.Matches import Matches as MatchesAPI, Match
from Services.LeagueServices.DataUtil.SummonerStatSummary import SummonerStatSummary, SummonerStatSummaryResults
from Services.LeagueServices.DataUtil.ChampionStats import ChampionStats
from DataAccess.LeagueDatabase import LeagueDatabase


@pytest.fixture
def mock_db():
    """Mock database object"""
    db = Mock(spec=LeagueDatabase)
    db.SummonerDB = Mock()
    db.MatchesDB = Mock()
    db.SummonerDB.getAllUsers.return_value = []
    db.MatchesDB.getMatches.return_value = []
    return db


@pytest.fixture
def league_service(mock_db):
    """Create a league service instance with mocked dependencies"""
    with patch('Services.LeagueServices.league.ChampionsAPI'), \
         patch('Services.LeagueServices.league.SummonersAPI'), \
         patch('Services.LeagueServices.league.MatchesAPI'):
        service = league("test_api_key", mock_db)
    return service


class TestLeagueInit:
    """Test league class initialization"""
    
    def test_init_sets_api_key(self, league_service):
        assert league_service.RIOT_API_KEY == "test_api_key"
    
    def test_init_sets_database(self, mock_db, league_service):
        assert league_service.db == mock_db
    
    def test_init_creates_empty_caches(self, league_service):
        assert isinstance(league_service.userToSummonerPUUID, dict)
        assert isinstance(league_service.matchCache, dict)
        assert len(league_service.userToSummonerPUUID) == 0
        assert len(league_service.matchCache) == 0
    
    def test_init_creates_api_objects(self, league_service):
        assert league_service.ChampionAPI is not None
        assert league_service.UserSummonerAPI is not None
        assert league_service.SummonerMatchAPI is not None
    
    def test_init_creates_summoner_stat(self, league_service):
        assert isinstance(league_service.SummonerStat, SummonerStatSummary)


class TestInitUserToSummonerPUUID:
    """Test __initUserToSummonerPUUID method"""
    
    def test_populates_user_to_puuid_mapping(self):
        """Test that user to PUUID mapping is populated from database"""
        mock_db = Mock(spec=LeagueDatabase)
        mock_db.SummonerDB = Mock()
        mock_db.MatchesDB = Mock()
        mock_db.SummonerDB.getAllUsers.return_value = [
            ("user1", "puuid1"),
            ("user2", "puuid2"),
        ]
        mock_db.MatchesDB.getMatches.return_value = []
        
        with patch('Services.LeagueServices.league.ChampionsAPI'), \
             patch('Services.LeagueServices.league.SummonersAPI'), \
             patch('Services.LeagueServices.league.MatchesAPI'):
            service = league("test_key", mock_db)
        
        assert service.userToSummonerPUUID["user1"] == "puuid1"
        assert service.userToSummonerPUUID["user2"] == "puuid2"
    
    def test_handles_empty_database(self, mock_db):
        mock_db.MatchesDB.getMatches.return_value = []
        
        with patch('Services.LeagueServices.league.ChampionsAPI'), \
             patch('Services.LeagueServices.league.SummonersAPI'), \
             patch('Services.LeagueServices.league.MatchesAPI'):
            service = league("test_key", mock_db)
        
        assert len(service.userToSummonerPUUID) == 0


class TestRegister:
    """Test register method"""
    
    def test_register_valid_riot_id(self, league_service):
        league_service.UserSummonerAPI.getPUUIDFromRiotID = Mock(return_value="new_puuid")
        league_service.db.SummonerDB.addOrUpdateUserToSummonerMapping = Mock()
        
        result = league_service.register("user123", "SummonerName#NA1")
        
        assert result == "new_puuid"
        assert league_service.userToSummonerPUUID["user123"] == "new_puuid"
        league_service.db.SummonerDB.addOrUpdateUserToSummonerMapping.assert_called_once_with(
            "user123", "SummonerName#NA1", "new_puuid"
        )
    
    def test_register_invalid_riot_id(self, league_service):
        league_service.UserSummonerAPI.getPUUIDFromRiotID = Mock(return_value="")
        league_service.db.SummonerDB.addOrUpdateUserToSummonerMapping = Mock()
        
        result = league_service.register("user123", "InvalidID")
        
        assert result == ""
        league_service.db.SummonerDB.addOrUpdateUserToSummonerMapping.assert_not_called()


class TestRandomChampion:
    """Test randomChampion method"""
    
    def test_random_champion(self, league_service):
        mock_champion = "Ahri"
        league_service.ChampionData = Mock()
        league_service.ChampionData.randomChampion = Mock(return_value=mock_champion)
        
        result = league_service.randomChampion()
        
        assert result == mock_champion
        league_service.ChampionData.randomChampion.assert_called_once()


class TestUpdateChampionList:
    """Test UpdateChampionList method"""
    
    @pytest.mark.asyncio
    async def test_update_champion_list_success(self, league_service):
        mock_result = {"data": "champion_data"}
        league_service.ChampionAPI.Update = AsyncMock(return_value=mock_result)
        league_service.ChampionAPI.version = "1.0.0"
        
        with patch('Services.LeagueServices.league.ChampionStats') as mock_stats:
            await league_service.UpdateChampionList()
            mock_stats.assert_called_once_with("1.0.0", mock_result)
    
    @pytest.mark.asyncio
    async def test_update_champion_list_none_result(self, league_service):
        league_service.ChampionAPI.Update = AsyncMock(return_value=None)
        
        await league_service.UpdateChampionList()
        # Should not raise exception, just return


class TestUpdateMissingMatchesData:
    """Test updateMissingMatchesData method"""
    
    def test_update_missing_matches_data(self, league_service):
        mock_match1 = Mock(spec=Match)
        mock_match1.matchID = "match1"
        mock_match1.EndEpoch = 1234567890
        mock_match1.results = {"data": "test"}
        
        league_service.db.MatchesDB.clearPastDays = Mock()
        league_service.db.MatchesDB.addMatches = Mock()
        
        league_service.updateMissingMatchesData([mock_match1])
        
        league_service.db.MatchesDB.clearPastDays.assert_called_once_with(7)
        league_service.db.MatchesDB.addMatches.assert_called_once()
        assert league_service.matchCache["match1"] == mock_match1


class TestGetListOfMatches:
    """Test getListOfMatches method"""
    
    def test_get_list_of_matches(self, league_service):
        mock_match1 = Mock(spec=Match)
        mock_match1.matchID = "match1"
        mock_match2 = Mock(spec=Match)
        mock_match2.matchID = "match2"
        
        league_service.matchCache = {"match1": mock_match1, "match2": mock_match2}
        
        result = league_service.getListOfMatches(["match1", "match2"])
        
        assert len(result) == 2
        assert result[0] == mock_match1
        assert result[1] == mock_match2


class TestPopulateMissingMatches:
    """Test populateMissingMatches method"""
    
    @pytest.mark.asyncio
    async def test_populate_missing_matches(self, league_service):
        mock_match = Mock(spec=Match)
        mock_match.matchID = "new_match"
        
        league_service.SummonerMatchAPI.getMatchesFromList = AsyncMock(return_value=[mock_match])
        league_service.updateMissingMatchesData = Mock()
        
        await league_service.populateMissingMatches(["new_match", "existing_match"])
        
        league_service.updateMissingMatchesData.assert_called_once_with([mock_match])
    
    @pytest.mark.asyncio
    async def test_populate_missing_matches_all_cached(self, league_service):
        mock_match = Mock(spec=Match)
        league_service.matchCache = {"cached_match": mock_match}
        league_service.SummonerMatchAPI.getMatchesFromList = AsyncMock()
        league_service.updateMissingMatchesData = Mock()
        
        await league_service.populateMissingMatches(["cached_match"])
        
        league_service.SummonerMatchAPI.getMatchesFromList.assert_called_once_with([])


class TestGetUserStatus:
    """Test getUserStatus method"""
    
    @pytest.mark.asyncio
    async def test_get_user_status_not_registered(self, league_service):
        result = await league_service.getUserStatus("unknown_user")
        
        assert result == "Not Registered"
    
    @pytest.mark.asyncio
    async def test_get_user_status_registered(self, league_service):
        mock_match = Mock(spec=Match)
        mock_result = Mock(spec=SummonerStatSummaryResults)
        
        league_service.userToSummonerPUUID = {"user1": "puuid1"}
        league_service.UserSummonerAPI.getMatchesFromSummoner = AsyncMock(
            return_value=["match1"]
        )
        league_service.populateMissingMatches = AsyncMock()
        league_service.getListOfMatches = Mock(return_value=[mock_match])
        league_service.SummonerStat.ListOfMatchesToSummonerStat = Mock(return_value=mock_result)
        
        with patch('Services.LeagueServices.league.format', return_value="formatted_result"):
            result = await league_service.getUserStatus("user1")
        
        league_service.UserSummonerAPI.getMatchesFromSummoner.assert_called_once_with("puuid1")
        league_service.populateMissingMatches.assert_called_once_with(["match1"])
        league_service.getListOfMatches.assert_called_once_with(["match1"])
        league_service.SummonerStat.ListOfMatchesToSummonerStat.assert_called_once_with(
            [mock_match], "puuid1"
        )

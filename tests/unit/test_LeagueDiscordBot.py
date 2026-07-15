import sys
import types
import asyncio
import importlib
import pytest
from unittest.mock import AsyncMock, Mock


# Create fake modules/classes for imports used by CoreDiscordBot
fake_league_module = types.ModuleType("Services.LeagueServices.league")
class FakeLeague:
    def __init__(self, key, db):
        self.key = key
        self.db = db
fake_league_module.league = FakeLeague

fake_db_module = types.ModuleType("DataAccess.LeagueDatabase")
class FakeDB:
    def __init__(self, path, file):
        self.path = path
        self.file = file
fake_db_module.LeagueDatabase = FakeDB

fake_dnd_module = types.ModuleType("Services.DnDServices.DnDService")
class FakeDnD:
    def __init__(self):
        self.started = True
fake_dnd_module.DnD = FakeDnD

sys.modules['Services.LeagueServices.league'] = fake_league_module
sys.modules['DataAccess.LeagueDatabase'] = fake_db_module
sys.modules['Services.DnDServices.DnDService'] = fake_dnd_module


@pytest.fixture(autouse=True)
def env(monkeypatch, tmp_path, tmp_path_factory):
    # Set minimal environment variables expected by the bot
    monkeypatch.setenv('DISCORD_BOT_TOKEN', 'dummy_token')
    monkeypatch.setenv('RIOT_API_KEY', 'riot_key')
    monkeypatch.setenv('BOT_STATUS', 'testing')
    monkeypatch.setenv('SQLITE3_PATH', str(tmp_path))
    monkeypatch.setenv('SQLITE3_DB_FILE', 'test.db')
    yield


def test_init_sets_services_and_keys():
    # import after injecting fake modules
    from CoreDiscordBot import CoreDiscordBot

    bot = CoreDiscordBot()

    assert bot.DISCORD_BOT_TOKEN == 'dummy_token'
    assert bot.RIOT_API_KEY == 'riot_key'
    assert bot.BOT_STATUS == 'testing'
    assert isinstance(bot.db, FakeDB)
    assert isinstance(bot.LeagueService, FakeLeague)
    assert isinstance(bot.DnDService, FakeDnD)


@pytest.mark.asyncio
async def test_on_ready_calls_load_extensions(monkeypatch):
    from CoreDiscordBot import CoreDiscordBot
    bot = CoreDiscordBot()

    mock_load = AsyncMock()
    monkeypatch.setattr(bot, 'load_extensions', mock_load)
    monkeypatch.setattr(bot, 'change_presence', AsyncMock())
    monkeypatch.setattr(bot.refreshEventForumThreads, 'start', Mock())
    
    await bot.on_ready()
    mock_load.assert_called_once()
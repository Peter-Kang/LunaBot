import pytest
from unittest.mock import Mock, AsyncMock

from CogCommands.LeagueCogCommands import LeagueCogCommands


class DummyUser:
    def __init__(self, id):
        self.id = id


class DummyResponse:
    def __init__(self):
        self.send_message = AsyncMock()


class DummyInteraction:
    def __init__(self, user_id):
        self.user = DummyUser(user_id)
        self.response = DummyResponse()

@pytest.mark.asyncio
async def test_register_no_riot_id_sends_prompt():
    bot = Mock()
    bot.LeagueService = Mock()
    cog = LeagueCogCommands(bot)

    interaction = DummyInteraction(user_id=123)
    
    await cog.registerSummoner.callback(cog, interaction, riot=None)

    interaction.response.send_message.assert_awaited_once_with("Please enter a Riot ID.")


@pytest.mark.asyncio
async def test_register_invalid_riot_shows_error():
    bot = Mock()
    league_service = Mock()
    # register returns empty string on failure
    league_service.register = Mock(return_value="")
    bot.LeagueService = league_service
    cog = LeagueCogCommands(bot)

    interaction = DummyInteraction(user_id=456)

    await cog.registerSummoner.callback(cog, interaction, riot="Bad#ID")

    expected = "Couldn't add the Riot ID: Bad#ID \nPlease check use a Riot id ie Petechan#NA1"
    interaction.response.send_message.assert_awaited_once_with(expected)


@pytest.mark.asyncio
async def test_register_valid_riot_reports_registered():
    bot = Mock()
    league_service = Mock()
    # register returns non-empty string on success
    league_service.register = Mock(return_value="somepuuid")
    bot.LeagueService = league_service
    cog = LeagueCogCommands(bot)

    interaction = DummyInteraction(user_id=789)

    await cog.registerSummoner.callback(cog, interaction, riot="Good#ID")

    interaction.response.send_message.assert_awaited_once_with("Registered")

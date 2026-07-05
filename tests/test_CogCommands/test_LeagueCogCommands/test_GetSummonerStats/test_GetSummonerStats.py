import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
import discord
from CogCommands.LeagueCogCommands import LeagueCogCommands


@pytest.fixture
def mock_bot():
    """Create a mock bot with LeagueService"""
    bot = MagicMock(spec=commands.Bot)
    bot.LeagueService = MagicMock()
    bot.LeagueService.userToSummonerPUUID = {}
    bot.LeagueService.getUserStatus = AsyncMock()
    return bot


@pytest.fixture
def league_cog(mock_bot):
    """Create a LeagueCogCommands instance with mock bot"""
    cog = LeagueCogCommands(mock_bot)
    return cog


@pytest.fixture
def mock_interaction():
    """Create a mock interaction"""
    interaction = MagicMock(spec=discord.Interaction)
    interaction.user = MagicMock()
    interaction.user.id = 12345
    interaction.response = AsyncMock()
    interaction.followup = AsyncMock()
    return interaction


@pytest.mark.asyncio
async def test_stats_user_not_registered(league_cog, mock_interaction):
    """Test stats command when user is not registered"""
    league_cog.bot.LeagueService.userToSummonerPUUID = {}
    
    await league_cog.stats.callback(league_cog, mock_interaction)
    
    mock_interaction.response.send_message.assert_called_once_with("You are not registered")


@pytest.mark.asyncio
async def test_stats_user_registered(league_cog, mock_interaction):
    """Test stats command when user is registered"""
    user_id = "12345"
    league_cog.bot.LeagueService.userToSummonerPUUID = {user_id: "some_puuid"}
    league_cog.bot.LeagueService.getUserStatus.return_value = "User stats here"
    
    await league_cog.stats.callback(league_cog, mock_interaction)
    
    mock_interaction.response.defer.assert_called_once()
    league_cog.bot.LeagueService.getUserStatus.assert_called_once_with(user_id)
    mock_interaction.followup.send.assert_called_once_with("User stats here")


@pytest.mark.asyncio
async def test_stats_user_id_conversion(league_cog, mock_interaction):
    """Test that user ID is correctly converted to string"""
    user_id = "12345"
    league_cog.bot.LeagueService.userToSummonerPUUID = {user_id: "some_puuid"}
    league_cog.bot.LeagueService.getUserStatus.return_value = "Status"
    
    await league_cog.stats.callback(league_cog, mock_interaction)
    
    league_cog.bot.LeagueService.getUserStatus.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_stats_deferred_response_flow(league_cog, mock_interaction):
    """Test that response is deferred before sending followup"""
    user_id = "12345"
    league_cog.bot.LeagueService.userToSummonerPUUID = {user_id: "some_puuid"}
    league_cog.bot.LeagueService.getUserStatus.return_value = "Test stats"
    
    call_order = []
    mock_interaction.response.defer.side_effect = lambda: call_order.append("defer")
    mock_interaction.followup.send.side_effect = lambda msg: call_order.append("followup")
    
    await league_cog.stats.callback(league_cog, mock_interaction)
    
    assert call_order == ["defer", "followup"]

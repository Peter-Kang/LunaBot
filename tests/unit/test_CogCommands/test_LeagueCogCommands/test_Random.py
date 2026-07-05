import pytest
import discord
from discord.ext import commands
from unittest.mock import AsyncMock, MagicMock, patch
from discord import Embed


@pytest.fixture
def bot_mock():
    bot = MagicMock(spec=commands.Bot)
    bot.LeagueService = MagicMock()
    return bot


@pytest.fixture
def interaction_mock():
    interaction = MagicMock(spec=discord.Interaction)
    interaction.response = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 12345
    return interaction


@pytest.mark.asyncio
async def test_random_command_sends_embed(bot_mock, interaction_mock):
    """Test that the random command calls randomChampion and sends the result."""
    from src.CogCommands.LeagueCogCommands import LeagueCogCommands
    
    # Arrange
    test_embed = Embed(title="Test Champion")
    bot_mock.LeagueService.randomChampion.return_value = test_embed
    
    cog = LeagueCogCommands(bot_mock)
    
    # Act
    await cog.random.callback(cog, interaction_mock)
    
    # Assert
    bot_mock.LeagueService.randomChampion.assert_called_once()
    interaction_mock.response.send_message.assert_called_once_with(embed=test_embed)


@pytest.mark.asyncio
async def test_random_command_calls_service(bot_mock, interaction_mock):
    """Test that the random command calls LeagueService.randomChampion."""
    from src.CogCommands.LeagueCogCommands import LeagueCogCommands
    
    # Arrange
    test_embed = Embed(title="Random Champion")
    bot_mock.LeagueService.randomChampion.return_value = test_embed
    
    cog = LeagueCogCommands(bot_mock)
    
    # Act
    await cog.random.callback(cog, interaction_mock)
    
    # Assert
    bot_mock.LeagueService.randomChampion.assert_called_once()


@pytest.mark.asyncio
async def test_random_command_with_callback_verification(bot_mock, interaction_mock):
    """Test random command with callback to verify embed was sent."""
    from src.CogCommands.LeagueCogCommands import LeagueCogCommands
    
    # Arrange
    test_embed = Embed(title="Champion", description="Test Description")
    bot_mock.LeagueService.randomChampion.return_value = test_embed
    
    verification_results = {"embed_received": False}
    
    def verify_callback(result):
        verification_results["embed_received"] = isinstance(result, Embed)
        verification_results["title"] = result.title
    
    cog = LeagueCogCommands(bot_mock)
    
    # Act
    await cog.random.callback(cog, interaction_mock)
    sent_embed = interaction_mock.response.send_message.call_args[1]["embed"]
    verify_callback(sent_embed)
    
    # Assert
    assert verification_results["embed_received"] is True
    assert verification_results["title"] == "Champion"

import pytest
from unittest.mock import AsyncMock, MagicMock, Mock

from src.CogCommands.DnDCogCommands import DnDCogCommands


class DummyInteraction:
    def __init__(self):
        self.response = MagicMock()
        self.response.send_message = AsyncMock()


class DummyBot():
    def __init__(self, roll_result: str):
        self.DnDService = MagicMock()
        # service.roll is awaited in the cog, so make it an AsyncMock
        self.DnDService.roll = AsyncMock(return_value=roll_result)


@pytest.mark.asyncio
async def test_roll_calls_service_roll_and_sends_message():
    dice_expression = "2d8+3"
    expected_result = "2d8+3 => 12"
    bot = Mock()
    bot.DnDService = Mock()
    bot.DnDService.roll = Mock(return_value=expected_result)

    cog = DnDCogCommands(bot)
    interaction = DummyInteraction()

    await cog.roll.callback(cog, interaction, dice_expression)

    bot.DnDService.roll.assert_called_once_with(dice_expression)
    interaction.response.send_message.assert_awaited_once_with(expected_result)
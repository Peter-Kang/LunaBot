import pytest
import discord
from unittest.mock import AsyncMock, Mock

from src.CogCommands.DnDCogCommands import DnDCogCommands
from Services.DnDServices.Monsters.DnDMonsters import DnDEnvironments


class DummyResponse:
    def __init__(self):
        self.sent = None

    async def send_message(self, *args, **kwargs):
        self.sent = (args, kwargs)


class DummyInteraction:
    def __init__(self):
        self.response = DummyResponse()


class DummyBot:
    def __init__(self):
        self.DnDService = Mock()


@pytest.mark.asyncio
async def test_encounter_calls_service_and_sends_embed_default():
    bot = DummyBot()
    # Prepare a fake embed to be returned
    fake_embed = discord.Embed(title="Encounter")
    bot.DnDService.Encounter.return_value = fake_embed

    cog = DnDCogCommands(bot=bot)
    interaction = DummyInteraction()

    await cog.encounter.callback(cog,interaction)

    bot.DnDService.Encounter.assert_called_once_with(-1.0, DnDEnvironments.All)
    assert interaction.response.sent is not None
    # ensure embed passed as keyword
    args, kwargs = interaction.response.sent
    assert kwargs.get("embed") is fake_embed


@pytest.mark.asyncio
async def test_encounter_with_parameters():
    bot = DummyBot()
    fake_embed = discord.Embed(title="Custom")
    bot.DnDService.Encounter.return_value = fake_embed

    cog = DnDCogCommands(bot=bot)
    interaction = DummyInteraction()

    await cog.encounter.callback(cog, interaction, challenge=2.5, environment=DnDEnvironments.Forest)

    bot.DnDService.Encounter.assert_called_once_with(2.5, DnDEnvironments.Forest)
    args, kwargs = interaction.response.sent
    assert kwargs.get("embed") is fake_embed


def test_get_environment_choices_filters_by_enum_value():
    bot = DummyBot()
    cog = DnDCogCommands(bot=bot)

    choices = cog.getEnvironmentChoices()

    expected_envs = [env for env in DnDEnvironments if int(env.value) < 24]
    assert len(choices) == len(expected_envs)
    for choice, env in zip(choices, expected_envs):
        assert choice.name == env.name
        assert choice.value == env


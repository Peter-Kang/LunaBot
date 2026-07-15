import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
import discord
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
sys.path.insert(0, os.path.join(ROOT, "src"))

from CogCommands.EventCogCommands import EventCogCommands


class DummyForumChannel:
    pass


class DummyAsyncIterator:
    def __init__(self, items):
        self._items = iter(items)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._items)
        except StopIteration:
            raise StopAsyncIteration


@pytest.mark.asyncio
async def test_cog_load_starts_refresh_event_forum_threads():
    bot = MagicMock()
    cog = EventCogCommands(bot)
    cog.refreshEventForumThreads.start = MagicMock()

    await cog.cog_load()

    cog.refreshEventForumThreads.start.assert_called_once()


@pytest.mark.asyncio
async def test_cog_unload_cancels_refresh_event_forum_threads():
    bot = MagicMock()
    cog = EventCogCommands(bot)
    cog.refreshEventForumThreads.cancel = MagicMock()

    await cog.cog_unload()

    cog.refreshEventForumThreads.cancel.assert_called_once()


@pytest.mark.asyncio
async def test_on_scheduled_event_create_creates_thread_for_new_event():
    bot = MagicMock()
    event = MagicMock()
    event.guild = MagicMock(id=123)
    event.name = "Test Event"
    event.url = "https://example.com/test-event"
    event.cover_image = MagicMock(url="https://example.com/image.png")

    forum_channel = DummyForumChannel()
    forum_channel.threads = []
    forum_channel.create_thread = AsyncMock()

    bot.get_guild.return_value = MagicMock(channels=[forum_channel])

    with patch("CogCommands.EventCogCommands.discord.utils.get", return_value=forum_channel), \
         patch("CogCommands.EventCogCommands.discord.ForumChannel", DummyForumChannel), \
         patch("CogCommands.EventCogCommands.discord.Embed", return_value=discord.Embed()):
        cog = EventCogCommands(bot)
        await cog.on_scheduled_event_create(event)

    forum_channel.create_thread.assert_awaited_once()
    _, kwargs = forum_channel.create_thread.call_args
    assert kwargs["name"] == "Test Event"
    assert kwargs["content"] == "https://example.com/test-event"
    assert kwargs["embed"].image.url == "https://example.com/image.png"


@pytest.mark.asyncio
async def test_on_scheduled_event_create_skips_existing_thread_name():
    bot = MagicMock()
    event = MagicMock()
    event.guild = MagicMock(id=123)
    event.name = "Existing Event"
    event.url = "https://example.com/existing-event"
    event.cover_image = None

    existing_thread = MagicMock(archived=False, locked=False, name="Existing Event")
    existing_thread.history = AsyncMock(return_value=DummyAsyncIterator([]))

    forum_channel = DummyForumChannel()
    forum_channel.threads = [existing_thread]
    forum_channel.create_thread = AsyncMock()

    bot.get_guild.return_value = MagicMock(channels=[forum_channel])

    with patch("CogCommands.EventCogCommands.discord.utils.get", return_value=forum_channel), \
         patch("CogCommands.EventCogCommands.discord.ForumChannel", DummyForumChannel):
        cog = EventCogCommands(bot)
        await cog.on_scheduled_event_create(event)

    forum_channel.create_thread.assert_awaited_once()


@pytest.mark.asyncio
async def test_on_scheduled_event_update_archives_thread_when_event_ends():
    bot = MagicMock()
    before = MagicMock(id=123, guild=MagicMock(id=456))
    after = MagicMock(status="completed")

    matching_message = MagicMock(content="Event ID 123")
    thread = MagicMock(archived=False, locked=False, name="Matching Thread")
    thread.history = MagicMock(return_value=DummyAsyncIterator([matching_message]))
    thread.edit = AsyncMock()

    forum_channel = DummyForumChannel()
    forum_channel.threads = [thread]

    bot.get_guild.return_value = MagicMock(channels=[forum_channel])

    mock_event_status = MagicMock(completed="completed", ended="ended")
    with patch("CogCommands.EventCogCommands.discord.utils.get", return_value=forum_channel), \
         patch("CogCommands.EventCogCommands.discord.ForumChannel", DummyForumChannel), \
         patch("CogCommands.EventCogCommands.discord.EventStatus", mock_event_status):
        cog = EventCogCommands(bot)
        await cog.on_scheduled_event_update(before, after)

    thread.edit.assert_awaited_once()
    assert thread.edit.call_args.kwargs["archived"] is True


@pytest.mark.asyncio
async def test_on_scheduled_event_user_add_adds_user_to_matching_thread():
    bot = MagicMock()
    event = MagicMock(id=123, guild=MagicMock(id=456))
    user = MagicMock()

    matching_message = MagicMock(content="Join 123")
    thread = MagicMock(archived=False, locked=False)
    thread.history = MagicMock(return_value=DummyAsyncIterator([matching_message]))
    thread.add_user = AsyncMock()

    forum_channel = DummyForumChannel()
    forum_channel.threads = [thread]

    bot.get_guild.return_value = MagicMock(channels=[forum_channel])

    with patch("CogCommands.EventCogCommands.discord.utils.get", return_value=forum_channel), \
         patch("CogCommands.EventCogCommands.discord.ForumChannel", DummyForumChannel):
        cog = EventCogCommands(bot)
        await cog.on_scheduled_event_user_add(event, user)

    thread.add_user.assert_awaited_once_with(user)

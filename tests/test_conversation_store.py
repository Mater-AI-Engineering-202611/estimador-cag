from uuid import UUID

import pytest

from app.services.conversation_manager import ConversationManager
from app.services.conversation_store import ConversationStore


def test_create_conversation():
    store = ConversationStore()

    conversation_id = store.create()

    assert store.exists(conversation_id)
    assert isinstance(
        store.get(conversation_id),
        ConversationManager,
    )


def test_conversation_id_is_valid_uuid():
    store = ConversationStore()

    conversation_id = store.create()

    assert UUID(conversation_id).version == 4


def test_conversation_ids_are_unique():
    store = ConversationStore()

    first_id = store.create()
    second_id = store.create()

    assert first_id != second_id


def test_get_existing_conversation():
    store = ConversationStore()

    conversation_id = store.create()

    first_reference = store.get(conversation_id)
    second_reference = store.get(conversation_id)

    assert first_reference is second_reference


def test_conversation_does_not_exist():
    store = ConversationStore()

    assert not store.exists("invalid-id")


def test_get_nonexistent_conversation():
    store = ConversationStore()

    with pytest.raises(KeyError):
        store.get("invalid-id")


def test_conversations_are_isolated():
    store = ConversationStore()

    first_id = store.create()
    second_id = store.create()

    first = store.get(first_id)
    second = store.get(second_id)

    first.add_user_message("Estima un CRM")
    first.add_assistant_message("400 horas")

    second.add_user_message("Estima un inventario")
    second.add_assistant_message("150 horas")

    assert first.get_messages() == [
        {"role": "user", "content": "Estima un CRM"},
        {"role": "assistant", "content": "400 horas"},
    ]

    assert second.get_messages() == [
        {"role": "user", "content": "Estima un inventario"},
        {"role": "assistant", "content": "150 horas"},
    ]
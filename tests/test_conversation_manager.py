import pytest

from app.services.conversation_manager import ConversationManager


def test_conversation_starts_empty():
    conversation = ConversationManager()

    assert conversation.get_messages() == []


def test_add_user_message():
    conversation = ConversationManager()

    conversation.add_user_message("Estima un CRM")

    assert conversation.get_messages() == [
        {
            "role": "user",
            "content": "Estima un CRM",
        }
    ]


def test_add_assistant_message():
    conversation = ConversationManager()

    conversation.add_assistant_message("400 horas")

    assert conversation.get_messages() == [
        {
            "role": "assistant",
            "content": "400 horas",
        }
    ]


def test_get_messages_returns_copy():
    conversation = ConversationManager()
    conversation.add_user_message("Estima un CRM")

    messages = conversation.get_messages()
    messages.clear()

    assert len(conversation.get_messages()) == 1


def test_sliding_window_returns_last_turn():
    conversation = ConversationManager()

    conversation.add_user_message("Estima un CRM")
    conversation.add_assistant_message("400 horas")

    conversation.add_user_message("Añade testing")
    conversation.add_assistant_message("450 horas")

    assert conversation.get_messages_windowed(max_turns=1) == [
        {
            "role": "user",
            "content": "Añade testing",
        },
        {
            "role": "assistant",
            "content": "450 horas",
        },
    ]

    assert len(conversation.get_messages()) == 4


def test_sliding_window_larger_than_history():
    conversation = ConversationManager()

    conversation.add_user_message("Estima un CRM")
    conversation.add_assistant_message("400 horas")

    assert conversation.get_messages_windowed(
        max_turns=10
    ) == conversation.get_messages()


def test_sliding_window_zero_turns():
    conversation = ConversationManager()
    conversation.add_user_message("Estima un CRM")
    conversation.add_assistant_message("400 horas")

    assert conversation.get_messages_windowed(max_turns=0) == []


def test_sliding_window_negative_turns():
    conversation = ConversationManager()

    with pytest.raises(ValueError):
        conversation.get_messages_windowed(max_turns=-1)
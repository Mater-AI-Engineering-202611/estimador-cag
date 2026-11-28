class ConversationManager:
    """Gestiona el historial de una conversación."""

    def __init__(self):
        self.messages: list[dict[str, str]] = []

    def add_user_message(self, content: str) -> None:
        self.messages.append({
            "role": "user",
            "content": content,
        })

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({
            "role": "assistant",
            "content": content,
        })

    def get_messages(self) -> list[dict[str, str]]:
        return self.messages.copy()

    def get_messages_windowed(
        self, max_turns: int = 10
    ) -> list[dict[str, str]]:
        """Devuelve los últimos N turnos completos."""

        if max_turns < 0:
            raise ValueError("max_turns no puede ser negativo")

        if max_turns == 0:
            return []

        return self.messages[-(max_turns * 2):]
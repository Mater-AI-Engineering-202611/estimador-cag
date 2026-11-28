from uuid import uuid4

from app.services.conversation_manager import ConversationManager


class ConversationStore:
    """Gestiona las conversaciones almacenadas en memoria."""

    def __init__(self):
        self.conversations: dict[str, ConversationManager] = {}

    def create(self) -> str:
        """Crea una nueva conversación y devuelve su identificador."""

        conversation_id = str(uuid4())

        self.conversations[conversation_id] = ConversationManager()

        return conversation_id

    def get(self, conversation_id: str) -> ConversationManager:
        """Recupera una conversación existente."""

        return self.conversations[conversation_id]

    def exists(self, conversation_id: str) -> bool:
        """Comprueba si existe una conversación."""

        return conversation_id in self.conversations


conversation_store = ConversationStore()
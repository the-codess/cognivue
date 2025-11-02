"""
Conversational Interface Module
Natural language interaction with insights
"""
from src.modules.conversational_interface.models import (
    QueryIntent,
    ConversationTurn,
    ConversationContext,
    QueryResponse,
    IntentClassification
)
from src.modules.conversational_interface.query_processor import QueryProcessor
from src.modules.conversational_interface.manager import ConversationManager

__all__ = [
    'QueryIntent',
    'ConversationTurn',
    'ConversationContext',
    'QueryResponse',
    'IntentClassification',
    'QueryProcessor',
    'ConversationManager'
]
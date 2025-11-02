"""
Conversation Manager
Manages conversation state and context with hybrid LLM + pattern matching
"""
import uuid
from datetime import datetime
from typing import Optional

from src.modules.conversational_interface.models import (
    ConversationContext, ConversationTurn, QueryResponse
)
from src.modules.conversational_interface.query_processor import QueryProcessor
from src.modules.conversational_interface.llm_handler import LLMQueryHandler
from src.modules.insight_generation.models import InsightCollection
from src.utils.logger import app_logger as logger

class ConversationManager:
    """Manage conversational interactions with hybrid LLM + pattern matching"""
    
    def __init__(self, use_llm: bool = True):
        self.query_processor = QueryProcessor()
        self.llm_handler = LLMQueryHandler() if use_llm else None
        self.active_sessions = {}
        self.use_llm = use_llm and (self.llm_handler.available if self.llm_handler else False)
        
        if self.use_llm:
            logger.info("ConversationManager initialized with LLM support")
        else:
            logger.info("ConversationManager initialized with pattern matching only")
    
    def create_session(self, user_role: Optional[str] = None) -> str:
        """Create a new conversation session"""
        
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        context = ConversationContext(
            session_id=session_id,
            user_role=user_role
        )
        
        self.active_sessions[session_id] = context
        
        logger.info(f"Created conversation session: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ConversationContext]:
        """Get conversation session"""
        return self.active_sessions.get(session_id)
    
    def process_message(
        self,
        session_id: str,
        user_message: str,
        insights_collection: Optional[InsightCollection] = None
    ) -> QueryResponse:
        """Process user message and generate response using hybrid approach"""
        
        # Get or create session
        context = self.active_sessions.get(session_id)
        if not context:
            session_id = self.create_session()
            context = self.active_sessions[session_id]
        
        # Try LLM first if available
        response = None
        if self.use_llm and self.llm_handler:
            try:
                history = self.get_conversation_history(session_id)
                response = self.llm_handler.process_query_with_llm(
                    user_message,
                    insights_collection,
                    history
                )
                if response:
                    logger.info("Used LLM for query processing")
            except Exception as e:
                logger.warning(f"LLM processing failed, falling back to pattern matching: {str(e)}")
        
        # Fallback to pattern matching
        if not response:
            response = self.query_processor.process_query(user_message, insights_collection)
            logger.info("Used pattern matching for query processing")
        
        # Create conversation turn
        turn = ConversationTurn(
            turn_id=f"turn_{uuid.uuid4().hex[:8]}",
            user_query=user_message,
            query_intent=response.intent,
            assistant_response=response.response_text,
            referenced_insights=response.insights_referenced,
            confidence=response.confidence
        )
        
        # Update context
        context.turns.append(turn)
        context.last_activity = datetime.now()
        
        if insights_collection:
            context.active_insights = [i.insight_id for i in insights_collection.insights[:5]]
        
        logger.info(f"Processed message in session {session_id}: intent={response.intent.value}")
        
        return response
    
    def get_conversation_history(self, session_id: str) -> list:
        """Get conversation history"""
        
        context = self.active_sessions.get(session_id)
        if not context:
            return []
        
        history = []
        for turn in context.turns:
            history.append({
                "user": turn.user_query,
                "assistant": turn.assistant_response,
                "intent": turn.query_intent.value if turn.query_intent else "unknown",
                "timestamp": turn.timestamp.isoformat()
            })
        
        return history
    
    def clear_session(self, session_id: str):
        """Clear a conversation session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logger.info(f"Cleared session: {session_id}")
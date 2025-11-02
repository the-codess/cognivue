"""
Conversational Interface Models
Defines conversation structures and query types
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class QueryIntent(str, Enum):
    """Types of user query intents"""
    CLARIFICATION = "clarification"  # Ask about an insight
    DRILL_DOWN = "drill_down"  # Get more details
    COMPARISON = "comparison"  # Compare entities/time periods
    SUMMARY = "summary"  # Get overview
    RECOMMENDATION = "recommendation"  # Ask for recommendations
    WHAT_IF = "what_if"  # Scenario analysis
    VISUALIZATION = "visualization"  # Change visualization type
    DATA_QUERY = "data_query"  # Query raw data
    GENERAL = "general"  # General question

class ConversationTurn(BaseModel):
    """Single turn in a conversation"""
    turn_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # User input
    user_query: str
    query_intent: Optional[QueryIntent] = None
    entities: List[str] = []  # Extracted entities (dates, metrics, etc.)
    
    # System response
    assistant_response: str
    response_type: str = "text"  # text, chart, table, etc.
    
    # Context
    referenced_insights: List[str] = []  # Insight IDs referenced
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)

class ConversationContext(BaseModel):
    """Context maintained across conversation"""
    session_id: str
    started_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    
    # User context
    user_role: Optional[str] = None
    
    # Conversation history
    turns: List[ConversationTurn] = []
    
    # Active context
    active_insights: List[str] = []  # Currently discussed insights
    active_data_sources: List[str] = []
    last_visualization: Optional[str] = None
    
    # State
    conversation_summary: str = ""

class QueryResponse(BaseModel):
    """Response to a user query"""
    response_text: str
    intent: QueryIntent
    confidence: float = Field(ge=0.0, le=1.0)
    
    # Supporting data
    insights_referenced: List[str] = []
    data_points: Optional[Dict[str, Any]] = None
    visualizations: List[str] = []
    
    # Follow-up suggestions
    suggested_questions: List[str] = []
    
    # Metadata
    response_time: float = 0.0  # seconds
    sources: List[str] = []

class IntentClassification(BaseModel):
    """Result of intent classification"""
    intent: QueryIntent
    confidence: float = Field(ge=0.0, le=1.0)
    entities: List[str] = []
    keywords: List[str] = []
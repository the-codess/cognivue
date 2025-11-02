"""
LLM Query Handler
Uses Ollama for natural language processing
"""
import json
from typing import Optional, Dict, Any
import ollama

from src.modules.conversational_interface.models import QueryResponse, QueryIntent
from src.modules.insight_generation.models import InsightCollection
from src.utils.logger import app_logger as logger
from src.config.settings import settings

class LLMQueryHandler:
    """Handle queries using local LLM via Ollama"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.LLM_MODEL
        self.available = self._check_ollama_available()
        
        if self.available:
            logger.info(f"LLMQueryHandler initialized with model: {self.model_name}")
        else:
            logger.warning("Ollama not available, will use fallback pattern matching")
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            # Try to list models
            response = ollama.list()
            
            # Check if our model is available
            available_models = [model['name'] for model in response.get('models', [])]
            
            if not available_models:
                logger.warning("No Ollama models found. Please run: ollama pull llama2")
                return False
            
            # Check if specified model exists
            model_available = any(self.model_name in model for model in available_models)
            
            if not model_available:
                logger.warning(f"Model {self.model_name} not found. Available: {available_models}")
                # Try to use first available model
                if available_models:
                    self.model_name = available_models[0].split(':')[0]
                    logger.info(f"Using available model: {self.model_name}")
                    return True
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"Ollama check failed: {str(e)}")
            return False
    
    def process_query_with_llm(
        self,
        query: str,
        insights_collection: Optional[InsightCollection] = None,
        conversation_history: list = None
    ) -> QueryResponse:
        """Process query using LLM"""
        
        if not self.available:
            logger.warning("LLM not available, cannot process query")
            return None
        
        try:
            # Build context from insights
            context = self._build_context(insights_collection)
            
            # Build conversation history
            history_text = self._build_history(conversation_history)
            
            # Create prompt
            prompt = self._create_prompt(query, context, history_text)
            
            # Call LLM
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': settings.LLM_TEMPERATURE,
                    'num_predict': settings.LLM_MAX_TOKENS
                }
            )
            
            response_text = response['response'].strip()
            
            # Parse response to extract intent
            intent = self._extract_intent(query, response_text)
            
            # Extract referenced insights
            referenced_insights = self._extract_referenced_insights(
                response_text, insights_collection
            )
            
            # Generate suggestions
            suggestions = self._generate_suggestions(query, intent)
            
            query_response = QueryResponse(
                response_text=response_text,
                intent=intent,
                confidence=0.85,
                insights_referenced=referenced_insights,
                suggested_questions=suggestions,
                sources=["llm_generated"]
            )
            
            logger.info(f"LLM processed query successfully: intent={intent.value}")
            return query_response
            
        except Exception as e:
            logger.error(f"Error processing query with LLM: {str(e)}")
            return None
    
    def _build_context(self, insights_collection: Optional[InsightCollection]) -> str:
        """Build context from insights"""
        
        if not insights_collection or insights_collection.total_count == 0:
            return "No insights are currently available."
        
        context = f"Available Insights ({insights_collection.total_count} total):\n\n"
        
        for i, insight in enumerate(insights_collection.insights[:5], 1):
            context += f"{i}. {insight.title}\n"
            context += f"   Type: {insight.insight_type.value}\n"
            context += f"   Severity: {insight.severity.value}\n"
            context += f"   Description: {insight.description}\n"
            context += f"   Narrative: {insight.narrative}\n"
            
            if insight.recommendations:
                context += f"   Recommendations: {', '.join(insight.recommendations[:2])}\n"
            
            context += "\n"
        
        return context
    
    def _build_history(self, conversation_history: Optional[list]) -> str:
        """Build conversation history text"""
        
        if not conversation_history:
            return ""
        
        history_text = "Recent conversation:\n"
        for turn in conversation_history[-3:]:  # Last 3 turns
            history_text += f"User: {turn.get('user', '')}\n"
            history_text += f"Assistant: {turn.get('assistant', '')}\n\n"
        
        return history_text
    
    def _create_prompt(self, query: str, context: str, history: str) -> str:
        """Create prompt for LLM"""
        
        prompt = f"""You are an intelligent data analysis assistant helping users understand business insights. 

{context}

{history}

User Question: {query}

Instructions:
1. Answer the user's question clearly and concisely
2. Reference specific insights from the context when relevant
3. If asked for recommendations, provide actionable advice
4. If asked for explanations, provide clear reasoning
5. Keep responses focused and professional
6. If you don't have enough information, say so
7. Do not make up data or insights not in the context

Your response:"""
        
        return prompt
    
    def _extract_intent(self, query: str, response: str) -> QueryIntent:
        """Extract intent from query and response"""
        
        query_lower = query.lower()
        
        # Simple keyword matching for intent
        if any(word in query_lower for word in ['summary', 'overview', 'main', 'key']):
            return QueryIntent.SUMMARY
        elif any(word in query_lower for word in ['why', 'how', 'explain', 'what is']):
            return QueryIntent.CLARIFICATION
        elif any(word in query_lower for word in ['compare', 'vs', 'versus', 'difference']):
            return QueryIntent.COMPARISON
        elif any(word in query_lower for word in ['detail', 'more', 'breakdown']):
            return QueryIntent.DRILL_DOWN
        elif any(word in query_lower for word in ['recommend', 'should', 'what do', 'action']):
            return QueryIntent.RECOMMENDATION
        elif any(word in query_lower for word in ['what if', 'scenario', 'predict']):
            return QueryIntent.WHAT_IF
        else:
            return QueryIntent.GENERAL
    
    def _extract_referenced_insights(
        self, response: str, insights_collection: Optional[InsightCollection]
    ) -> list:
        """Extract which insights were referenced in response"""
        
        if not insights_collection:
            return []
        
        referenced = []
        
        # Simple approach: check if insight titles appear in response
        for insight in insights_collection.insights[:5]:
            # Check for title keywords in response
            title_words = insight.title.lower().split()
            if any(word in response.lower() for word in title_words if len(word) > 4):
                referenced.append(insight.insight_id)
        
        return referenced
    
    def _generate_suggestions(self, query: str, intent: QueryIntent) -> list:
        """Generate follow-up question suggestions"""
        
        suggestions = {
            QueryIntent.SUMMARY: [
                "Tell me more about the critical insights",
                "What should I focus on first?",
                "Explain the most important finding"
            ],
            QueryIntent.CLARIFICATION: [
                "What data supports this?",
                "What should we do about it?",
                "Are there any risks?"
            ],
            QueryIntent.COMPARISON: [
                "Why is there a difference?",
                "What caused this gap?",
                "How can we improve?"
            ],
            QueryIntent.DRILL_DOWN: [
                "Show me the underlying data",
                "What are the specific numbers?",
                "Break this down further"
            ],
            QueryIntent.RECOMMENDATION: [
                "What's the expected impact?",
                "How long will this take?",
                "What resources do we need?"
            ]
        }
        
        return suggestions.get(intent, [
            "Tell me more",
            "What else should I know?",
            "Show me a summary"
        ])
    
    def chat(
        self,
        message: str,
        context: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """Simple chat interface for testing"""
        
        if not self.available:
            return "Ollama is not available. Please install and start Ollama."
        
        try:
            prompt = message
            if context:
                prompt = f"Context: {context}\n\nQuestion: {message}"
            
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={'temperature': temperature}
            )
            
            return response['response'].strip()
            
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return f"Error: {str(e)}"
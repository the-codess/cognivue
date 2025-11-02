"""
Query Processor
Processes natural language queries without requiring LLM
Uses pattern matching and keyword extraction
"""
import re
from typing import List, Dict, Optional, Tuple
import uuid

from src.modules.conversational_interface.models import (
    QueryIntent, IntentClassification, QueryResponse
)
from src.modules.insight_generation.models import InsightCollection
from src.utils.logger import app_logger as logger

class QueryProcessor:
    """Process natural language queries using pattern matching"""
    
    def __init__(self):
        self.intent_patterns = self._build_intent_patterns()
        logger.info("QueryProcessor initialized")
    
    def _build_intent_patterns(self) -> Dict[QueryIntent, List[str]]:
        """Build keyword patterns for intent classification"""
        return {
            QueryIntent.CLARIFICATION: [
                r'\bwhy\b', r'\bhow\b', r'\bexplain\b', r'\bwhat (is|does|means?)\b',
                r'\bcan you (explain|clarify)\b', r'\btell me (about|more)\b'
            ],
            QueryIntent.DRILL_DOWN: [
                r'\bmore details?\b', r'\bdetailed\b', r'\bbreakdown\b',
                r'\bshow me (more|details)\b', r'\bwhat about\b', r'\bspecific\b'
            ],
            QueryIntent.COMPARISON: [
                r'\bcompare\b', r'\bvs\.?\b', r'\bversus\b', r'\bdifference\b',
                r'\bbetter\b', r'\bworse\b', r'\bhigher\b', r'\blower\b'
            ],
            QueryIntent.SUMMARY: [
                r'\bsummary\b', r'\boverview\b', r'\bmain\b', r'\bkey\b',
                r'\bhighlights?\b', r'\btop\b', r'\bimportant\b'
            ],
            QueryIntent.RECOMMENDATION: [
                r'\brecommend\b', r'\bsugg', r'\bshould\b', r'\bwhat (can|should) (i|we) do\b',
                r'\badvice\b', r'\bnext steps?\b', r'\baction\b'
            ],
            QueryIntent.WHAT_IF: [
                r'\bwhat if\b', r'\bscenario\b', r'\bif (we|i)\b',
                r'\bpredict\b', r'\bforecast\b', r'\bwould happen\b'
            ],
            QueryIntent.VISUALIZATION: [
                r'\bshow (me )?(a |the )?(chart|graph|plot|table)\b',
                r'\bvisuali[sz]e\b', r'\bdisplay\b', r'\b(bar|line|pie) chart\b'
            ],
            QueryIntent.DATA_QUERY: [
                r'\bwhat (is|are) (the|our)\b', r'\bhow many\b', r'\bhow much\b',
                r'\bdata\b', r'\bnumber\b', r'\bvalue\b', r'\btotal\b'
            ]
        }
    
    def classify_intent(self, query: str) -> IntentClassification:
        """Classify user query intent"""
        
        query_lower = query.lower()
        intent_scores = {}
        
        # Score each intent
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    score += 1
            intent_scores[intent] = score
        
        # Get best match
        if max(intent_scores.values()) > 0:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 3, 1.0)
        else:
            best_intent = QueryIntent.GENERAL
            confidence = 0.5
        
        # Extract entities (numbers, dates, etc.)
        entities = self._extract_entities(query)
        
        # Extract keywords
        keywords = self._extract_keywords(query)
        
        classification = IntentClassification(
            intent=best_intent,
            confidence=confidence,
            entities=entities,
            keywords=keywords
        )
        
        logger.info(f"Classified intent: {best_intent.value} (confidence: {confidence:.2f})")
        return classification
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract entities from query"""
        entities = []
        
        # Extract numbers
        numbers = re.findall(r'\b\d+\.?\d*%?\b', query)
        entities.extend(numbers)
        
        # Extract dates/time periods
        time_patterns = [
            r'\b\d{4}\b',  # Year
            r'\b(Q[1-4])\b',  # Quarter
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b',
            r'\b(last|this|next) (week|month|quarter|year)\b'
        ]
        for pattern in time_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            entities.extend([m if isinstance(m, str) else m[0] for m in matches])
        
        return entities
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords"""
        # Common business keywords
        business_keywords = [
            'revenue', 'sales', 'profit', 'cost', 'expense', 'margin',
            'customer', 'product', 'region', 'growth', 'trend', 'performance',
            'budget', 'forecast', 'target', 'actual', 'variance'
        ]
        
        query_lower = query.lower()
        keywords = [kw for kw in business_keywords if kw in query_lower]
        
        return keywords
    
    def process_query(
        self,
        query: str,
        insights_collection: Optional[InsightCollection] = None
    ) -> QueryResponse:
        """Process a user query and generate response"""
        
        # Classify intent
        classification = self.classify_intent(query)
        
        # Generate response based on intent
        if classification.intent == QueryIntent.SUMMARY:
            response = self._handle_summary(insights_collection)
        elif classification.intent == QueryIntent.CLARIFICATION:
            response = self._handle_clarification(query, insights_collection)
        elif classification.intent == QueryIntent.COMPARISON:
            response = self._handle_comparison(query, insights_collection)
        elif classification.intent == QueryIntent.DRILL_DOWN:
            response = self._handle_drill_down(query, insights_collection)
        elif classification.intent == QueryIntent.RECOMMENDATION:
            response = self._handle_recommendation(insights_collection)
        else:
            response = self._handle_general(query, insights_collection)
        
        return response
    
    def _handle_summary(self, insights_collection: Optional[InsightCollection]) -> QueryResponse:
        """Handle summary request"""
        
        if not insights_collection or insights_collection.total_count == 0:
            response_text = "No insights are currently available. Please process some data first."
            suggested = ["What data sources are available?", "How do I upload data?"]
        else:
            response_text = f"Here's a summary of the analysis:\n\n"
            response_text += f"I've identified {insights_collection.total_count} key insights "
            response_text += f"with an average confidence of {insights_collection.avg_confidence:.1%}.\n\n"
            
            if insights_collection.critical_insights > 0:
                response_text += f"🔴 {insights_collection.critical_insights} critical insights need immediate attention:\n"
                for insight in insights_collection.insights:
                    if insight.severity.value == "critical":
                        response_text += f"  • {insight.title}\n"
                response_text += "\n"
            
            response_text += "Top 3 insights:\n"
            for i, insight in enumerate(insights_collection.insights[:3], 1):
                response_text += f"{i}. {insight.title}\n"
            
            suggested = [
                "Tell me more about the first insight",
                "Why is this happening?",
                "What should we do about it?"
            ]
        
        return QueryResponse(
            response_text=response_text,
            intent=QueryIntent.SUMMARY,
            confidence=0.9,
            insights_referenced=[i.insight_id for i in insights_collection.insights[:3]] if insights_collection else [],
            suggested_questions=suggested
        )
    
    def _handle_clarification(
        self, query: str, insights_collection: Optional[InsightCollection]
    ) -> QueryResponse:
        """Handle clarification questions"""
        
        if not insights_collection or insights_collection.total_count == 0:
            response_text = "I don't have any insights to explain yet. Let's start by analyzing some data."
            suggested = ["Show me a summary", "What data is available?"]
        else:
            # Try to find relevant insight
            query_lower = query.lower()
            relevant_insight = None
            
            for insight in insights_collection.insights:
                if any(word in insight.title.lower() for word in query_lower.split()):
                    relevant_insight = insight
                    break
            
            if relevant_insight:
                response_text = f"Let me explain the insight: '{relevant_insight.title}'\n\n"
                response_text += f"{relevant_insight.narrative}\n\n"
                
                if relevant_insight.explanations:
                    response_text += "Technical details:\n"
                    for exp in relevant_insight.explanations[:2]:
                        response_text += f"• {exp.content}\n"
                
                if relevant_insight.recommendations:
                    response_text += f"\nRecommended actions:\n"
                    for rec in relevant_insight.recommendations[:2]:
                        response_text += f"• {rec}\n"
                
                suggested = [
                    "What data supports this?",
                    "How confident are you?",
                    "What else should I know?"
                ]
            else:
                response_text = "I can explain any of these insights:\n"
                for i, insight in enumerate(insights_collection.insights[:3], 1):
                    response_text += f"{i}. {insight.title}\n"
                suggested = ["Tell me about #1", "Explain the trend", "Show me the details"]
        
        return QueryResponse(
            response_text=response_text,
            intent=QueryIntent.CLARIFICATION,
            confidence=0.8,
            insights_referenced=[relevant_insight.insight_id] if relevant_insight else [],
            suggested_questions=suggested
        )
    
    def _handle_comparison(
        self, query: str, insights_collection: Optional[InsightCollection]
    ) -> QueryResponse:
        """Handle comparison requests"""
        
        if not insights_collection:
            response_text = "I need data to make comparisons. Please provide data first."
            suggested = ["Upload data", "Show me what's available"]
        else:
            # Find comparison insights
            comparison_insights = [
                i for i in insights_collection.insights
                if i.insight_type.value == "comparison"
            ]
            
            if comparison_insights:
                response_text = "Here are the key comparisons I found:\n\n"
                for i, insight in enumerate(comparison_insights[:3], 1):
                    response_text += f"{i}. {insight.title}\n"
                    response_text += f"   {insight.description}\n\n"
                suggested = ["Tell me more about #1", "Why is there a difference?", "What should we do?"]
            else:
                response_text = "I haven't found any direct comparisons yet. "
                response_text += "Would you like me to compare specific metrics or time periods?"
                suggested = ["Compare this quarter to last quarter", "Show regional differences"]
        
        return QueryResponse(
            response_text=response_text,
            intent=QueryIntent.COMPARISON,
            confidence=0.75,
            insights_referenced=[i.insight_id for i in comparison_insights[:3]],
            suggested_questions=suggested
        )
    
    def _handle_drill_down(
        self, query: str, insights_collection: Optional[InsightCollection]
    ) -> QueryResponse:
        """Handle drill-down requests"""
        
        if not insights_collection or insights_collection.total_count == 0:
            response_text = "There's nothing to drill down into yet. Let's start with a summary."
            suggested = ["Show me a summary", "What insights do you have?"]
        else:
            # Get first insight for drill-down
            insight = insights_collection.insights[0]
            
            response_text = f"Drilling deeper into: {insight.title}\n\n"
            response_text += f"Full analysis:\n{insight.narrative}\n\n"
            
            if insight.key_metrics:
                response_text += "Key metrics:\n"
                for key, value in list(insight.key_metrics.items())[:5]:
                    response_text += f"• {key}: {value}\n"
            
            if insight.data_provenance:
                prov = insight.data_provenance[0]
                response_text += f"\nBased on {prov.data_points_used} data points "
                response_text += f"from {prov.source_path}\n"
            
            suggested = ["What caused this?", "Show me the raw data", "What should we do?"]
        
        return QueryResponse(
            response_text=response_text,
            intent=QueryIntent.DRILL_DOWN,
            confidence=0.8,
            insights_referenced=[insight.insight_id] if insight else [],
            suggested_questions=suggested
        )
    
    def _handle_recommendation(
        self, insights_collection: Optional[InsightCollection]
    ) -> QueryResponse:
        """Handle recommendation requests"""
        
        if not insights_collection or insights_collection.total_count == 0:
            response_text = "I need to analyze data before I can make recommendations."
            suggested = ["Process some data first", "What can you analyze?"]
        else:
            response_text = "Based on the analysis, here are my recommendations:\n\n"
            
            # Collect all recommendations
            all_recommendations = []
            for insight in insights_collection.insights:
                if insight.recommendations:
                    all_recommendations.extend(insight.recommendations)
            
            if all_recommendations:
                for i, rec in enumerate(all_recommendations[:5], 1):
                    response_text += f"{i}. {rec}\n"
                suggested = ["Why do you recommend this?", "What's the expected impact?"]
            else:
                response_text = "Based on current insights:\n"
                for insight in insights_collection.insights[:3]:
                    response_text += f"• Monitor {insight.title.lower()}\n"
                suggested = ["What else should I know?", "Show me the trends"]
        
        return QueryResponse(
            response_text=response_text,
            intent=QueryIntent.RECOMMENDATION,
            confidence=0.85,
            suggested_questions=suggested
        )
    
    def _handle_general(
        self, query: str, insights_collection: Optional[InsightCollection]
    ) -> QueryResponse:
        """Handle general questions"""
        
        response_text = "I'm here to help you understand your data and insights. "
        
        if insights_collection and insights_collection.total_count > 0:
            response_text += f"I currently have {insights_collection.total_count} insights available. "
            response_text += "You can ask me to:\n"
            response_text += "• Summarize the findings\n"
            response_text += "• Explain specific insights\n"
            response_text += "• Make recommendations\n"
            response_text += "• Compare metrics\n"
        else:
            response_text += "Let's start by analyzing some data.\n"
        
        suggested = ["Show me a summary", "What are the key insights?", "What should I focus on?"]
        
        return QueryResponse(
            response_text=response_text,
            intent=QueryIntent.GENERAL,
            confidence=0.6,
            suggested_questions=suggested
        )
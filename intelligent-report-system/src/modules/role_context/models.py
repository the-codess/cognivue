"""
Role-Context Models
Defines organizational roles and their information requirements
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Set, Any
from enum import Enum
from datetime import datetime

class RoleLevel(str, Enum):
    """Organizational role levels"""
    EXECUTIVE = "executive"
    DIRECTOR = "director"
    MANAGER = "manager"
    ANALYST = "analyst"
    SPECIALIST = "specialist"

class Department(str, Enum):
    """Organizational departments"""
    FINANCE = "finance"
    SALES = "sales"
    OPERATIONS = "operations"
    MARKETING = "marketing"
    HR = "human_resources"
    IT = "information_technology"
    PRODUCT = "product"
    CUSTOMER_SERVICE = "customer_service"

class DataGranularity(str, Enum):
    """Level of data detail"""
    ENTERPRISE = "enterprise"  # Company-wide aggregated
    DIVISION = "division"  # Division level
    DEPARTMENT = "department"  # Department level
    TEAM = "team"  # Team level
    INDIVIDUAL = "individual"  # Individual contributor level
    TRANSACTION = "transaction"  # Transaction/record level

class TemporalHorizon(str, Enum):
    """Time perspective for analysis"""
    REAL_TIME = "real_time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    MULTI_YEAR = "multi_year"

class VisualizationType(str, Enum):
    """Preferred visualization types"""
    EXECUTIVE_DASHBOARD = "executive_dashboard"
    DETAILED_REPORT = "detailed_report"
    TREND_CHART = "trend_chart"
    COMPARISON_TABLE = "comparison_table"
    METRIC_CARDS = "metric_cards"
    DRILL_DOWN_TABLE = "drill_down_table"
    GEOGRAPHIC_MAP = "geographic_map"

class DecisionContext(str, Enum):
    """Decision-making context"""
    STRATEGIC = "strategic"  # Long-term, high-level decisions
    TACTICAL = "tactical"  # Medium-term, department-level
    OPERATIONAL = "operational"  # Day-to-day operations

class KPI(BaseModel):
    """Key Performance Indicator definition"""
    name: str
    category: str  # financial, operational, customer, growth, etc.
    description: str
    formula: Optional[str] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None
    importance: int = Field(ge=1, le=10, default=5)  # 1-10 scale

class RoleProfile(BaseModel):
    """Complete profile for an organizational role"""
    role_id: str
    role_name: str
    role_level: RoleLevel
    department: Department
    
    # Information requirements
    data_granularity: List[DataGranularity]
    temporal_horizons: List[TemporalHorizon]
    preferred_visualizations: List[VisualizationType]
    decision_context: DecisionContext
    
    # KPIs and metrics
    primary_kpis: List[KPI]
    secondary_kpis: List[KPI] = []
    
    # Data access
    accessible_departments: List[Department]
    accessible_regions: List[str] = []  # Geographic scope
    
    # Insight preferences
    focus_areas: List[str]  # Areas of primary interest
    alert_triggers: List[str] = []  # What anomalies to flag
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class InsightRequirement(BaseModel):
    """Defines what insights a role needs"""
    role_id: str
    insight_types: List[str]  # trend, anomaly, comparison, forecast, etc.
    min_confidence: float = Field(ge=0.0, le=1.0, default=0.7)
    include_explanations: bool = True
    include_recommendations: bool = True
    max_insights_per_report: int = 10

class RoleContext(BaseModel):
    """Current context for a role's data request"""
    role_profile: RoleProfile
    current_time_period: str  # e.g., "2024-Q3"
    specific_filters: Dict[str, Any] = {}  # Additional filters
    urgency: str = "normal"  # low, normal, high, critical
    report_purpose: Optional[str] = None  # meeting, review, decision, etc.

class RoleHierarchy(BaseModel):
    """Defines reporting structure"""
    role_id: str
    reports_to: Optional[str] = None  # Parent role ID
    direct_reports: List[str] = []  # Child role IDs
    peers: List[str] = []  # Same-level roles

class DataAccessPolicy(BaseModel):
    """Access control for role-based data filtering"""
    role_id: str
    can_view_financial: bool = True
    can_view_hr: bool = False
    can_view_salaries: bool = False
    can_view_competitors: bool = True
    can_export_data: bool = True
    pii_access_level: str = "none"  # none, anonymized, full
    region_restrictions: List[str] = []
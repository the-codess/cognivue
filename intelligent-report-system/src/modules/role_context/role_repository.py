"""
Role Repository
Stores predefined organizational roles
"""
from typing import Dict, List, Optional
from src.modules.role_context.models import (
    RoleProfile, KPI, RoleLevel, Department, DataGranularity,
    TemporalHorizon, VisualizationType, DecisionContext, DataAccessPolicy
)
from src.utils.logger import app_logger as logger

class RoleRepository:
    """Repository of predefined organizational roles"""
    
    def __init__(self):
        self.roles: Dict[str, RoleProfile] = {}
        self.access_policies: Dict[str, DataAccessPolicy] = {}
        self._initialize_default_roles()
        logger.info(f"RoleRepository initialized with {len(self.roles)} roles")
    
    def _initialize_default_roles(self):
        """Initialize standard organizational roles"""
        
        # CFO - Chief Financial Officer
        cfo = RoleProfile(
            role_id="cfo",
            role_name="Chief Financial Officer",
            role_level=RoleLevel.EXECUTIVE,
            department=Department.FINANCE,
            data_granularity=[DataGranularity.ENTERPRISE, DataGranularity.DIVISION],
            temporal_horizons=[TemporalHorizon.QUARTERLY, TemporalHorizon.YEARLY, TemporalHorizon.MULTI_YEAR],
            preferred_visualizations=[VisualizationType.EXECUTIVE_DASHBOARD, VisualizationType.TREND_CHART],
            decision_context=DecisionContext.STRATEGIC,
            primary_kpis=[
                KPI(name="Revenue", category="financial", description="Total revenue", importance=10),
                KPI(name="Net Profit Margin", category="financial", description="Profit as % of revenue", unit="%", importance=10),
                KPI(name="Operating Cash Flow", category="financial", description="Cash from operations", importance=9),
                KPI(name="EBITDA", category="financial", description="Earnings before interest, taxes, depreciation", importance=9),
            ],
            secondary_kpis=[
                KPI(name="Customer Acquisition Cost", category="financial", description="Cost to acquire customer", importance=7),
                KPI(name="Return on Investment", category="financial", description="ROI percentage", unit="%", importance=8),
            ],
            accessible_departments=[d for d in Department],
            focus_areas=["financial_health", "profitability", "cash_flow", "strategic_investments"],
            alert_triggers=["revenue_decline", "margin_compression", "cash_flow_issues"]
        )
        
        # Regional Sales Manager
        regional_sales_mgr = RoleProfile(
            role_id="regional_sales_manager",
            role_name="Regional Sales Manager",
            role_level=RoleLevel.MANAGER,
            department=Department.SALES,
            data_granularity=[DataGranularity.DEPARTMENT, DataGranularity.TEAM, DataGranularity.INDIVIDUAL],
            temporal_horizons=[TemporalHorizon.DAILY, TemporalHorizon.WEEKLY, TemporalHorizon.MONTHLY],
            preferred_visualizations=[VisualizationType.DETAILED_REPORT, VisualizationType.DRILL_DOWN_TABLE, VisualizationType.GEOGRAPHIC_MAP],
            decision_context=DecisionContext.TACTICAL,
            primary_kpis=[
                KPI(name="Regional Sales", category="sales", description="Total sales in region", importance=10),
                KPI(name="Sales Growth Rate", category="sales", description="YoY growth", unit="%", importance=9),
                KPI(name="Sales per Rep", category="sales", description="Average sales per representative", importance=8),
                KPI(name="Customer Retention", category="customer", description="% customers retained", unit="%", importance=8),
            ],
            secondary_kpis=[
                KPI(name="Lead Conversion Rate", category="sales", description="% leads converted", unit="%", importance=7),
                KPI(name="Average Deal Size", category="sales", description="Average transaction value", importance=7),
            ],
            accessible_departments=[Department.SALES, Department.MARKETING, Department.CUSTOMER_SERVICE],
            accessible_regions=["assigned_region"],  # Specific to their region
            focus_areas=["territory_performance", "team_productivity", "customer_relationships", "pipeline_health"],
            alert_triggers=["quota_miss", "rep_underperformance", "customer_churn"]
        )
        
        # Financial Analyst
        financial_analyst = RoleProfile(
            role_id="financial_analyst",
            role_name="Financial Analyst",
            role_level=RoleLevel.ANALYST,
            department=Department.FINANCE,
            data_granularity=[DataGranularity.DEPARTMENT, DataGranularity.TEAM, DataGranularity.TRANSACTION],
            temporal_horizons=[TemporalHorizon.DAILY, TemporalHorizon.WEEKLY, TemporalHorizon.MONTHLY, TemporalHorizon.QUARTERLY],
            preferred_visualizations=[VisualizationType.DETAILED_REPORT, VisualizationType.COMPARISON_TABLE, VisualizationType.TREND_CHART],
            decision_context=DecisionContext.OPERATIONAL,
            primary_kpis=[
                KPI(name="Budget Variance", category="financial", description="Actual vs budget", unit="%", importance=9),
                KPI(name="Expense Ratio", category="financial", description="Expenses as % of revenue", unit="%", importance=8),
                KPI(name="Working Capital", category="financial", description="Current assets - liabilities", importance=8),
            ],
            secondary_kpis=[
                KPI(name="Days Sales Outstanding", category="financial", description="Average collection period", unit="days", importance=7),
                KPI(name="Inventory Turnover", category="operational", description="Times inventory sold/replaced", importance=6),
            ],
            accessible_departments=[Department.FINANCE, Department.OPERATIONS],
            focus_areas=["variance_analysis", "cost_control", "forecasting", "financial_modeling"],
            alert_triggers=["budget_overrun", "unusual_transactions", "forecast_deviation"]
        )
        
        # Marketing Director
        marketing_director = RoleProfile(
            role_id="marketing_director",
            role_name="Marketing Director",
            role_level=RoleLevel.DIRECTOR,
            department=Department.MARKETING,
            data_granularity=[DataGranularity.DIVISION, DataGranularity.DEPARTMENT, DataGranularity.TEAM],
            temporal_horizons=[TemporalHorizon.WEEKLY, TemporalHorizon.MONTHLY, TemporalHorizon.QUARTERLY],
            preferred_visualizations=[VisualizationType.EXECUTIVE_DASHBOARD, VisualizationType.TREND_CHART, VisualizationType.METRIC_CARDS],
            decision_context=DecisionContext.TACTICAL,
            primary_kpis=[
                KPI(name="Marketing ROI", category="marketing", description="Return on marketing spend", unit="%", importance=10),
                KPI(name="Lead Generation", category="marketing", description="Number of qualified leads", importance=9),
                KPI(name="Customer Acquisition Cost", category="marketing", description="Cost per customer acquired", importance=9),
                KPI(name="Brand Awareness", category="marketing", description="Brand recognition metrics", unit="%", importance=8),
            ],
            secondary_kpis=[
                KPI(name="Campaign Performance", category="marketing", description="Individual campaign metrics", importance=7),
                KPI(name="Website Traffic", category="marketing", description="Visitors to website", importance=7),
            ],
            accessible_departments=[Department.MARKETING, Department.SALES, Department.PRODUCT],
            focus_areas=["campaign_effectiveness", "lead_quality", "brand_metrics", "channel_performance"],
            alert_triggers=["campaign_underperformance", "cac_increase", "lead_quality_drop"]
        )
        
        # Operations Manager
        operations_manager = RoleProfile(
            role_id="operations_manager",
            role_name="Operations Manager",
            role_level=RoleLevel.MANAGER,
            department=Department.OPERATIONS,
            data_granularity=[DataGranularity.DEPARTMENT, DataGranularity.TEAM, DataGranularity.TRANSACTION],
            temporal_horizons=[TemporalHorizon.REAL_TIME, TemporalHorizon.DAILY, TemporalHorizon.WEEKLY],
            preferred_visualizations=[VisualizationType.DETAILED_REPORT, VisualizationType.METRIC_CARDS, VisualizationType.TREND_CHART],
            decision_context=DecisionContext.OPERATIONAL,
            primary_kpis=[
                KPI(name="Operational Efficiency", category="operational", description="Output per resource unit", unit="%", importance=9),
                KPI(name="On-Time Delivery", category="operational", description="% deliveries on time", unit="%", importance=9),
                KPI(name="Defect Rate", category="quality", description="% defective products", unit="%", importance=8),
                KPI(name="Resource Utilization", category="operational", description="% capacity utilized", unit="%", importance=8),
            ],
            secondary_kpis=[
                KPI(name="Cycle Time", category="operational", description="Time to complete process", unit="hours", importance=7),
                KPI(name="Cost per Unit", category="financial", description="Production cost per unit", importance=7),
            ],
            accessible_departments=[Department.OPERATIONS, Department.FINANCE],
            focus_areas=["process_efficiency", "quality_control", "capacity_management", "cost_optimization"],
            alert_triggers=["quality_issues", "delivery_delays", "capacity_constraints"]
        )
        
        # Store roles
        self.roles["cfo"] = cfo
        self.roles["regional_sales_manager"] = regional_sales_mgr
        self.roles["financial_analyst"] = financial_analyst
        self.roles["marketing_director"] = marketing_director
        self.roles["operations_manager"] = operations_manager
        
        # Define access policies
        self.access_policies["cfo"] = DataAccessPolicy(
            role_id="cfo",
            can_view_financial=True,
            can_view_hr=True,
            can_view_salaries=True,
            can_view_competitors=True,
            can_export_data=True,
            pii_access_level="full"
        )
        
        self.access_policies["regional_sales_manager"] = DataAccessPolicy(
            role_id="regional_sales_manager",
            can_view_financial=True,
            can_view_hr=False,
            can_view_salaries=False,
            can_view_competitors=True,
            can_export_data=True,
            pii_access_level="anonymized",
            region_restrictions=["assigned_region"]
        )
        
        self.access_policies["financial_analyst"] = DataAccessPolicy(
            role_id="financial_analyst",
            can_view_financial=True,
            can_view_hr=False,
            can_view_salaries=False,
            can_view_competitors=False,
            can_export_data=True,
            pii_access_level="none"
        )
        
        self.access_policies["marketing_director"] = DataAccessPolicy(
            role_id="marketing_director",
            can_view_financial=True,
            can_view_hr=False,
            can_view_salaries=False,
            can_view_competitors=True,
            can_export_data=True,
            pii_access_level="anonymized"
        )
        
        self.access_policies["operations_manager"] = DataAccessPolicy(
            role_id="operations_manager",
            can_view_financial=True,
            can_view_hr=False,
            can_view_salaries=False,
            can_view_competitors=False,
            can_export_data=True,
            pii_access_level="none"
        )
    
    def get_role(self, role_id: str) -> Optional[RoleProfile]:
        """Get role profile by ID"""
        return self.roles.get(role_id)
    
    def get_access_policy(self, role_id: str) -> Optional[DataAccessPolicy]:
        """Get access policy for role"""
        return self.access_policies.get(role_id)
    
    def list_roles(self) -> List[RoleProfile]:
        """Get all roles"""
        return list(self.roles.values())
    
    def get_roles_by_level(self, level: RoleLevel) -> List[RoleProfile]:
        """Get roles by organizational level"""
        return [role for role in self.roles.values() if role.role_level == level]
    
    def get_roles_by_department(self, department: Department) -> List[RoleProfile]:
        """Get roles by department"""
        return [role for role in self.roles.values() if role.department == department]
    
    def add_role(self, role: RoleProfile, access_policy: DataAccessPolicy):
        """Add custom role"""
        self.roles[role.role_id] = role
        self.access_policies[role.role_id] = access_policy
        logger.info(f"Added custom role: {role.role_name}")
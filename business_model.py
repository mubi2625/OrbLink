"""
Business Model for LEO Constellation Optimization Service

Defines revenue model, market analysis, and value proposition.
"""

from typing import Dict, List

# Service Pricing (USD)
BASIC_SUBSCRIPTION_MONTHLY = 5_000
PROFESSIONAL_SUBSCRIPTION_MONTHLY = 15_000
ENTERPRISE_SUBSCRIPTION_MONTHLY = 50_000
CONSTELLATION_DESIGN_PROJECT = 150_000  # One-time project
CONSULTING_HOURLY_RATE = 250
CUSTOM_ANALYSIS_BASE = 25_000

def get_service_tiers() -> Dict[str, Dict]:
    """
    Define service tier offerings and pricing.
    
    Returns:
        Service tier definitions
    """
    return {
        'Basic': {
            'price_monthly': BASIC_SUBSCRIPTION_MONTHLY,
            'price_annual': BASIC_SUBSCRIPTION_MONTHLY * 10,  # 2 months free
            'features': [
                'Web-based constellation simulator access',
                'Architecture comparison (ground vs crosslink)',
                'Cost and performance analysis',
                'Standard technical support',
                'Export reports (PDF, CSV)',
                'Up to 3 users'
            ],
            'target_customers': 'Small satellite startups, universities, early-stage companies'
        },
        'Professional': {
            'price_monthly': PROFESSIONAL_SUBSCRIPTION_MONTHLY,
            'price_annual': PROFESSIONAL_SUBSCRIPTION_MONTHLY * 10,
            'features': [
                'All Basic features',
                'NASA TLE data integration',
                'Debris risk analysis',
                'Regulatory compliance checklist',
                'Priority technical support',
                'Custom constellation scenarios',
                'API access for integration',
                'Up to 10 users',
                '5 hours monthly consulting included'
            ],
            'target_customers': 'Mid-size satellite operators, aerospace contractors, investors'
        },
        'Enterprise': {
            'price_monthly': ENTERPRISE_SUBSCRIPTION_MONTHLY,
            'price_annual': ENTERPRISE_SUBSCRIPTION_MONTHLY * 10,
            'features': [
                'All Professional features',
                'Dedicated account manager',
                'Custom feature development',
                'White-label options',
                'Priority feature requests',
                'Advanced debris modeling',
                'Regulatory filing support',
                'Unlimited users',
                '20 hours monthly consulting included',
                'On-site training available'
            ],
            'target_customers': 'Large satellite operators, government agencies, major aerospace firms'
        }
    }

def calculate_revenue_projections(years: int = 5) -> Dict[str, any]:
    """
    Project revenue growth over time.
    
    Conservative estimates based on market growth.
    
    Args:
        years: Number of years to project
        
    Returns:
        Revenue projections by year and tier
    """
    # Customer acquisition projections (conservative)
    projections = []
    
    for year in range(1, years + 1):
        # Customer counts (grow over time)
        if year == 1:
            basic_customers = 10
            pro_customers = 3
            enterprise_customers = 1
            design_projects = 2
        elif year == 2:
            basic_customers = 25
            pro_customers = 8
            enterprise_customers = 2
            design_projects = 5
        elif year == 3:
            basic_customers = 50
            pro_customers = 15
            enterprise_customers = 4
            design_projects = 10
        elif year == 4:
            basic_customers = 80
            pro_customers = 25
            enterprise_customers = 6
            design_projects = 15
        else:  # year 5+
            basic_customers = 120
            pro_customers = 35
            enterprise_customers = 10
            design_projects = 20
        
        # Annual revenue by source
        basic_revenue = basic_customers * BASIC_SUBSCRIPTION_MONTHLY * 12
        pro_revenue = pro_customers * PROFESSIONAL_SUBSCRIPTION_MONTHLY * 12
        enterprise_revenue = enterprise_customers * ENTERPRISE_SUBSCRIPTION_MONTHLY * 12
        project_revenue = design_projects * CONSTELLATION_DESIGN_PROJECT
        
        # Additional consulting (assume 20% of customers buy extra)
        consulting_hours = (basic_customers + pro_customers + enterprise_customers) * 0.2 * 10
        consulting_revenue = consulting_hours * CONSULTING_HOURLY_RATE
        
        total_revenue = (basic_revenue + pro_revenue + enterprise_revenue + 
                        project_revenue + consulting_revenue)
        
        projections.append({
            'year': year,
            'basic_customers': basic_customers,
            'pro_customers': pro_customers,
            'enterprise_customers': enterprise_customers,
            'total_customers': basic_customers + pro_customers + enterprise_customers,
            'basic_revenue': basic_revenue,
            'pro_revenue': pro_revenue,
            'enterprise_revenue': enterprise_revenue,
            'project_revenue': project_revenue,
            'consulting_revenue': consulting_revenue,
            'total_revenue': total_revenue
        })
    
    return {
        'projections': projections,
        'year_1_revenue': projections[0]['total_revenue'],
        'year_5_revenue': projections[-1]['total_revenue'],
        'cagr': ((projections[-1]['total_revenue'] / projections[0]['total_revenue']) ** (1/years) - 1) * 100
    }

def get_market_analysis() -> Dict[str, any]:
    """
    Market size and opportunity analysis.
    
    Returns:
        Market analysis data
    """
    return {
        'total_addressable_market': {
            'description': 'Global satellite operators and space agencies',
            'size_usd': 400_000_000_000,  # $400B satellite industry
            'growth_rate_annual': 0.08,  # 8% CAGR
            'note': 'Total satellite industry value'
        },
        'serviceable_addressable_market': {
            'description': 'LEO constellation planning and optimization',
            'size_usd': 5_000_000_000,  # $5B subset
            'growth_rate_annual': 0.15,  # 15% CAGR
            'note': 'Constellation design and consulting services'
        },
        'serviceable_obtainable_market': {
            'description': 'Realistic market capture in 5 years',
            'size_usd': 50_000_000,  # $50M
            'market_share': 0.01,  # 1% of SAM
            'note': 'Conservative estimate for new entrant'
        },
        'target_segments': [
            'Small satellite startups (100+ companies)',
            'Mid-size satellite operators (50+ companies)',
            'Large aerospace contractors (20+ companies)',
            'Government space agencies (10+ agencies)',
            'Investment firms evaluating space ventures (200+ firms)',
            'Academic institutions (50+ universities)'
        ],
        'market_drivers': [
            'LEO constellation boom (Starlink, OneWeb, Amazon Kuiper)',
            'Decreasing launch costs',
            'Increasing space debris concerns',
            'Regulatory complexity growing',
            'Need for optimization tools'
        ]
    }

def get_competitive_landscape() -> Dict[str, any]:
    """
    Competitive analysis.
    
    Returns:
        Competitor information
    """
    return {
        'direct_competitors': [
            {
                'name': 'AGI Systems Tool Kit (STK)',
                'strengths': 'Industry standard, comprehensive',
                'weaknesses': 'Expensive, complex, no business model focus',
                'pricing': 'Enterprise only, $50K+ per year'
            },
            {
                'name': 'Ansys Space',
                'strengths': 'Engineering focused, detailed simulation',
                'weaknesses': 'No cost optimization, steep learning curve',
                'pricing': 'Enterprise licenses, $100K+'
            }
        ],
        'indirect_competitors': [
            'Aerospace consulting firms (McKinsey, Deloitte Space practice)',
            'Academic research groups',
            'In-house tools at major operators'
        ],
        'competitive_advantages': [
            'Focus on business model optimization (not just technical)',
            'Web-based accessibility (no expensive software)',
            'Integrated debris and regulatory analysis',
            'Clear ROI and tipping point analysis',
            'Transparent pricing (SaaS model)',
            'NASA data integration',
            'Faster time-to-insight'
        ],
        'barriers_to_entry': [
            'Technical expertise required',
            'NASA and regulatory knowledge',
            'Customer relationships in space industry',
            'Ongoing data integration costs'
        ]
    }

def calculate_business_costs(years: int = 5) -> Dict[str, any]:
    """
    Calculate operational costs for the service business.
    
    Args:
        years: Number of years to project
        
    Returns:
        Cost projections
    """
    cost_projections = []
    
    for year in range(1, years + 1):
        # Team size grows with customers
        if year == 1:
            engineers = 3
            sales = 1
            support = 1
        elif year == 2:
            engineers = 5
            sales = 2
            support = 2
        elif year == 3:
            engineers = 8
            sales = 3
            support = 3
        elif year == 4:
            engineers = 12
            sales = 4
            support = 4
        else:
            engineers = 15
            sales = 5
            support = 5
        
        # Salaries (fully loaded with benefits)
        engineering_cost = engineers * 150_000
        sales_cost = sales * 120_000
        support_cost = support * 80_000
        total_personnel = engineering_cost + sales_cost + support_cost
        
        # Infrastructure
        cloud_hosting = 50_000 + (year * 20_000)  # Scales with usage
        data_subscriptions = 100_000  # NASA data, debris tracking
        software_licenses = 50_000
        
        # Marketing and sales
        marketing_budget = 200_000 * year  # Grows with scale
        
        # Office and operations
        office_cost = 100_000 + (engineers + sales + support) * 5_000
        
        # Total costs
        total_costs = (total_personnel + cloud_hosting + data_subscriptions + 
                      software_licenses + marketing_budget + office_cost)
        
        cost_projections.append({
            'year': year,
            'personnel_cost': total_personnel,
            'infrastructure_cost': cloud_hosting + data_subscriptions + software_licenses,
            'marketing_cost': marketing_budget,
            'operations_cost': office_cost,
            'total_cost': total_costs,
            'team_size': engineers + sales + support
        })
    
    return {
        'projections': cost_projections,
        'year_1_cost': cost_projections[0]['total_cost'],
        'year_5_cost': cost_projections[-1]['total_cost']
    }

def calculate_profitability(years: int = 5) -> Dict[str, any]:
    """
    Calculate profitability and key business metrics.
    
    Args:
        years: Number of years to project
        
    Returns:
        Profitability analysis
    """
    revenue_proj = calculate_revenue_projections(years)
    cost_proj = calculate_business_costs(years)
    
    profitability = []
    cumulative_profit = 0
    
    for i in range(years):
        revenue = revenue_proj['projections'][i]['total_revenue']
        costs = cost_proj['projections'][i]['total_cost']
        profit = revenue - costs
        cumulative_profit += profit
        margin = (profit / revenue * 100) if revenue > 0 else -100
        
        profitability.append({
            'year': i + 1,
            'revenue': revenue,
            'costs': costs,
            'profit': profit,
            'profit_margin': margin,
            'cumulative_profit': cumulative_profit
        })
    
    # Find break-even year
    break_even_year = None
    for p in profitability:
        if p['cumulative_profit'] > 0 and break_even_year is None:
            break_even_year = p['year']
    
    return {
        'profitability': profitability,
        'break_even_year': break_even_year if break_even_year else 'Beyond 5 years',
        'year_5_profit': profitability[-1]['profit'],
        'year_5_margin': profitability[-1]['profit_margin'],
        'total_investment_needed': abs(min([p['cumulative_profit'] for p in profitability]))
    }

def get_go_to_market_strategy() -> Dict[str, List[str]]:
    """
    Go-to-market strategy and customer acquisition.
    
    Returns:
        GTM strategy
    """
    return {
        'channels': [
            'Direct sales to satellite operators',
            'Partnerships with aerospace consultants',
            'Academic partnerships and research sponsorships',
            'Industry conference presentations',
            'NASA and ESA ecosystem engagement',
            'Content marketing (technical blog, whitepapers)',
            'Free tier or trial for universities'
        ],
        'customer_acquisition': [
            'Target recent FCC filers (public data)',
            'Attend satellite industry conferences',
            'Publish case studies and benchmarks',
            'Offer free constellation assessments',
            'Build relationships with space VCs',
            'Partner with launch providers for referrals'
        ],
        'retention_strategy': [
            'Continuous feature development',
            'Regular NASA data updates',
            'Customer success team',
            'Annual user conferences',
            'Feature voting by customers',
            'Long-term contracts with discounts'
        ],
        'expansion_opportunities': [
            'Add launch optimization module',
            'Integrate with mission planning tools',
            'Offer managed services (full outsourcing)',
            'Expand to GEO and MEO orbits',
            'International market expansion',
            'Government contracting'
        ]
    }


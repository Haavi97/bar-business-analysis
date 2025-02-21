import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, CustomJS
from bokeh.layouts import column, row
from bokeh.palettes import Spectral6

# Set page configuration
st.set_page_config(page_title="Bar Business Analysis", layout="wide")

# Title and Introduction
st.title("Bar Business Analysis Dashboard")
st.markdown("""
This dashboard helps analyze the financial viability of running a bar in Estonia.
It considers both fixed and variable costs, along with expected income to project business performance.
""")

# Sidebar for input parameters
st.sidebar.header("Business Parameters")

# Location and Size Parameters
st.sidebar.subheader("Location & Size")
location = st.sidebar.selectbox(
    "Location",
    ["City Center", "Non-central Location"],
    help="Location affects rent costs and potential customer base"
)

size = st.sidebar.slider(
    "Premises Size (m²)",
    min_value=50,
    max_value=300,
    value=150,
    step=10,
    help="Size affects rent, utilities, and maximum capacity"
)

# Calculate maximum capacity based on size
max_capacity = int(size * 0.75)  # Assuming 0.75 persons per m²

# Operating Parameters
st.sidebar.subheader("Operations")
operating_hours = st.sidebar.slider(
    "Daily Operating Hours",
    min_value=4,
    max_value=16,
    value=8,
    help="Affects labor costs and utilities"
)

days_per_week = st.sidebar.slider(
    "Operating Days per Week",
    min_value=3,
    max_value=7,
    value=6,
    help="Affects total monthly costs and revenue"
)

# Staff Parameters
st.sidebar.subheader("Staffing")
full_time_staff = st.sidebar.number_input(
    "Full-time Staff",
    min_value=1,
    max_value=10,
    value=2,
    help="Base staff for operations"
)

# Fixed Costs Calculations
def calculate_fixed_costs(location, size, full_time_staff):
    # Rent calculation
    rent_per_m2 = 17.5 if location == "City Center" else 10
    rent = size * rent_per_m2
    
    # Insurance costs
    insurance = 150 + (size * 0.5)  # Base + size-dependent component
    
    # Utilities base calculation
    utilities = size * 2.5  # €2.5 per m² for basic utilities
    
    # Labor costs (fixed component)
    labor_cost = full_time_staff * 1600 * 1.338  # Base salary + social tax + insurance
    
    # Other fixed costs
    licenses = 200  # Monthly amortized
    pos_system = 80
    security = 65
    internet = 50
    maintenance = size * 1  # €1 per m² for maintenance
    
    total_fixed = rent + insurance + utilities + labor_cost + licenses + pos_system + security + internet + maintenance
    
    return {
        'Rent': rent,
        'Insurance': insurance,
        'Utilities': utilities,
        'Labor': labor_cost,
        'Other': licenses + pos_system + security + internet + maintenance,
        'Total': total_fixed
    }

# Fixed Costs Section
st.header("Fixed Costs Analysis")

fixed_costs = calculate_fixed_costs(location, size, full_time_staff)

# Create Fixed Costs Bar Chart
fixed_costs_df = pd.DataFrame({
    'Category': ['Rent', 'Insurance', 'Utilities', 'Labor', 'Other'],
    'Cost': [fixed_costs['Rent'], fixed_costs['Insurance'], fixed_costs['Utilities'], 
             fixed_costs['Labor'], fixed_costs['Other']]
})

fixed_costs_df['color'] = Spectral6[:len(fixed_costs_df)]
source = ColumnDataSource(fixed_costs_df)

p = figure(x_range=fixed_costs_df['Category'].tolist(), height=400, title="Monthly Fixed Costs Breakdown")
p.vbar(x='Category', top='Cost', width=0.9, source=source, fill_color='color', line_color='color')
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.add_tools(HoverTool(tooltips=[("Category", "@Category"), ("Cost", "€@Cost{0,0}")]))

st.bokeh_chart(p, use_container_width=True)

# Variable Costs Section
st.header("Variable Costs Analysis")

# Variable cost parameters
st.sidebar.markdown("""
<style>
.tooltip {
    position: relative;
    display: inline-block;
    cursor: help;
}
.tooltip:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    background: #333;
    color: white;
    padding: 5px;
    border-radius: 5px;
    font-size: 14px;
    z-index: 1;
    width: 300px;
    left: 25px;
    top: -5px;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.sidebar.columns([4, 1])
with col1:
    avg_drink_price = st.slider("Average Drink Price (€)", 4.0, 12.0, 7.0)
with col2:
    st.markdown("""
    <div class="tooltip" data-tooltip="The average price customers pay per drink. Higher prices increase revenue but may reduce customer volume.">❓</div>
    """, unsafe_allow_html=True)

col1, col2 = st.sidebar.columns([4, 1])
with col1:
    pour_cost_percent = st.slider("Pour Cost Percentage", 15, 35, 22)
with col2:
    st.markdown("""
    <div class="tooltip" data-tooltip="Pour cost is the cost of ingredients as a percentage of the drink's price. Example: If a drink sells for €10 and costs €2 to make, pour cost is 20%. Industry standard is 18-24%. Lower is better but might affect quality.">❓</div>
    """, unsafe_allow_html=True)

col1, col2 = st.sidebar.columns([4, 1])
with col1:
    expected_customers_per_hour = st.slider("Expected Customers per Hour", 5, 50, 20)
with col2:
    st.markdown("""
    <div class="tooltip" data-tooltip="Average number of customers per hour. Affects revenue (customers × drinks per customer × price) and staffing needs. Typical bar serves 20-30 customers per hour. Weekend peaks can be 2-3× higher.">❓</div>
    """, unsafe_allow_html=True)

def calculate_variable_costs(customers_per_hour, operating_hours, days_per_week, pour_cost_percent, avg_drink_price):
    # Calculate monthly values
    monthly_hours = operating_hours * days_per_week * 4.33  # 4.33 weeks per month
    monthly_customers = customers_per_hour * monthly_hours
    
    # Beverage costs
    beverage_cost = monthly_customers * avg_drink_price * (pour_cost_percent/100)
    
    # Labor (variable component)
    staff_needed = max(1, customers_per_hour // 30)  # 1 staff per 30 customers
    labor_cost = staff_needed * monthly_hours * 10 * 1.338  # €10/hour + taxes
    
    # Consumables
    consumables = monthly_customers * 0.5  # €0.5 per customer for garnishes, napkins, etc.
    
    # Payment processing
    payment_processing = monthly_customers * avg_drink_price * 0.02  # 2% processing fee
    
    return {
        'Beverage Cost': beverage_cost,
        'Variable Labor': labor_cost,
        'Consumables': consumables,
        'Payment Processing': payment_processing,
        'Total': beverage_cost + labor_cost + consumables + payment_processing
    }

variable_costs = calculate_variable_costs(expected_customers_per_hour, operating_hours, 
                                       days_per_week, pour_cost_percent, avg_drink_price)

# Create Variable Costs Bar Chart
variable_costs_df = pd.DataFrame({
    'Category': ['Beverage Cost', 'Variable Labor', 'Consumables', 'Payment Processing'],
    'Cost': [variable_costs['Beverage Cost'], variable_costs['Variable Labor'],
             variable_costs['Consumables'], variable_costs['Payment Processing']]
})

variable_costs_df['color'] = Spectral6[2:2+len(variable_costs_df)]
source_var = ColumnDataSource(variable_costs_df)

p_var = figure(x_range=variable_costs_df['Category'].tolist(), height=400, title="Monthly Variable Costs Breakdown")
p_var.vbar(x='Category', top='Cost', width=0.9, source=source_var, fill_color='color', line_color='color')
p_var.xgrid.grid_line_color = None
p_var.y_range.start = 0
p_var.add_tools(HoverTool(tooltips=[("Category", "@Category"), ("Cost", "€@Cost{0,0}")]))

st.bokeh_chart(p_var, use_container_width=True)

# Revenue Projection
st.header("Revenue Analysis")

# Define seasonal factors
def get_seasonal_factor(month):
    # Summer boost (June-August)
    if month % 12 in [5, 6, 7]:
        return 1.25
    # Winter holidays (December)
    elif month % 12 == 11:
        return 1.4
    # Low season (January-February)
    elif month % 12 in [0, 1]:
        return 0.8
    # Regular months
    else:
        return 1.0

# Define growth pattern
def get_growth_factor(month):
    if month < 3:
        return 0.7 + (month * 0.1)  # Slow start
    elif month < 8:
        return 0.9 + (month * 0.05)  # Steeper growth
    else:
        return 1.2 + (month * 0.02)  # Gradual stabilization

# Calculate utility cost factor
def get_utility_factor(month):
    # Higher in summer and winter months
    if month % 12 in [0, 1, 6, 7]:  # Winter and summer peaks
        return 1.3
    else:
        return 1.0

# Calculate base revenue and costs
base_monthly_customers = expected_customers_per_hour * operating_hours * days_per_week * 4.33
base_monthly_revenue = base_monthly_customers * avg_drink_price
base_total_costs = fixed_costs['Total'] + variable_costs['Total']

# Create monthly projections for 36 months
months = list(range(1, 37))
revenue_projection = []
costs_projection = []

for month in range(36):
    # Revenue calculation with seasonality and growth
    seasonal_factor = get_seasonal_factor(month)
    growth_factor = get_growth_factor(month)
    monthly_revenue = base_monthly_revenue * seasonal_factor * growth_factor
    
    # Cost calculation with various factors
    utility_factor = get_utility_factor(month)
    staff_experience_factor = 1 + (month * 0.002)  # Small increase in staff costs over time
    maintenance_factor = 1 + (month * 0.005)  # Increasing maintenance costs
    
    # Apply factors to different cost components
    monthly_costs = base_total_costs * (
        0.4 +  # Fixed portion
        0.3 * utility_factor +  # Utilities portion
        0.2 * staff_experience_factor +  # Staff costs
        0.1 * maintenance_factor  # Maintenance
    )
    
    revenue_projection.append(monthly_revenue)
    costs_projection.append(monthly_costs)
profit_projection = [r - c for r, c in zip(revenue_projection, costs_projection)]

# Create projection chart
source_proj = ColumnDataSource({
    'months': months,
    'revenue': revenue_projection,
    'costs': costs_projection,
    'profit': profit_projection
})

p_proj = figure(height=400, title="12-Month Financial Projection", x_axis_label='Month', y_axis_label='Euros (€)')
p_proj.line('months', 'revenue', line_color='green', legend_label='Revenue', source=source_proj)
p_proj.line('months', 'costs', line_color='red', legend_label='Costs', source=source_proj)
p_proj.line('months', 'profit', line_color='blue', legend_label='Profit', source=source_proj)
p_proj.add_tools(HoverTool(tooltips=[
    ("Month", "@months"),
    ("Revenue", "€@revenue{0,0}"),
    ("Costs", "€@costs{0,0}"),
    ("Profit", "€@profit{0,0}")
]))

st.bokeh_chart(p_proj, use_container_width=True)

# Initial Capital Requirements
st.header("Initial Capital Requirements")

# Calculate setup costs
setup_costs = {
    'Renovation': size * 200,  # €200 per m²
    'Equipment': size * 300,  # €300 per m²
    'Initial Inventory': monthly_revenue * 0.5,  # Half month of revenue
    'Licenses & Permits': 3000,
    'Working Capital': monthly_costs * 3  # 3 months of operating costs
}

total_setup = sum(setup_costs.values())

# Create setup costs chart
setup_df = pd.DataFrame({
    'Category': list(setup_costs.keys()),
    'Cost': list(setup_costs.values())
})

setup_df['color'] = Spectral6[:len(setup_df)]
source_setup = ColumnDataSource(setup_df)

p_setup = figure(x_range=setup_df['Category'].tolist(), height=400, title="Initial Capital Requirements")
p_setup.vbar(x='Category', top='Cost', width=0.9, source=source_setup, fill_color='color', line_color='color')
p_setup.xgrid.grid_line_color = None
p_setup.y_range.start = 0
p_setup.add_tools(HoverTool(tooltips=[("Category", "@Category"), ("Cost", "€@Cost{0,0}")]))

st.bokeh_chart(p_setup, use_container_width=True)

# Summary metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Monthly Fixed Costs", f"€{fixed_costs['Total']:,.2f}")
with col2:
    st.metric("Monthly Variable Costs", f"€{variable_costs['Total']:,.2f}")
with col3:
    st.metric("Projected First Month Profit", f"€{profit_projection[0]:,.2f}")

st.metric("Total Initial Capital Required", f"€{total_setup:,.2f}")

# Payback Period Analysis
st.header("Investment Payback Analysis")

# Calculate cumulative cash flow
cumulative_cash_flow = [-total_setup]  # Start with initial investment as negative
monthly_profits = [r - c for r, c in zip(revenue_projection, costs_projection)]

for profit in monthly_profits:
    cumulative_cash_flow.append(cumulative_cash_flow[-1] + profit)

# Find break-even point (when cumulative cash flow becomes positive)
break_even_month = next((i for i, cf in enumerate(cumulative_cash_flow) if cf >= 0), len(cumulative_cash_flow))

# Create payback period visualization
source_payback = ColumnDataSource({
    'months': list(range(0, len(cumulative_cash_flow))),
    'cash_flow': cumulative_cash_flow
})

p_payback = figure(height=400, 
                  title=f"Investment Payback Analysis (Break-even: {break_even_month} months)",
                  x_axis_label='Months',
                  y_axis_label='Cumulative Cash Flow (€)')

# Add horizontal line at y=0 to show break-even point
p_payback.line(x=[0, 36], y=[0, 0], line_color='gray', line_dash='dashed')

# Add main cash flow line
p_payback.line('months', 'cash_flow', line_color='blue', line_width=2, source=source_payback)

# Add break-even point marker
if break_even_month < len(cumulative_cash_flow):
    break_even_value = cumulative_cash_flow[break_even_month]
    p_payback.circle(x=[break_even_month], y=[break_even_value], size=10, color='green')

# Add hover tool
p_payback.add_tools(HoverTool(tooltips=[
    ("Month", "@months"),
    ("Cash Flow", "€@cash_flow{0,0}")
]))

st.bokeh_chart(p_payback, use_container_width=True)

# Add explanation of the break-even analysis
st.markdown(f"""
### Break-even Analysis Summary:
- Initial Investment: €{total_setup:,.2f}
- Expected Break-even Point: {break_even_month} months
- First Month Projected Profit: €{profit_projection[0]:,.2f}
- Return on Investment (ROI) after 3 years: {((cumulative_cash_flow[-1] + total_setup)/total_setup * 100):.1f}%
""")

# Add notes about key relationships
st.markdown("""
### Key Relationship Notes:
- Location affects both rent costs and potential customer volume
- Size affects maximum capacity, rent, and utilities
- Operating hours affect both fixed and variable labor costs
- Customer volume affects variable costs and staffing requirements
- Pour cost percentage directly impacts profitability
""")
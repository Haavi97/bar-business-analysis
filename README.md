# 🍸 Bar Business Analysis Dashboard

## Overview
An interactive Streamlit dashboard for analyzing the financial viability of running a bar business in Estonia. This tool provides comprehensive analysis of costs, revenue projections, and investment returns using realistic business modeling.

![Python](https://img.shields.io/badge/python-v3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.29-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### Financial Analysis
- **Fixed Costs Breakdown**
  - Rent calculations based on location and size
  - Insurance costs with property value scaling
  - Utility cost projections with seasonal variations
  - Staff costs with social taxes
  - Licensing and operational expenses

### Dynamic Projections
- **Revenue Modeling**
  - Seasonal variation patterns
  - Growth projections with realistic phases
  - Customer volume analysis
  - Price point optimization

### Cost Analysis
- **Sophisticated Cost Modeling**
  - Step-function staffing costs
  - Non-linear scaling of variable costs
  - Seasonal utility variations
  - Time-dependent maintenance costs
  - Pour cost analysis

### Investment Analysis
- **ROI Calculations**
  - Break-even point analysis
  - Initial capital requirements
  - 3-year profitability projections
  - Cash flow visualizations

## 📊 Business Parameters

### Location & Size
- Premises location (City Center/Non-central)
- Floor space (m²)
- Maximum capacity calculations

### Operational Parameters
- Operating hours
- Days per week
- Staffing levels
- Average drink prices
- Pour cost percentages

## 🚀 Getting Started

### Live Demo
Check out the live demo of the dashboard at [bar-business-analysis.streamlit.app](https://bar-business-analysis.streamlit.app)

### Prerequisites
- Python 3.11 (recommended)
- Virtual environment manager

We strongly recommend using Python 3.11 for optimal performance and compatibility. While the application may work with other Python versions, it has been thoroughly tested with Python 3.11.

### Setting up the Development Environment

1. Create and activate a virtual environment:

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

### Installation
1. Clone the repository:
```bash
git clone git@github.com:Haavi97/bar-business-analysis.git
cd bar-business-analysis
```

2. Install dependencies:
```bash
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install streamlit==1.29.0
pip install bokeh==3.3.0
```

3. Run the dashboard:
```bash
streamlit run bar_dashboard.py
```

## 📖 Usage Guide

### Setting Up Initial Parameters
1. Use the sidebar to input basic business parameters:
   - Location selection
   - Premises size
   - Operating hours
   - Staffing levels

### Understanding the Metrics
- **Pour Cost**: Cost of ingredients as a percentage of drink price
  - Industry standard: 18-24%
  - Lower percentages indicate better margins

- **Customer Volume**: Expected customers per hour
  - Affects staffing requirements
  - Influences utility costs
  - Drives revenue projections

### Interpreting Results
- **Break-even Analysis**: Shows when initial investment will be recovered
- **Profit Projections**: Monthly and annual profit expectations
- **Cost Breakdown**: Detailed analysis of fixed and variable costs

## 🔄 Business Model Assumptions

### Seasonal Variations
- Summer months: +20-30% revenue
- Winter holidays: +40% revenue
- January-February: -20% revenue
- Spring/Fall: Baseline

### Growth Patterns
- Months 1-3: Initial slow growth
- Months 4-8: Accelerated growth
- Months 9+: Stabilization

### Cost Scaling
- Fixed costs: 60% of base costs
- Staff costs: Step function based on customer volume
- Variable costs: Non-linear scaling with revenue
- Maintenance: Time-dependent increase

## 📝 Notes
- All financial calculations are in Euros (€)
- Tax calculations based on Estonian regulations
- Labor costs include social tax (33%) and unemployment insurance (0.8%)
- Utility costs include seasonal variations for heating/cooling

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- Estonian Business Registry for standard cost metrics
- Local bar owners for operational insights
- Streamlit and Bokeh communities for visualization capabilities

## 🚀 Deployment

### Deploying to Streamlit Cloud

1. **Prerequisites**
   - A GitHub account
   - Your code pushed to a GitHub repository
   - Requirements.txt file containing:
     ```
     numpy==1.24.3
     pandas==2.0.3
     streamlit==1.29.0
     bokeh==3.3.0
     ```

2. **Step-by-Step Deployment**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository from the list
   - Select the branch (usually `main`)
   - Select the main file: `bar_dashboard.py`
   - Click "Deploy!"

3. **Deployment Settings**
   - In your repository, create a file `.streamlit/config.toml`:
     ```toml
     [theme]
     primaryColor = "#E694FF"
     backgroundColor = "#00172B"
     secondaryBackgroundColor = "#0083B8"
     textColor = "#FFF"
     font = "sans serif"
     ```

4. **Advanced Settings**
   - You can customize your app's resources in Streamlit Cloud:
     - Memory
     - CPU allocation
     - Python version (we recommend 3.11)
     - Custom subdomains
   - Access these in the app settings after deployment

5. **Troubleshooting**
   - Check deployment logs in Streamlit Cloud
   - Ensure all dependencies are in requirements.txt
   - Verify file paths are relative to the repository root
   - Monitor app health in Streamlit Cloud dashboard

### Live Demo
The dashboard is live at [bar-business-analysis.streamlit.app](https://bar-business-analysis.streamlit.app)

Visit the demo to:
- Explore financial projections
- Test different business scenarios
- Analyze cost structures
- Evaluate investment requirements

### Environment Variables

## 📬 Contact
For questions and feedback:
- Create an issue in the repository

---
*Remember to adjust all financial projections based on your specific circumstances and market conditions.*
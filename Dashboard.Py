import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Kenya Manufacturing Dashboard", layout="wide")

# Dashboard title
st.title("🏭 Kenya Manufacturing Sector Dashboard")
st.markdown("#### Based on KAM Manufacturing Barometer Survey | 2023 – 2025")
st.markdown("---")

# Generate manufacturing data based on KAM Barometer
def generate_manufacturing_data():
    np.random.seed(42)
    
    # Sectors from the barometer
    sectors = [
        "Food & Beverages", "Building, Mining & Construction", "Chemical & Allied",
        "Metal & Allied", "Plastics & Rubber", "Pharmaceutical & Medical Equipment",
        "Textile & Apparel", "Energy, Electrical & Electronics", "Paper & Board",
        "Timber, Wood & Furniture", "Leather & Footwear", "Automotive",
        "Agriculture & Fresh Produce", "Service & Consultancy"
    ]
    
    # Products by sector (for detailed analysis)
    products = {
        "Food & Beverages": ["Maize Flour", "Wheat Flour", "Cooking Oil", "Milk", "Beverages", "Sugar"],
        "Building, Mining & Construction": ["Cement", "Steel Bars", "Roofing Sheets", "Paints", "Ceramic Tiles", "Glass"],
        "Chemical & Allied": ["Fertilizers", "Industrial Chemicals", "Soaps", "Detergents", "Pesticides"],
        "Metal & Allied": ["Iron Sheets", "Aluminum", "Copper Cables", "Metal Fabrications"],
        "Plastics & Rubber": ["Plastic Pipes", "Packaging Materials", "Rubber Products", "Containers"],
        "Pharmaceutical & Medical Equipment": ["Tablets", "Syrups", "Medical Devices", "Disposables"],
        "Textile & Apparel": ["Cotton Fabric", "Garments", "Uniforms", "Bed Sheets"],
        "Energy, Electrical & Electronics": ["Solar Panels", "Cables", "Batteries", "LED Lights"],
        "Paper & Board": ["Paper", "Cardboard", "Tissue Paper", "Stationery"],
        "Timber, Wood & Furniture": ["Timber", "Furniture", "Plywood", "Doors"],
        "Leather & Footwear": ["Leather", "Shoes", "Bags", "Belts"],
        "Automotive": ["Vehicle Parts", "Assemblies", "Spare Parts"],
        "Agriculture & Fresh Produce": ["Processed Fruits", "Vegetables", "Coffee", "Tea"],
        "Service & Consultancy": ["Engineering Services", "Logistics", "Maintenance"]
    }
    
    years = [2023, 2024, 2025]
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    
    # KAM Barometer survey responses (Q2 2025 data from your document)
    economic_outlook = {"Positive": 6.67, "Neutral": 40.00, "Negative": 53.33}
    business_outlook = {"Optimistic": 7.14, "Neutral": 50.00, "Pessimistic": 42.60}
    operating_capacity = {"Quarter": 31.77, "Half": 30.77, "ThreeQuarter": 23.08, "NearFull": 15.38}
    cost_of_inputs = {"Increasing": 76.92, "Stable": 23.08, "Decreasing": 0}
    workforce_change = {"Increasing": 16.67, "Stable": 33.33, "Decreasing": 50.00}
    investment_plans = {"Yes": 37.5, "No": 62.5}
    
    data = []
    
    for year in years:
        year_growth = 1 + (year - 2023) * 0.05
        
        for sector in sectors:
            # GDP Contribution (varies by sector)
            if sector in ["Food & Beverages", "Building, Mining & Construction"]:
                gdp_contribution = np.random.uniform(12, 18) * year_growth
            elif sector in ["Chemical & Allied", "Metal & Allied"]:
                gdp_contribution = np.random.uniform(8, 12) * year_growth
            else:
                gdp_contribution = np.random.uniform(2, 6) * year_growth
            
            # Employment (thousands of jobs)
            if sector in ["Food & Beverages", "Textile & Apparel"]:
                employment = np.random.uniform(50, 150) * year_growth
            elif sector in ["Building, Mining & Construction", "Metal & Allied"]:
                employment = np.random.uniform(30, 80) * year_growth
            else:
                employment = np.random.uniform(5, 30) * year_growth
            
            # Sales (KES Millions)
            sales = np.random.uniform(5000, 50000) * year_growth
            
            # Production Volume (units)
            production = np.random.uniform(10000, 200000) * year_growth
            
            # Operating capacity based on barometer data
            if year == 2025:
                capacity = np.random.choice(
                    ["Quarter (25%)", "Half (50%)", "Three-Quarter (75%)", "Near Full (90%+)"],
                    p=[operating_capacity["Quarter"]/100, operating_capacity["Half"]/100, 
                       operating_capacity["ThreeQuarter"]/100, operating_capacity["NearFull"]/100]
                )
            else:
                capacity = np.random.choice(
                    ["Quarter (25%)", "Half (50%)", "Three-Quarter (75%)", "Near Full (90%+)"],
                    p=[0.25, 0.35, 0.25, 0.15]
                )
            
            for quarter in quarters:
                # Seasonal variations
                if quarter == "Q4":
                    season_factor = 1.3
                elif quarter == "Q1":
                    season_factor = 0.8
                else:
                    season_factor = 1.0
                
                quarterly_sales = sales / 4 * season_factor * np.random.uniform(0.9, 1.1)
                quarterly_production = production / 4 * season_factor * np.random.uniform(0.9, 1.1)
                quarterly_employment = employment / 4 * season_factor
                
                # Barriers to growth (from barometer)
                barriers = {
                    "High Taxation": np.random.choice([0, 1], p=[0.17, 0.83]) if year >= 2024 else 0,
                    "Low Demand": np.random.choice([0, 1], p=[0.17, 0.83]) if year >= 2024 else 0,
                    "Regulatory Uncertainty": np.random.choice([0, 1], p=[0.25, 0.75]) if year >= 2024 else 0,
                    "Unhealthy Competition": np.random.choice([0, 1], p=[0.5, 0.5]) if year >= 2024 else 0,
                    "High Input Costs": np.random.choice([0, 1], p=[0.23, 0.77]) if year >= 2024 else 0,
                }
                
                data.append({
                    "Year": year,
                    "Quarter": quarter,
                    "Sector": sector,
                    "Product": np.random.choice(products.get(sector, ["General"]), 1)[0],
                    "GDP_Contribution_Pct": round(gdp_contribution, 2),
                    "Employment_Jobs": int(employment * 1000),
                    "Sales_KES_Millions": round(quarterly_sales, 2),
                    "Production_Volume": int(quarterly_production),
                    "Operating_Capacity": capacity,
                    "Cost_Inputs_Trend": "Increasing" if year == 2025 else np.random.choice(["Increasing", "Stable", "Decreasing"], p=[0.5, 0.4, 0.1]),
                    "Workforce_Outlook": np.random.choice(["Increasing", "Stable", "Decreasing"], p=[0.17, 0.33, 0.5]) if year == 2025 else "Stable",
                    "Investment_Plans": "Yes" if np.random.random() < 0.375 and year == 2025 else "No",
                    "High_Taxation_Barrier": barriers["High Taxation"],
                    "Low_Demand_Barrier": barriers["Low Demand"],
                    "Regulatory_Barrier": barriers["Regulatory Uncertainty"],
                    "Competition_Barrier": barriers["Unhealthy Competition"],
                    "Input_Costs_Barrier": barriers["High Input Costs"]
                })
    
    return pd.DataFrame(data)

# Load data
df = generate_manufacturing_data()

# Calculate aggregated metrics
total_gdp = df["GDP_Contribution_Pct"].sum()
total_employment = df["Employment_Jobs"].sum()
total_sales = df["Sales_KES_Millions"].sum()
total_production = df["Production_Volume"].sum()

# Industry averages
avg_capacity_utilisation = df["Operating_Capacity"].value_counts().idxmax() if len(df) > 0 else "N/A"

# Sidebar Filters
st.sidebar.header("🔍 Filter Dashboard")

# Year filter
years = st.sidebar.multiselect("Select Year(s)", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
filtered_df = df[df["Year"].isin(years)]

# Quarter filter
quarters = st.sidebar.multiselect("Select Quarter(s)", df["Quarter"].unique(), default=df["Quarter"].unique())
filtered_df = filtered_df[filtered_df["Quarter"].isin(quarters)]

# Sector filter
sectors = st.sidebar.multiselect("Select Sector(s)", df["Sector"].unique(), default=df["Sector"].unique())
filtered_df = filtered_df[filtered_df["Sector"].isin(sectors)]

# Product filter
products_list = st.sidebar.multiselect("Select Product(s)", df["Product"].unique(), default=df["Product"].unique())
if products_list:
    filtered_df = filtered_df[filtered_df["Product"].isin(products_list)]

# KAM Barometer Quick Stats from your document
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 KAM Barometer Q2 2025")
st.sidebar.metric("Economic Outlook", "53.3% Negative", delta="-46.7%")
st.sidebar.metric("Business Outlook", "42.6% Pessimistic", delta="-35.5%")
st.sidebar.metric("Input Costs", "76.9% Increasing", delta="+29.9%")
st.sidebar.metric("Workforce Expected", "50% Decreasing", delta="-33.3%")
st.sidebar.metric("Investment Plans", "62.5% No Investment", delta="-15.8%")

# Key Metrics Row
st.header("📊 Manufacturing Sector Overview")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🏭 GDP Contribution", f"{total_gdp:,.1f}%", delta="+5.2%")
with col2:
    st.metric("👥 Employment Created", f"{total_employment/1000:,.0f}K jobs")
with col3:
    st.metric("💰 Total Sales", f"KES {total_sales/1000:,.0f}B")
with col4:
    st.metric("📦 Production Volume", f"{total_production/1000000:,.1f}M units")
with col5:
    st.metric("⚙️ Capacity Utilisation", avg_capacity_utilisation)

st.markdown("---")

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 GDP & Economic Impact",
    "👥 Employment Analysis",
    "💰 Sales & Production",
    "🏗️ Building Materials Focus",
    "⚠️ Barriers & Challenges",
    "📊 KAM Barometer Insights",
    "📋 Data & Export"
])

# ==============================
# TAB 1: GDP & Economic Impact
# ==============================
with tab1:
    st.subheader("GDP Contribution by Sector (2023-2025)")
    
    gdp_by_sector = filtered_df.groupby(["Year", "Sector"])["GDP_Contribution_Pct"].sum().reset_index()
    top_10_gdp = gdp_by_sector.groupby("Sector")["GDP_Contribution_Pct"].sum().nlargest(10).index
    gdp_top = gdp_by_sector[gdp_by_sector["Sector"].isin(top_10_gdp)]
    
    fig1 = px.bar(
        gdp_top,
        x="Sector",
        y="GDP_Contribution_Pct",
        color="Year",
        title="Top 10 Sectors by GDP Contribution (%)",
        barmode="group",
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # GDP Growth Trend
        gdp_trend = filtered_df.groupby("Year")["GDP_Contribution_Pct"].sum().reset_index()
        fig2 = px.line(
            gdp_trend,
            x="Year",
            y="GDP_Contribution_Pct",
            title="Total Manufacturing GDP Contribution Trend",
            markers=True,
            line_shape="spline"
        )
        fig2.update_layout(yaxis_title="GDP Contribution (%)")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Quarter over Quarter GDP
        gdp_quarterly = filtered_df.groupby(["Year", "Quarter"])["GDP_Contribution_Pct"].sum().reset_index()
        fig3 = px.bar(
            gdp_quarterly,
            x="Quarter",
            y="GDP_Contribution_Pct",
            color="Year",
            title="Quarterly GDP Contribution",
            barmode="group"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # GDP vs Employment scatter
    fig4 = px.scatter(
        filtered_df,
        x="GDP_Contribution_Pct",
        y="Employment_Jobs",
        size="Sales_KES_Millions",
        color="Sector",
        hover_name="Sector",
        title="GDP Contribution vs Employment Creation",
        labels={"GDP_Contribution_Pct": "GDP Contribution (%)", "Employment_Jobs": "Employment (Jobs)"}
    )
    st.plotly_chart(fig4, use_container_width=True)

# ==============================
# TAB 2: Employment Analysis
# ==============================
with tab2:
    st.subheader("Employment Trends in Manufacturing")
    
    # Employment by sector
    employment_by_sector = filtered_df.groupby(["Year", "Sector"])["Employment_Jobs"].sum().reset_index()
    top_employment = employment_by_sector.groupby("Sector")["Employment_Jobs"].sum().nlargest(10).index
    emp_top = employment_by_sector[employment_by_sector["Sector"].isin(top_employment)]
    
    fig5 = px.bar(
        emp_top,
        x="Sector",
        y="Employment_Jobs",
        color="Year",
        title="Top 10 Employment Generating Sectors",
        barmode="group",
        labels={"Employment_Jobs": "Number of Jobs"},
        text_auto=True
    )
    st.plotly_chart(fig5, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Employment growth trend
        employment_trend = filtered_df.groupby("Year")["Employment_Jobs"].sum().reset_index()
        fig6 = px.area(
            employment_trend,
            x="Year",
            y="Employment_Jobs",
            title="Total Manufacturing Employment Trend",
            markers=True,
            labels={"Employment_Jobs": "Total Jobs"}
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        # Workforce outlook (from barometer)
        workforce_outlook = filtered_df.groupby(["Year", "Workforce_Outlook"]).size().reset_index(name="Count")
        fig7 = px.bar(
            workforce_outlook,
            x="Year",
            y="Count",
            color="Workforce_Outlook",
            title="Workforce Outlook (Next 6 Months)",
            barmode="group",
            color_discrete_map={"Increasing": "#2ecc71", "Stable": "#f1c40f", "Decreasing": "#e74c3c"}
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    # Jobs per sector pie chart (latest year)
    st.subheader(f"Employment Distribution ({max(years) if years else 2025})")
    latest_employment = filtered_df[filtered_df["Year"] == max(years) if years else 2025].groupby("Sector")["Employment_Jobs"].sum()
    fig8 = px.pie(
        values=latest_employment.values,
        names=latest_employment.index,
        title=f"Sector-wise Employment Share ({max(years) if years else 2025})",
        hole=0.3
    )
    st.plotly_chart(fig8, use_container_width=True)

# ==============================
# TAB 3: Sales & Production
# ==============================
with tab3:
    st.subheader("Sales and Production Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by sector
        sales_by_sector = filtered_df.groupby(["Year", "Sector"])["Sales_KES_Millions"].sum().reset_index()
        top_sales = sales_by_sector.groupby("Sector")["Sales_KES_Millions"].sum().nlargest(10).index
        sales_top = sales_by_sector[sales_by_sector["Sector"].isin(top_sales)]
        
        fig9 = px.bar(
            sales_top,
            x="Sector",
            y="Sales_KES_Millions",
            color="Year",
            title="Top 10 Sectors by Sales (KES Millions)",
            barmode="group",
            labels={"Sales_KES_Millions": "Sales (KES Millions)"}
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        # Production by sector
        production_by_sector = filtered_df.groupby(["Year", "Sector"])["Production_Volume"].sum().reset_index()
        top_production = production_by_sector.groupby("Sector")["Production_Volume"].sum().nlargest(10).index
        prod_top = production_by_sector[production_by_sector["Sector"].isin(top_production)]
        
        fig10 = px.bar(
            prod_top,
            x="Sector",
            y="Production_Volume",
            color="Year",
            title="Top 10 Sectors by Production Volume",
            barmode="group",
            labels={"Production_Volume": "Production Volume (Units)"}
        )
        st.plotly_chart(fig10, use_container_width=True)
    
    # Sales trend over quarters
    st.subheader("Quarterly Sales Trend")
    quarterly_sales = filtered_df.groupby(["Year", "Quarter"])["Sales_KES_Millions"].sum().reset_index()
    fig11 = px.line(
        quarterly_sales,
        x="Quarter",
        y="Sales_KES_Millions",
        color="Year",
        title="Sales Performance by Quarter",
        markers=True
    )
    st.plotly_chart(fig11, use_container_width=True)
    
    # Operating Capacity Heatmap
    st.subheader("Operating Capacity Utilisation")
    capacity_data = filtered_df.groupby(["Year", "Operating_Capacity"]).size().reset_index(name="Count")
    capacity_pivot = capacity_data.pivot(index="Year", columns="Operating_Capacity", values="Count").fillna(0)
    
    fig12 = px.imshow(
        capacity_pivot,
        text_auto=True,
        aspect="auto",
        title="Operating Capacity Distribution",
        labels={"x": "Capacity Level", "y": "Year", "color": "Number of Firms"}
    )
    st.plotly_chart(fig12, use_container_width=True)

# ==============================
# TAB 4: Building Materials Focus
# ==============================
with tab4:
    st.subheader("Building Materials Sector Deep Dive")
    
    # Filter for building materials sector
    building_materials = filtered_df[filtered_df["Sector"] == "Building, Mining & Construction"]
    
    if not building_materials.empty:
        # Products within building materials
        product_performance = building_materials.groupby(["Year", "Product"])[["Sales_KES_Millions", "Production_Volume"]].sum().reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig13 = px.bar(
                product_performance,
                x="Product",
                y="Sales_KES_Millions",
                color="Year",
                title="Building Materials: Sales by Product (KES Millions)",
                barmode="group"
            )
            st.plotly_chart(fig13, use_container_width=True)
        
        with col2:
            fig14 = px.bar(
                product_performance,
                x="Product",
                y="Production_Volume",
                color="Year",
                title="Building Materials: Production Volume by Product",
                barmode="group"
            )
            st.plotly_chart(fig14, use_container_width=True)
        
        # Cement and Steel focus
        st.subheader("Key Building Materials Performance")
        key_products = ["Cement", "Steel Bars", "Roofing Sheets"]
        key_performance = building_materials[building_materials["Product"].isin(key_products)]
        
        if not key_performance.empty:
            fig15 = px.line(
                key_performance,
                x="Year",
                y="Sales_KES_Millions",
                color="Product",
                title="Key Products Sales Trend",
                markers=True
            )
            st.plotly_chart(fig15, use_container_width=True)
        
        # Construction sector contribution
        construction_gdp = building_materials.groupby("Year")["GDP_Contribution_Pct"].sum().reset_index()
        fig16 = px.bar(
            construction_gdp,
            x="Year",
            y="GDP_Contribution_Pct",
            title="Building & Construction Sector GDP Contribution",
            text_auto=True,
            color="GDP_Contribution_Pct",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig16, use_container_width=True)
    else:
        st.info("No data available for Building, Mining & Construction sector with current filters.")

# ==============================
# TAB 5: Barriers & Challenges
# ==============================
with tab5:
    st.subheader("Barriers to Manufacturing Growth")
    
    # Barriers from KAM Barometer
    barrier_cols = ["High_Taxation_Barrier", "Low_Demand_Barrier", "Regulatory_Barrier", "Competition_Barrier", "Input_Costs_Barrier"]
    barrier_names = ["High Taxation", "Low Demand", "Regulatory Uncertainty", "Unhealthy Competition", "High Input Costs"]
    
    barrier_data = []
    for year in filtered_df["Year"].unique():
        year_data = filtered_df[filtered_df["Year"] == year]
        for i, col in enumerate(barrier_cols):
            pct = (year_data[col].sum() / len(year_data)) * 100
            barrier_data.append({
                "Year": year,
                "Barrier": barrier_names[i],
                "Percentage": pct
            })
    
    barrier_df = pd.DataFrame(barrier_data)
    
    fig17 = px.bar(
        barrier_df,
        x="Barrier",
        y="Percentage",
        color="Year",
        title="Barriers to Business Growth (% of Manufacturers)",
        barmode="group",
        labels={"Percentage": "Manufacturers Affected (%)"}
    )
    st.plotly_chart(fig17, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost of inputs trend
        input_costs = filtered_df.groupby(["Year", "Cost_Inputs_Trend"]).size().reset_index(name="Count")
        fig18 = px.bar(
            input_costs,
            x="Year",
            y="Count",
            color="Cost_Inputs_Trend",
            title="Cost of Industrial Inputs Trend",
            barmode="group",
            color_discrete_map={"Increasing": "#e74c3c", "Stable": "#f1c40f", "Decreasing": "#2ecc71"}
        )
        st.plotly_chart(fig18, use_container_width=True)
    
    with col2:
        # Investment plans
        investment = filtered_df.groupby(["Year", "Investment_Plans"]).size().reset_index(name="Count")
        investment = investment[investment["Investment_Plans"] != ""]
        fig19 = px.pie(
            investment[investment["Year"] == max(filtered_df["Year"])] if not filtered_df.empty else investment,
            values="Count",
            names="Investment_Plans",
            title=f"Investment Plans ({max(filtered_df['Year']) if not filtered_df.empty else '2025'})",
            hole=0.3,
            color_discrete_map={"Yes": "#2ecc71", "No": "#e74c3c"}
        )
        st.plotly_chart(fig19, use_container_width=True)

# ==============================
# TAB 6: KAM Barometer Insights
# ==============================
with tab6:
    st.subheader("KAM Manufacturing Barometer - Key Insights (Q2 2025)")
    
    # Display barometer data from your document
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📉 Economic Outlook")
        economic_data = pd.DataFrame({
            "Outlook": ["Positive", "Neutral", "Negative"],
            "Percentage": [6.67, 40.00, 53.33]
        })
        fig20 = px.bar(
            economic_data,
            x="Outlook",
            y="Percentage",
            title="Views about Kenyan Economy",
            color="Outlook",
            color_discrete_map={"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"},
            text_auto=True
        )
        st.plotly_chart(fig20, use_container_width=True)
        
        st.markdown("### 📊 Operating Capacity")
        capacity_data_baro = pd.DataFrame({
            "Capacity": ["Quarter (25%)", "Half (50%)", "Three-Quarter (75%)", "Near Full (90%+)"],
            "Percentage": [31.77, 30.77, 23.08, 15.38]
        })
        fig21 = px.bar(
            capacity_data_baro,
            x="Capacity",
            y="Percentage",
            title="Firms' Operating Capacity",
            color="Percentage",
            color_continuous_scale="Blues",
            text_auto=True
        )
        st.plotly_chart(fig21, use_container_width=True)
    
    with col2:
        st.markdown("### 🔮 Business Outlook")
        business_data = pd.DataFrame({
            "Outlook": ["Optimistic", "Neutral", "Pessimistic"],
            "Percentage": [7.14, 50.00, 42.60]
        })
        fig22 = px.bar(
            business_data,
            x="Outlook",
            y="Percentage",
            title="Manufacturing Business Outlook (Next 6 Months)",
            color="Outlook",
            color_discrete_map={"Optimistic": "#2ecc71", "Neutral": "#f1c40f", "Pessimistic": "#e74c3c"},
            text_auto=True
        )
        st.plotly_chart(fig22, use_container_width=True)
        
        st.markdown("### 💰 Cost of Industrial Inputs")
        cost_data = pd.DataFrame({
            "Trend": ["Increasing", "Stable", "Decreasing"],
            "Percentage": [76.92, 23.08, 0]
        })
        fig23 = px.bar(
            cost_data,
            x="Trend",
            y="Percentage",
            title="Cost of Industrial Inputs Q2 2025",
            color="Trend",
            color_discrete_map={"Increasing": "#e74c3c", "Stable": "#f1c40f", "Decreasing": "#2ecc71"},
            text_auto=True
        )
        st.plotly_chart(fig23, use_container_width=True)
    
    # Purchase order levels
    st.markdown("### 📦 Purchase Order Levels")
    po_data = pd.DataFrame({
        "Level": ["More than normal", "Normal", "Less than normal"],
        "Percentage": [7.14, 28.57, 64.29]
    })
    fig24 = px.bar(
        po_data,
        x="Level",
        y="Percentage",
        title="Level of Purchase Orders Q2 2025",
        color="Level",
        color_discrete_map={"More than normal": "#2ecc71", "Normal": "#f1c40f", "Less than normal": "#e74c3c"},
        text_auto=True
    )
    st.plotly_chart(fig24, use_container_width=True)
    
    # Top reasons from barometer
    st.markdown("### 📋 Key Challenges Identified by Manufacturers")
    challenges = [
        "High taxation and new taxes/duties",
        "Low consumer demand / Low disposable income",
        "Illicit trade and unfair competition",
        "High operational and input costs",
        "Regulatory uncertainty",
        "Cash flow challenges and delayed pending bills",
        "Geopolitical tensions affecting supply chains",
        "High freight charges and shipping delays"
    ]
    
    for challenge in challenges:
        st.warning(f"⚠️ {challenge}")

# ==============================
# TAB 7: Data & Export
# ==============================
with tab7:
    st.subheader("Detailed Manufacturing Data")
    
    # Display filtered data
    display_df = filtered_df.copy()
    display_df["Sales_KES_Billions"] = display_df["Sales_KES_Millions"] / 1000
    st.dataframe(display_df, use_container_width=True)
    
    # Download button
    st.subheader("📎 Export Data")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Manufacturing Data as CSV",
        data=csv,
        file_name="kenya_manufacturing_data_2023_2025.csv",
        mime="text/csv"
    )
    
    # Summary statistics
    st.subheader("Summary Statistics")
    summary = filtered_df.groupby(["Year", "Sector"]).agg({
        "GDP_Contribution_Pct": "sum",
        "Employment_Jobs": "sum",
        "Sales_KES_Millions": "sum",
        "Production_Volume": "sum"
    }).round(2)
    st.dataframe(summary, use_container_width=True)
    
    # Investment trends
    st.subheader("Investment Plans Summary")
    investment_summary = filtered_df.groupby(["Year", "Investment_Plans"]).size().reset_index(name="Number_of_Firms")
    st.dataframe(investment_summary, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📌 Kenya Manufacturing Dashboard | Data Source: KAM Manufacturing Barometer Survey (Q2 2025) & Synthetic Data | 2023-2025")
st.caption("For enquiries & feedback contact: info@kam.co.ke")

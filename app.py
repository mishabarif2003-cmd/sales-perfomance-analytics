"""
Sales Performance Analytics Dashboard
--------------------------------------
An interactive Streamlit dashboard for exploring sales, profit, customer
and product performance using Pandas, NumPy and Plotly Express.

Run with:  streamlit run app.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================================================
# 1. PAGE CONFIG
# ==========================================================================
st.set_page_config(
    page_title="Sales Performance Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- Professional color theme -------------------------------------------
PRIMARY_COLOR = "#2E5CB8"
ACCENT_COLOR = "#00B4A6"
NEGATIVE_COLOR = "#E15759"
PLOTLY_TEMPLATE = "plotly_white"
COLOR_SEQUENCE = px.colors.qualitative.Bold

# ---- Light custom CSS for a cleaner, more professional look -------------
st.markdown(
    """
    <style>
        .main { background-color: #F7F9FC; }
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E6E9F0;
            border-radius: 10px;
            padding: 15px 15px 5px 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        h1, h2, h3 { color: #1F2A44; }
        .stTabs [data-baseweb="tab"] { font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================================
# 2. DATA LOADING (cached for fast reloads)
# ==========================================================================
@st.cache_data(show_spinner="Loading sales data...")
def load_data(path: str) -> pd.DataFrame:
    """Load the sales CSV, parse dates, and add helper columns."""
    try:
        df = pd.read_csv(path, parse_dates=["Order Date", "Ship Date"])
    except FileNotFoundError:
        st.error(f"Data file not found at '{path}'. Please check the /data folder.")
        st.stop()
    except Exception as e:
        st.error(f"Error while loading data: {e}")
        st.stop()

    # Helper / derived columns
    df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Order Year"] = df["Order Date"].dt.year
    df["Days to Ship"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Profit Margin %"] = np.where(
        df["Sales"] != 0, (df["Profit"] / df["Sales"]) * 100, 0
    )
    return df


DATA_PATH = "data/sales.csv"
raw_df = load_data(DATA_PATH)


# ==========================================================================
# 3. SIDEBAR FILTERS
# ==========================================================================
st.sidebar.title("🔎 Filters")
st.sidebar.markdown("Use the filters below to slice the dashboard.")

min_date, max_date = raw_df["Order Date"].min(), raw_df["Order Date"].max()

date_range = st.sidebar.date_input(
    "📅 Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

region_filter = st.sidebar.multiselect(
    "🌍 Region", options=sorted(raw_df["Region"].unique()), default=None,
    placeholder="All regions",
)
category_filter = st.sidebar.multiselect(
    "📦 Category", options=sorted(raw_df["Category"].unique()), default=None,
    placeholder="All categories",
)
segment_filter = st.sidebar.multiselect(
    "🧑‍💼 Segment", options=sorted(raw_df["Segment"].unique()), default=None,
    placeholder="All segments",
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit, Pandas, NumPy & Plotly Express")


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters to the raw dataframe. Defensive against bad input."""
    filtered = df.copy()

    # Date range filter (handles case where user picks only one date)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["Order Date"] >= pd.to_datetime(start))
            & (filtered["Order Date"] <= pd.to_datetime(end))
        ]

    if region_filter:
        filtered = filtered[filtered["Region"].isin(region_filter)]
    if category_filter:
        filtered = filtered[filtered["Category"].isin(category_filter)]
    if segment_filter:
        filtered = filtered[filtered["Segment"].isin(segment_filter)]

    return filtered


df = apply_filters(raw_df)

if df.empty:
    st.warning("⚠️ No data matches the selected filters. Please broaden your filter selection.")
    st.stop()


# ==========================================================================
# 4. HEADER
# ==========================================================================
st.title("📊 Sales Performance Analytics Dashboard")
st.caption(
    f"Showing **{len(df):,}** of {len(raw_df):,} orders | "
    f"Date range: {df['Order Date'].min().date()} → {df['Order Date'].max().date()}"
)

# ==========================================================================
# 5. KPI CARDS
# ==========================================================================
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
avg_order_value = total_sales / total_orders if total_orders else 0
overall_margin = (total_profit / total_sales * 100) if total_sales else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Sales", f"${total_sales:,.0f}")
k2.metric("📈 Total Profit", f"${total_profit:,.0f}")
k3.metric("🧾 Total Orders", f"{total_orders:,}")
k4.metric("🛒 Avg Order Value", f"${avg_order_value:,.2f}")
k5.metric("📐 Profit Margin", f"{overall_margin:,.1f}%")

st.markdown("---")


# ==========================================================================
# 6. TABS
# ==========================================================================
tab_overview, tab_products, tab_customers, tab_data, tab_insights = st.tabs(
    ["📈 Overview", "📦 Products & Discounts", "🧑‍💼 Customers", "🗂️ Data Explorer",
     "💡 Insights & Recommendations"]
)

# --------------------------------------------------------------------------
# TAB 1: OVERVIEW — trends, category, region
# --------------------------------------------------------------------------
with tab_overview:
    col1, col2 = st.columns(2)

    with col1:
        monthly = df.groupby("Order Month", as_index=False)["Sales"].sum()
        fig = px.line(
            monthly, x="Order Month", y="Sales", markers=True,
            title="Monthly Sales Trend", template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[PRIMARY_COLOR],
        )
        fig.update_layout(yaxis_title="Sales ($)", xaxis_title="Month")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        monthly_p = df.groupby("Order Month", as_index=False)["Profit"].sum()
        fig = px.area(
            monthly_p, x="Order Month", y="Profit",
            title="Monthly Profit Trend", template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[ACCENT_COLOR],
        )
        fig.update_layout(yaxis_title="Profit ($)", xaxis_title="Month")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        cat_sales = df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales")
        fig = px.bar(
            cat_sales, x="Sales", y="Category", orientation="h",
            title="Sales by Category", template=PLOTLY_TEMPLATE,
            color="Category", color_discrete_sequence=COLOR_SEQUENCE, text_auto=".2s",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        region_sales = df.groupby("Region", as_index=False)["Sales"].sum()
        fig = px.pie(
            region_sales, names="Region", values="Sales", hole=0.45,
            title="Sales by Region", template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_SEQUENCE,
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("ℹ️ About these charts"):
        st.write(
            "Monthly trends reveal seasonality. Category and region breakdowns show "
            "where revenue concentration lies, useful for resource allocation."
        )

# --------------------------------------------------------------------------
# TAB 2: PRODUCTS & DISCOUNTS
# --------------------------------------------------------------------------
with tab_products:
    col1, col2 = st.columns(2)

    with col1:
        top_products = (
            df.groupby("Product Name", as_index=False)["Sales"]
            .sum().sort_values("Sales", ascending=False).head(10)
        )
        fig = px.bar(
            top_products.sort_values("Sales"), x="Sales", y="Product Name",
            orientation="h", title="Top 10 Products by Sales",
            template=PLOTLY_TEMPLATE, color="Sales",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            df, x="Sales", y="Profit", color="Category", size="Quantity",
            hover_data=["Product Name"], title="Sales vs Profit Scatter",
            template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        disc_bin = pd.cut(
            df["Discount"], bins=[-0.01, 0, 0.1, 0.2, 0.3, 1],
            labels=["0%", "1-10%", "11-20%", "21-30%", "30%+"]
        )
        disc_profit = df.groupby(disc_bin, observed=True, as_index=False)["Profit"].mean()
        disc_profit.columns = ["Discount Band", "Avg Profit"]
        fig = px.bar(
            disc_profit, x="Discount Band", y="Avg Profit",
            title="Discount Impact on Average Profit", template=PLOTLY_TEMPLATE,
            color="Avg Profit", color_continuous_scale="RdYlGn",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        if "Payment Mode" in df.columns:
            pay_dist = df["Payment Mode"].value_counts().reset_index()
            pay_dist.columns = ["Payment Mode", "Count"]
            fig = px.pie(
                pay_dist, names="Payment Mode", values="Count",
                title="Payment Mode Distribution", template=PLOTLY_TEMPLATE,
                color_discrete_sequence=COLOR_SEQUENCE,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Payment Mode column not available in this dataset.")

# --------------------------------------------------------------------------
# TAB 3: CUSTOMERS
# --------------------------------------------------------------------------
with tab_customers:
    top_customers = (
        df.groupby("Customer Name", as_index=False)
        .agg(Total_Sales=("Sales", "sum"), Orders=("Order ID", "nunique"),
             Total_Profit=("Profit", "sum"))
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )
    fig = px.bar(
        top_customers.sort_values("Total_Sales"), x="Total_Sales", y="Customer Name",
        orientation="h", title="Top 10 Customers by Sales", template=PLOTLY_TEMPLATE,
        color="Total_Profit", color_continuous_scale="Teal",
    )
    st.plotly_chart(fig, use_container_width=True)

    seg_col1, seg_col2 = st.columns(2)
    with seg_col1:
        seg_sales = df.groupby("Segment", as_index=False)["Sales"].sum()
        fig = px.bar(
            seg_sales, x="Segment", y="Sales", title="Sales by Segment",
            template=PLOTLY_TEMPLATE, color="Segment", color_discrete_sequence=COLOR_SEQUENCE,
        )
        st.plotly_chart(fig, use_container_width=True)

    with seg_col2:
        st.metric("👥 Unique Customers", f"{df['Customer Name'].nunique():,}")
        st.dataframe(top_customers, use_container_width=True, hide_index=True)

# --------------------------------------------------------------------------
# TAB 4: DATA EXPLORER — searchable, sortable, downloadable
# --------------------------------------------------------------------------
with tab_data:
    st.subheader("🗂️ Order-Level Data")

    search_term = st.text_input("🔍 Search (Customer, Product, Order ID, State...)")

    display_df = df.copy()
    if search_term:
        mask = display_df.astype(str).apply(
            lambda col: col.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[mask]

    st.dataframe(
        display_df.sort_values("Order Date", ascending=False),
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )

# --------------------------------------------------------------------------
# TAB 5: INSIGHTS & RECOMMENDATIONS (auto-generated from the filtered data)
# --------------------------------------------------------------------------
with tab_insights:

    def generate_insights(data: pd.DataFrame) -> list:
        """Compute 10 data-driven insight strings from the current dataframe."""
        insights = []

        best_cat = data.groupby("Category")["Sales"].sum().idxmax()
        insights.append(f"**{best_cat}** is the top-selling category, driving the largest share of revenue.")

        worst_margin_cat = data.groupby("Category")["Profit Margin %"].mean().idxmin()
        insights.append(f"**{worst_margin_cat}** has the lowest average profit margin among all categories.")

        best_region = data.groupby("Region")["Sales"].sum().idxmax()
        insights.append(f"The **{best_region}** region generates the highest total sales.")

        top_month = data.groupby("Order Month")["Sales"].sum().idxmax()
        insights.append(f"Peak sales month is **{top_month.strftime('%B %Y')}**, indicating seasonal demand.")

        high_disc_corr = data[data["Discount"] >= 0.2]["Profit"].mean()
        low_disc_corr = data[data["Discount"] < 0.2]["Profit"].mean()
        if high_disc_corr < low_disc_corr:
            insights.append(
                f"Orders with discounts ≥20% average **${high_disc_corr:,.0f}** profit vs "
                f"**${low_disc_corr:,.0f}** for lower discounts — heavy discounting erodes profit."
            )
        else:
            insights.append("High discount orders do not show a significant negative impact on profit.")

        top_segment = data.groupby("Segment")["Sales"].sum().idxmax()
        insights.append(f"The **{top_segment}** segment contributes the most to overall revenue.")

        loss_orders_pct = (data["Profit"] < 0).mean() * 100
        insights.append(f"**{loss_orders_pct:.1f}%** of orders are sold at a loss (negative profit).")

        avg_ship_days = data["Days to Ship"].mean()
        insights.append(f"Average shipping time across all orders is **{avg_ship_days:.1f} days**.")

        top_product = data.groupby("Product Name")["Sales"].sum().idxmax()
        insights.append(f"**{top_product}** is the single best-selling product by revenue.")

        repeat_rate = (data["Customer Name"].value_counts() > 1).mean() * 100
        insights.append(f"**{repeat_rate:.1f}%** of customers have placed more than one order (repeat buyers).")

        aov_by_segment = data.groupby("Segment")["Sales"].mean().idxmax()
        insights.append(f"The **{aov_by_segment}** segment has the highest average order value.")

        return insights[:10]

    def generate_recommendations(data: pd.DataFrame) -> list:
        """Compute 10 business recommendation strings from the current dataframe."""
        recs = []

        worst_margin_cat = data.groupby("Category")["Profit Margin %"].mean().idxmin()
        recs.append(f"Review pricing and cost structure for **{worst_margin_cat}** to improve thin margins.")

        recs.append("Cap discounts above 20% to categories/products with proven demand elasticity, "
                     "since heavy discounting is squeezing profit.")

        weakest_region = data.groupby("Region")["Sales"].sum().idxmin()
        recs.append(f"Invest in targeted marketing for the **{weakest_region}** region, currently the weakest performer.")

        loss_share = (data["Profit"] < 0).mean() * 100
        if loss_share > 5:
            recs.append("Audit loss-making orders — consider minimum order values or renegotiated supplier costs.")
        else:
            recs.append("Loss-making orders are minimal; maintain current pricing discipline.")

        recs.append("Launch loyalty or bundle offers for top customers to increase repeat purchase rate.")

        best_cat = data.groupby("Category")["Sales"].sum().idxmax()
        recs.append(f"Expand product range and inventory in **{best_cat}**, the strongest revenue driver.")

        recs.append("Align inventory and staffing with the identified peak sales month to avoid stockouts.")

        recs.append("Negotiate faster shipping options where average ship time exceeds customer expectations.")

        weak_segment = data.groupby("Segment")["Sales"].sum().idxmin()
        recs.append(f"Create tailored offers for the **{weak_segment}** segment to grow its contribution.")

        recs.append("Introduce dynamic, data-driven discounting instead of flat discount tiers to protect margin.")

        return recs[:10]

    st.subheader("💡 Automated Business Insights")
    insights = generate_insights(df)
    for i, text in enumerate(insights, 1):
        st.markdown(f"**{i}.** {text}")

    st.markdown("---")

    st.subheader("✅ Business Recommendations")
    recommendations = generate_recommendations(df)
    for i, text in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {text}")

    with st.expander("📌 Methodology"):
        st.write(
            "Insights and recommendations are computed live from the currently filtered "
            "dataset using Pandas group-by aggregations — they update automatically as "
            "you change the sidebar filters."
        )

# ==========================================================================
# 7. FOOTER
# ==========================================================================
st.markdown("---")
st.caption("Sales Performance Analytics Dashboard · Built with Streamlit, Pandas, NumPy & Plotly Express")

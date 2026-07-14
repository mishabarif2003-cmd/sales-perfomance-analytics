# 📊 Sales Performance Analytics Dashboard

An interactive, professional-grade **Sales Analytics Dashboard** built with **Streamlit**, **Pandas**, **NumPy**, and **Plotly Express**. It turns raw order-level sales data into KPIs, trends, product/customer insights, and auto-generated business recommendations.

---

## 🚀 Project Overview

This project simulates a real-world retail/superstore sales analytics tool. It loads a sales dataset, lets users filter it by date range, region, category, and segment, and instantly visualizes performance across sales, profit, products, customers, and payment behavior — plus a data-driven insights and recommendations engine.

---

## ✨ Features

- **KPI Cards**: Total Sales, Total Profit, Total Orders, Average Order Value, Profit Margin
- **Sidebar Filters**: Date range, Region, Category, Segment
- **Interactive Charts** (Plotly Express):
  - Monthly Sales Trend
  - Monthly Profit Trend
  - Sales by Category
  - Sales by Region
  - Top 10 Products
  - Top 10 Customers
  - Sales vs Profit Scatter Plot
  - Discount Impact on Profit
  - Payment Mode Distribution
- **Data Explorer Tab**: Search, sort, and download filtered data as CSV
- **Automated Insights**: 10 auto-generated, data-driven insights
- **Automated Recommendations**: 10 business recommendations based on the analytics
- **Professional UI**: Wide layout, custom color theme, tabs, expanders, icons, responsive metrics

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data manipulation & aggregation |
| NumPy | Numerical calculations |
| Plotly Express | Interactive charting |
| Streamlit | Web dashboard framework |

---

## 📁 Folder Structure

```
Sales_Analytics_Dashboard/
│
├── app.py                # Main Streamlit application
├── generate_data.py       # Synthetic data generator (creates data/sales.csv)
├── data/
│   └── sales.csv          # Sales dataset (6,000 rows)
├── requirements.txt       # Python dependencies
├── README.md               # Project documentation
└── screenshots/            # Dashboard screenshots
```

---

## ⚙️ Installation

1. **Clone or download** this project folder.
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Project

The dataset (`data/sales.csv`) is already included. If you want to regenerate it:

```bash
python generate_data.py
```

Then launch the dashboard:

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🖼️ Dashboard Screenshots

> Add your own screenshots to the `screenshots/` folder and reference them here, e.g.:

```
screenshots/
├── overview_tab.png
├── products_tab.png
├── customers_tab.png
└── insights_tab.png
```

`![Overview](screenshots/overview_tab.png)`

---

## 📈 Dataset

The bundled dataset is a **synthetic, realistic sales dataset** (6,000 rows) modeled after the popular "Superstore Sales" format, including:

`Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Region, State, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit, Payment Mode`

You can swap in a real dataset (e.g. Kaggle's Superstore Sales) by replacing `data/sales.csv` with matching column names.

---

## 🔮 Future Improvements

- Add authentication for multi-user access
- Connect to a live database (PostgreSQL / BigQuery) instead of a static CSV
- Add forecasting (e.g. Prophet / ARIMA) for sales prediction
- Export full PDF report generation
- Add cohort and customer lifetime value (CLV) analysis
- Deploy to Streamlit Community Cloud / Docker container
- Add role-based dashboards (Sales Manager vs Executive view)

---

## 📄 License

This project is provided for educational and portfolio purposes.

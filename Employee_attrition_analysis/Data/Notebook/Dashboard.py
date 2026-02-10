import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide")

st.title("📊 Employee Attrition & Workforce Dashboard")

# -----------------------
# Load Data
# -----------------------
df = pd.read_csv(r"C:\Users\nandn\OneDrive\Documents\Employee_attrition_analysis\Data\WA_Fn-UseC_-HR-Employee-Attrition.csv")

# -----------------------
# Data Preparation
# -----------------------
df["Attrition Count"] = df["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

department_filter = st.sidebar.multiselect(
    "Select Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_filtered = df[
    (df["Department"].isin(department_filter)) &
    (df["Gender"].isin(gender_filter))
]

# -----------------------
# KPI Section
# -----------------------
total_employees = len(df_filtered)
attrition_rate = df_filtered["Attrition Count"].sum() / total_employees
avg_income = df_filtered["MonthlyIncome"].mean()
avg_years = df_filtered["YearsAtCompany"].mean()
avg_satisfaction = df_filtered["JobSatisfaction"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Employees", total_employees)
col2.metric("Attrition Rate", f"{attrition_rate:.2%}")
col3.metric("Avg Monthly Income", f"{avg_income:,.0f}")
col4.metric("Avg Years at Company", f"{avg_years:.1f}")
col5.metric("Avg Job Satisfaction", f"{avg_satisfaction:.2f}")

st.divider()

# -----------------------
# Attrition by Department
# -----------------------
st.subheader("Attrition by Department")

dept_data = df_filtered.groupby("Department")["Attrition Count"].sum()

fig1, ax1 = plt.subplots()
dept_data.plot(kind="bar", ax=ax1)
st.pyplot(fig1)

# -----------------------
# Attrition by Job Role
# -----------------------
st.subheader("Attrition by Job Role")

role_data = df_filtered.groupby("JobRole")["Attrition Count"].sum()

fig2, ax2 = plt.subplots()
role_data.sort_values().plot(kind="barh", ax=ax2)
st.pyplot(fig2)

# -----------------------
# Attrition Trend by Years at Company
# -----------------------
st.subheader("Attrition Trend by Experience")

trend_data = df_filtered.groupby("YearsAtCompany")["Attrition Count"].sum()

fig3, ax3 = plt.subplots()
trend_data.plot(kind="line", marker="o", ax=ax3)
st.pyplot(fig3)

# -----------------------
# Salary vs Attrition
# -----------------------
st.subheader("Salary Distribution vs Attrition")

fig4, ax4 = plt.subplots()
df_filtered.boxplot(column="MonthlyIncome", by="Attrition", ax=ax4)
plt.suptitle("")
st.pyplot(fig4)

# -----------------------
# Overtime Impact
# -----------------------
st.subheader("Overtime Impact on Attrition")

overtime_data = df_filtered.groupby("OverTime")["Attrition Count"].sum()

fig5, ax5 = plt.subplots()
ax5.pie(overtime_data, labels=overtime_data.index, autopct="%1.1f%%")
st.pyplot(fig5)











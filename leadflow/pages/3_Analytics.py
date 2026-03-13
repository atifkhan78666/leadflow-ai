import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_all_leads

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.title("Lead Generation Analytics")

st.write("Overview of scraped leads and outreach performance.")

rows = get_all_leads()

if len(rows) == 0:
    st.warning("No data available yet. Generate leads first.")
    st.stop()

df = pd.DataFrame(rows)

df.columns = [
    "ID",
    "Name",
    "Address",
    "Phone",
    "Website",
    "Email",
    "Rating",
    "Reviews",
    "Maps URL",
    "Industry",
    "Location",
    "Scraped At",
    "Email Sent"
]

total_leads = len(df)
emails_available = df["Email"].notnull().sum()
emails_sent = df["Email Sent"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Leads Scraped", total_leads)
col2.metric("Leads With Email", emails_available)
col3.metric("Emails Sent", emails_sent)

st.divider()

st.subheader("Leads by Industry")

industry_chart = px.histogram(
    df,
    x="Industry",
    title="Industry Distribution"
)

st.plotly_chart(industry_chart, use_container_width=True)

st.subheader("Leads by Location")

location_chart = px.histogram(
    df,
    x="Location",
    title="Location Distribution"
)

st.plotly_chart(location_chart, use_container_width=True)

st.subheader("Outreach Status")

status_counts = df["Email Sent"].value_counts().rename(
    {0: "Not Contacted", 1: "Email Sent"}
)

status_df = pd.DataFrame({
    "Status": status_counts.index,
    "Count": status_counts.values
})

status_chart = px.pie(
    status_df,
    names="Status",
    values="Count",
    title="Email Outreach Status"
)

st.plotly_chart(status_chart, use_container_width=True)

st.subheader("Lead Database")

st.dataframe(df, use_container_width=True)
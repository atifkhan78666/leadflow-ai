import streamlit as st
import pandas as pd

from scraper import scrape_leads, enrich_emails
from database import insert_lead, create_table

st.set_page_config(page_title="Lead Generator", layout="wide")

st.title("AI Lead Generator")
st.write("Scrape business leads from Google Maps and store them in your database.")

create_table()
st.sidebar.header("Lead Filters")
# industry = st.sidebar.selectbox(
#     "Industry",
#     [
#         "Technology",
#         "Healthcare",
#         "Finance",
#         "Retail",
#         "Education",
#         "Law firm"
#     ]
# )
search_query = st.text_input(
    "Search Businesses",
    placeholder="Example: salon near Dubai, bakery in Delhi, dentist in London"
)
col1, col2 = st.columns(2)
with col1:
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0)
with col2:
    min_reviews = st.number_input("Minimum Reviews", 0, 1000, 0)

# location = st.sidebar.text_input("Location")
location = ""

num_leads = st.sidebar.slider(
    "Number of Leads",
    min_value=2,
    max_value=200,
    value=50
)

generate_button = st.sidebar.button("Generate Leads")


if generate_button:

    if search_query == "":
        st.error("Please enter a search query")
        st.stop()
    with st.spinner("Finding businesses..."):
        leads = scrape_leads(search_query, num_leads)
    if not leads:
        st.warning("No leads found.")
        st.stop()
    saved = 0

    saved = 0

    for lead in leads:
        insert_lead(lead, search_query, search_query)
        saved += 1
    st.success(f"{saved} leads saved to database")

    df = pd.DataFrame(leads)
    st.subheader("Preview")
    st.dataframe(df, use_container_width=True)

    # Save leads for enrichment later
    st.session_state["leads"] = leads
    for lead in leads:
        insert_lead(lead, search_query, search_query)
    df = pd.DataFrame(leads)
    st.success(f"{len(df)} leads generated!")
    st.subheader("Generated Leads")
    st.dataframe(df, use_container_width=True)


# ---------------- EMAIL ENRICHMENT ---------------- #

if st.button("🔎 Extract Emails from Websites"):

    if "leads" not in st.session_state:
        st.warning("No leads available for enrichment.")
        st.stop()

    leads = st.session_state["leads"]
    enriched = enrich_emails(leads)
    st.session_state["leads"] = enriched

    df = pd.DataFrame(enriched)

    st.success("Email enrichment completed!")
    st.dataframe(df, use_container_width=True)

    # st.dataframe(
    #     df,
    #     use_container_width=True
    # )

    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Leads CSV",
        csv,
        "leads.csv",
        "text/csv"
    )

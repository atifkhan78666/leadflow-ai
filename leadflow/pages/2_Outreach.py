import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

from database import get_unsent_leads, mark_email_sent

st.set_page_config(page_title="Email Outreach")

st.title("Outreach Campaign Manager")

# ---------------- SESSION STATE ---------------- #

if "leads_df" not in st.session_state:
    st.session_state["leads_df"] = pd.DataFrame()

# ---------------- TABS ---------------- #

tab1, tab2, tab3 = st.tabs(
    ["Lead Manager", "Campaign Builder", "Campaign Results"]
)



# ---------------- ADD LEAD DIALOG ---------------- #

@st.dialog("Add New Lead")
def add_lead_dialog():

    name = st.text_input("Business Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    website = st.text_input("Website")
    industry = st.text_input("Industry")
    location = st.text_input("Location")

    if st.button("Save Lead"):

        if not name or not email:
            st.warning("Business name and email are required.")
            return

        new_lead = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Website": website,
            "Industry": industry,
            "Location": location
        }
        df = st.session_state.get("leads_df", pd.DataFrame())
        df = pd.concat(
            [df, pd.DataFrame([new_lead])],
            ignore_index=True
        )
        st.session_state["leads_df"] = df
        st.success("Lead added successfully")

# ============================================================
# TAB 1 — LEAD MANAGER
# ============================================================

with tab1:

    st.subheader("Lead Management")

    col1, col2, col3 = st.columns(3)

    # Load scraped leads
    with col1:
        if st.button("Load Scraped Leads"):
            leads = get_unsent_leads()

            if len(leads) == 0:
                st.warning("No leads found.")
            else:
                df = pd.DataFrame(leads)

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

                st.session_state["leads_df"] = df

                st.success("Scraped leads loaded.")

    # Upload CSV
    with col2:
        file = st.file_uploader("Upload Leads CSV")

        if file:
            csv_df = pd.read_csv(file)

            st.session_state["leads_df"] = pd.concat(
                [st.session_state["leads_df"], csv_df],
                ignore_index=True
            )

            st.success("CSV leads added.")

    # Clear leads
    with col3:
        if st.button("Clear Lead List"):
            st.session_state["leads_df"] = pd.DataFrame()
            st.success("Lead list cleared.")

    st.divider()

    # Popup form
    # Add lead button
    if st.button("➕ Add Lead"):
            add_lead_dialog()

            # name = st.text_input("Business Name")
            # email = st.text_input("Email")
            # phone = st.text_input("Phone")
            # website = st.text_input("Website")
            # industry = st.text_input("Industry")
            # location = st.text_input("Location")

            if st.button("Save Lead"):

                new_lead = {
                    "Name": name,
                    "Email": email,
                    "Phone": phone,
                    "Website": website,
                    "Industry": industry,
                    "Location": location
                }

                df = st.session_state["leads_df"]

                df = pd.concat(
                    [df, pd.DataFrame([new_lead])],
                    ignore_index=True
                )

                st.session_state["leads_df"] = df

                st.success("Lead added successfully")

    st.divider()

    # Lead table
    if not st.session_state["leads_df"].empty:

        st.subheader("Lead Table")

        edited_df = st.data_editor(
            st.session_state["leads_df"],
            use_container_width=True,
            num_rows="dynamic"
        )

        st.session_state["leads_df"] = edited_df

        st.write(f"{len(edited_df)} leads ready")

    else:
        st.info("No leads available yet.")

# ============================================================
# TAB 2 — CAMPAIGN BUILDER
# ============================================================

with tab2:

    st.subheader("Create Email Campaign")

    subject = st.text_input("Email Subject")

    body = st.text_area(
        "Email Template (HTML)",
        height=250,
        value="""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Yunite Automation</title>
</head>

<body style="margin:0; padding:0; background-color:#f5f7fa; font-family:Arial, Helvetica, sans-serif;">

<table align="center" width="600" style="background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">

<!-- Header -->
<tr>
<td style="background:#0f6fff; padding:30px; text-align:center; color:#ffffff;">
<h1 style="margin:0; font-size:26px;">Yunite Automations</h1>
<p style="margin-top:8px; font-size:14px; opacity:0.9;">AI Automation for Modern Businesses</p>
</td>
</tr>

<!-- Body -->
<tr>
<td style="padding:40px; color:#333333; font-size:15px; line-height:1.6;">

<p>Hi <strong>{{Name}}</strong>,</p>

<p>
I came across your business and thought you might be interested in improving your 
<strong>online presence and customer acquisition</strong>.
</p>

<p>
At <strong>Yunite Automations</strong>, we help businesses generate more customers using 
<strong>AI-powered automation systems</strong> such as:
</p>

<ul style="padding-left:20px;">
<li>AI Lead Generation</li>
<li>Automated Outreach</li>
<li>WhatsApp & Chatbot Automation</li>
<li>Business Workflow Automation</li>
</ul>

<p>
Our solutions reduce manual work and help businesses grow faster using smart automation.
</p>

<p>
Would you be open to a <strong>quick conversation</strong> to explore how this could help your business?
</p>

<!-- CTA Button -->
<table align="center" style="margin-top:30px;">
<tr>
<td style="background:#0f6fff; padding:12px 28px; border-radius:5px;">
<a href="https://getyunite.com" style="color:#ffffff; text-decoration:none; font-weight:bold; font-size:14px;">
Visit Website
</a>
</td>
</tr>
</table>

</td>
</tr>

<!-- Footer -->
<tr>
<td style="background:#f5f7fa; padding:25px; text-align:center; font-size:13px; color:#666;">
<p style="margin:5px 0;"><strong>Mohd Atif Khan</strong></p>
<p style="margin:5px 0;">📞 +91 9643748904</p>
<p style="margin:5px 0;">🌐 getyunite.com</p>
<p style="margin:5px 0;">✉ contact@getyunite.com</p>
</td>
</tr>

</table>

</body>
</html>
"""


    )

    st.sidebar.header("SMTP Settings")

    sender_email = st.sidebar.text_input("Sender Email")
    sender_password = st.sidebar.text_input(
        "Email Password / App Password",
        type="password"
    )

    smtp_server = st.sidebar.text_input(
        "SMTP Server",
        value="smtp.gmail.com"
    )

    smtp_port = st.sidebar.number_input(
        "SMTP Port",
        value=587
    )
    df = df[df["Email"].notna()]
    if st.button("Send Campaign"):

        if st.session_state["leads_df"].empty:
            st.error("No leads available.")
            st.stop()

        if subject.strip() == "":
            st.error("Please enter a subject.")
            st.stop()

        df = st.session_state["leads_df"]

        results = []

        progress = st.progress(0)

        try:

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

        except:
            st.error("SMTP Login Failed")
            st.stop()

        for i, row in df.iterrows():

            email_body = body.replace(
                "{{Name}}",
                str(row.get("Name", "there"))
            )
            msg = MIMEText(email_body, "html")
            msg["Subject"] = subject.strip()
            msg["From"] = sender_email
            msg["To"] = row["Email"]
            status = "Failed"

            try:
                server.send_message(msg)

                if "ID" in row:
                    mark_email_sent(row["ID"])
                status = "Sent"

            except:
                status = "Failed"
            results.append({
                "Name": row.get("Name"),
                "Email": row.get("Email"),
                "Status": status
            })
            progress.progress((i + 1) / len(df))
        server.quit()
        st.session_state["campaign_results"] = pd.DataFrame(results)
        st.success("Campaign finished.")

# ============================================================
# TAB 3 — CAMPAIGN RESULTS
# ============================================================

with tab3:

    if "campaign_results" in st.session_state:
        result_df = st.session_state["campaign_results"]
        total = len(result_df)
        sent = len(result_df[result_df["Status"] == "Sent"])
        failed = len(result_df[result_df["Status"] == "Failed"])
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Leads", total)
        col2.metric("Emails Sent", sent)
        col3.metric("Failed", failed)
        st.divider()
        st.dataframe(result_df, use_container_width=True)

    else:
        st.info("No campaign results yet.")
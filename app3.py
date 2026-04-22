import streamlit as st
import gspread
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Karthic's Pro Dashboard", page_icon="📊", layout="wide")

# --- CONNECT ---
try:
    gc = gspread.oauth(
        credentials_filename='credentials.json',
        authorized_user_filename='authorized_user.json'
    )
    sh = gc.open_by_key('1y7rT5o3Gl-e3Tnm_1ZBNkhtNOMs8xKDOIAO-Rz-AsJo')
    karthic_sheet = [tab for tab in sh.worksheets() if str(tab.id) == '219188003'][0]
except Exception as e:
    st.error(f"Connection Error: {e}")

# --- APP LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.title("🚀 Work Logger")
    selected_date = st.date_input("Select Date:", datetime.now())
    today_str = selected_date.strftime("%d-%b-%Y")
    
    slot = st.selectbox("Time Slot:", [
        "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00",
        "12:00-01:00", "01:00-02:00", "02:00-03:00", "03:00-04:00", "04:00-05:00"
    ])

    options = ["Programming", "Automation", "Meeting", "Documentation", "Lunch", "Other..."]
    activity = st.selectbox("Activity:", options)
    if activity == "Other...":
        activity = st.text_input("Describe activity:")

    if st.button("Save to Sheet"):
        try:
            date_cell = karthic_sheet.find(today_str)
            time_mapping = {
                "08:00-09:00": -3, "09:00-10:00": -2, "10:00-11:00": -1,
                "11:00-12:00": 0,  "12:00-01:00": 1,  "01:00-02:00": 2,
                "02:00-03:00": 3,  "03:00-04:00": 4,  "04:00-05:00": 5
            }
            target_row = date_cell.row + time_mapping[slot]
            karthic_sheet.update_cell(target_row, 3, activity)
            st.success(f"✅ Logged to {today_str}!")
            st.balloons()
        except:
            st.error("Date not found in sheet!")

with col2:
    st.title("📈 Daily Stats")
    if st.button("Refresh Dashboard"):
        try:
            # 1. Pull the last 50 rows of data
            # Adjust range if your sheet structure is different
            data = karthic_sheet.get_all_values()
            df = pd.DataFrame(data)
            
            # 2. Filter for today's activities in Column C (Index 2)
            # This is a simple count of activities
            today_logs = df[df[0] == today_str] # Find rows for selected date
            activity_counts = df[2].value_counts().head(5) # Top 5 activities
            
            if not activity_counts.empty:
                st.write(f"Activity Distribution for {today_str}:")
                st.bar_chart(activity_counts)
            else:
                st.info("No data found for this date yet.")
        except Exception as e:
            st.write("Click 'Refresh' to load chart data.")


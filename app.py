# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt  # type: ignore
# import seaborn as sns  # type: ignore

# # Set page title and icon
# st.set_page_config(page_title="UV Index Analyzer", page_icon="🌍", layout="wide")

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .stButton button {
#         background-color: #4CAF50;
#         color: white;
#         border-radius: 5px;
#         padding: 10px 20px;
#         font-size: 16px;
#     }
#     .stButton button:hover {
#         background-color: #45a049;
#     }
#     .stHeader {
#         font-size: 2.5em;
#         font-weight: bold;
#         color: #4CAF50;
#     }
#     .stSubheader {
#         font-size: 1.5em;
#         font-weight: bold;
#         color: #2E86C1;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Title of the app
# st.markdown('<p class="stHeader">🌍 UV Index Analyzer</p>', unsafe_allow_html=True)
# st.markdown("""
# Welcome to the **UV Index Analyzer**! Analyze and visualize UV index data to understand trends and get actionable insights.
# """)

# # Sidebar for user inputs
# with st.sidebar:
#     st.markdown('<p class="stSubheader">⚙️ Input Options</p>', unsafe_allow_html=True)
#     input_method = st.radio("Choose input method:", ("Manual Input", "Upload CSV"))

#     if input_method == "Manual Input":
#         uv_data = st.text_area("Enter UV index data (comma-separated values):", "3, 5, 7, 9, 11, 8, 6, 4")
#     else:
#         uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
#         if uploaded_file:
#             st.success("File uploaded successfully!")

# # Process data based on input method
# if input_method == "Manual Input":
#     if uv_data:
#         try:
#             # Convert input to a list of floats
#             uv_values = [float(x) for x in uv_data.split(",")]
#             dates = pd.date_range(start="2023-10-01", periods=len(uv_values), freq="D")
#             data = pd.DataFrame({"Date": dates, "UV Index": uv_values})
#         except Exception as e:
#             st.error(f"Invalid input: {e}")
# else:
#     if uploaded_file:
#         try:
#             # Read CSV file
#             data = pd.read_csv(uploaded_file)
#             if "Date" not in data.columns or "UV Index" not in data.columns:
#                 st.error("CSV file must contain 'Date' and 'UV Index' columns.")
#                 st.stop()
#             data["Date"] = pd.to_datetime(data["Date"])
#         except Exception as e:
#             st.error(f"Error reading file: {e}")

# # Display data and analysis
# if 'data' in locals():
#     st.markdown('<p class="stSubheader">📊 Data Overview</p>', unsafe_allow_html=True)
#     st.write("Here's a preview of your UV index data:")
#     st.dataframe(data)

#     # Data Summary
#     st.markdown('<p class="stSubheader">📈 Data Summary</p>', unsafe_allow_html=True)
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Average UV Index", round(data["UV Index"].mean(), 2))
#     with col2:
#         st.metric("Maximum UV Index", data["UV Index"].max())
#     with col3:
#         st.metric("Minimum UV Index", data["UV Index"].min())

#     # Data Visualizations
#     st.markdown('<p class="stSubheader">📉 Data Visualizations</p>', unsafe_allow_html=True)
#     tab1, tab2, tab3 = st.tabs(["Line Chart", "Bar Chart", "Heatmap"])

#     with tab1:
#         st.write("Line Chart of UV Index Over Time")
#         st.line_chart(data.set_index("Date")["UV Index"])

#     with tab2:
#         st.write("Bar Chart of UV Index Over Time")
#         st.bar_chart(data.set_index("Date")["UV Index"])

#     with tab3:
#         st.write("Heatmap of UV Index Over Time")
#         pivot_data = data.pivot_table(index=data["Date"].dt.date, values="UV Index", aggfunc="mean")
#         plt.figure(figsize=(10, 6))
#         sns.heatmap(pivot_data, annot=True, cmap="YlOrRd", fmt=".1f")
#         st.pyplot(plt)

#     # Insights and Recommendations
#     st.markdown('<p class="stSubheader">🔍 Insights and Recommendations</p>', unsafe_allow_html=True)
#     if data["UV Index"].max() > 10:
#         st.warning("⚠️ High UV Index Detected! Wear sunscreen and avoid prolonged sun exposure.")
#     elif data["UV Index"].max() > 7:
#         st.info("🌤️ Moderate UV Index Detected! Consider wearing a hat and sunglasses.")
#     else:
#         st.success("🌥️ Low UV Index Detected! Enjoy the outdoors safely.")

#     # Filter Data
#     st.markdown('<p class="stSubheader">🔧 Filter Data</p>', unsafe_allow_html=True)
#     min_uv, max_uv = st.slider(
#         "Select UV Index Range:",
#         min_value=int(data["UV Index"].min()),
#         max_value=int(data["UV Index"].max()),
#         value=(int(data["UV Index"].min()), int(data["UV Index"].max()))
#     )  # Fixed missing closing parenthesis

#     filtered_data = data[(data["UV Index"] >= min_uv) & (data["UV Index"] <= max_uv)]
#     st.write("Filtered Data:")
#     st.dataframe(filtered_data)

#     # Download Processed Data
#     st.markdown('<p class="stSubheader">📥 Download Processed Data</p>', unsafe_allow_html=True)
#     if st.button("Download Processed Data as CSV"):
#         csv = filtered_data.to_csv(index=False)
#         st.download_button(
#             label="Download CSV",
#             data=csv,
#             file_name="processed_uv_data.csv",
#             mime="text/csv"
#         )
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import requests
import datetime

st.set_page_config(page_title="TrafficSense Dashboard", layout="wide")

# Sidebar
st.sidebar.title("TrafficSense Dashboard")
st.sidebar.markdown("### Analyze Real-Time Traffic Flow & Patterns")

# Sample Data
traffic_data = pd.DataFrame({
    "Location": ["Downtown", "Airport Road", "Highway 1", "Market Street"],
    "Congestion Level": [75, 60, 85, 50],
    "Accidents Reported": [3, 2, 5, 1],
    "Average Speed (km/h)": [30, 45, 20, 50],
    "Vehicle Count": [500, 300, 800, 250]
})

# Traffic Congestion Chart
st.subheader("Traffic Congestion Levels")
fig_congestion = px.bar(traffic_data, x="Location", y="Congestion Level", 
                        color="Congestion Level", labels={"Congestion Level": "Congestion (%)"})
st.plotly_chart(fig_congestion, use_container_width=True)

# Average Speed Chart
st.subheader("Average Speed of Vehicles")
fig_speed = px.line(traffic_data, x="Location", y="Average Speed (km/h)", 
                    markers=True, labels={"Average Speed (km/h)": "Speed (km/h)"})
st.plotly_chart(fig_speed, use_container_width=True)

# Vehicle Count Chart
st.subheader("Vehicle Count at Different Locations")
fig_vehicle = px.pie(traffic_data, names="Location", values="Vehicle Count", title="Vehicle Distribution")
st.plotly_chart(fig_vehicle, use_container_width=True)

# Geospatial Mapping
st.subheader("Accident-Prone Areas")
map_center = [37.7749, -122.4194]  # Example coordinates (San Francisco)
m = folium.Map(location=map_center, zoom_start=12)

for index, row in traffic_data.iterrows():
    folium.Marker(location=[map_center[0] + (index * 0.01), map_center[1] + (index * 0.01)],
                  popup=f"{row['Location']}\nAccidents: {row['Accidents Reported']}\nSpeed: {row['Average Speed (km/h)']} km/h\nVehicles: {row['Vehicle Count']}",
                  icon=folium.Icon(color="red" if row['Accidents Reported'] > 2 else "blue")).add_to(m)
folium_static(m)

# UV Index Data
st.sidebar.subheader("Check UV Index")
city = st.sidebar.text_input("Enter city for UV Index", "San Francisco")
if st.sidebar.button("Get UV Index"):
    uv_api_url = f"https://api.open-meteo.com/v1/forecast?latitude=37.7749&longitude=-122.4194&current=uv_index"
    response = requests.get(uv_api_url)
    if response.status_code == 200:
        uv_data = response.json()
        st.sidebar.success(f"UV Index: {uv_data['current']['uv_index']}")
    else:
        st.sidebar.error("Failed to fetch UV Index.")

# Additional Enhancements
st.sidebar.subheader("Traffic Alert Notifications")
alert_threshold = st.sidebar.slider("Set Congestion Alert Threshold (%)", 0, 100, 70)
if any(traffic_data["Congestion Level"] > alert_threshold):
    st.sidebar.warning("High congestion detected! Consider alternate routes.")
else:
    st.sidebar.success("Traffic is flowing smoothly.")

# Live Traffic Feed Simulation
st.subheader("Live Traffic Feed")
live_traffic = pd.DataFrame({
    "Timestamp": [datetime.datetime.now().strftime("%H:%M:%S")],
    "Current Traffic": ["Moderate Traffic"]
})
st.table(live_traffic)

# Weather Information
st.sidebar.subheader("Current Weather Conditions")
weather_api_url = "https://api.open-meteo.com/v1/forecast?latitude=37.7749&longitude=-122.4194&current=temperature_2m,weathercode"
response = requests.get(weather_api_url)
if response.status_code == 200:
    weather_data = response.json()
    temperature = weather_data['current']['temperature_2m']
    weather_condition = weather_data['current']['weathercode']
    st.sidebar.success(f"Temperature: {temperature}°C, Condition Code: {weather_condition}")
else:
    st.sidebar.error("Failed to fetch weather data.")

st.success("Data last updated: Just now")

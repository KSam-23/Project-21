import streamlit as st
import pandas as pd
import plotly.express as px
import time
import base64

# ---------------------------------------------
# Function to render a local GIF
# ---------------------------------------------
def render_gif(file_path):
    """Reads a local GIF file and encodes it to base64 for embedding."""
    with open(file_path, "rb") as f:
        gif_data = f.read()
    encoded_gif = base64.b64encode(gif_data).decode("utf-8")
    return f"data:image/gif;base64,{encoded_gif}"

# ---------------------------------------------
# Function to render a background image
# ---------------------------------------------
def set_background_image(image_path):
    """Sets a background image for the app."""
    with open(image_path, "rb") as f:
        bg_data = f.read()
    bg_base64 = base64.b64encode(bg_data).decode("utf-8")
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url('data:image/png;base64,{bg_base64}');
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            color: #ffffff;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Initialize session state for loading screen
if "loading_shown" not in st.session_state:
    st.session_state["loading_shown"] = False

# ---------------------------------------------
# Loading Page (Shown Once)
# ---------------------------------------------
if not st.session_state["loading_shown"]:
    gif_path = r"D:\UB_SaiKumar\Keerthi\pythonproject\second.gif"  # Update path as necessary
    loading_placeholder = st.empty()
    loading_placeholder.markdown(
        f"""
        <div style="text-align: center; margin-top: 50px;">
            <h1 style="color: #60a5fa; font-size: 3rem; animation: fadeIn 2s;">🎮 Loading Your Gaming Dashboard... 🎮</h1>
            <div style="margin-top: 20px; animation: fadeIn 4s;">
                <img src="{render_gif(gif_path)}" alt="Loading GIF" style="width: 400px; border-radius: 10px;"/>
            </div>
            <h4 style="color: #d1d5db; margin-top: 20px; animation: fadeIn 6s;">"Hang tight, data magic is happening! 😂"</h4>
        </div>
        <style>
            @keyframes fadeIn {{
                0% {{ opacity: 0; }}
                100% {{ opacity: 1; }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(4)  # Simulate longer loading time
    loading_placeholder.empty()
    st.session_state["loading_shown"] = True  # Mark loading as shown

    # Set the background image after loading
    background_image_path = r"D:\UB_SaiKumar\Keerthi\pythonproject\converted_image.png"
    set_background_image(background_image_path)

# ---------------------------------------------
# Hero Section
# ---------------------------------------------
# Set the background image after loading
background_image_path = r"D:\UB_SaiKumar\Keerthi\pythonproject\converted_image.png"
set_background_image(background_image_path)

st.markdown(
    """
    <div class="hero-container">
        <h1>Welcome to the Ultimate Gaming Dashboard! 🎮</h1>
        <p>Explore insights, trends, and epic gaming data adventures!</p>
        <p class="tagline">"Remember, a dashboard a day keeps bad decisions away!"</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------
# Load Data
# ---------------------------------------------
data_path = r"D:\UB_SaiKumar\Keerthi\pythonproject\vgsales.csv"
data = pd.read_csv(data_path)
data.dropna(subset=["Year", "Publisher"], inplace=True)
data["Year"] = data["Year"].astype(int)

# Filters Section
st.markdown("<h2>🎯 Filters: Tailor Your View</h2>", unsafe_allow_html=True)
genre_filter = st.multiselect("Genre(s)", options=sorted(data["Genre"].unique()))
platform_filter = st.multiselect("Platform(s)", options=sorted(data["Platform"].unique()))
year_filter = st.slider("Year Range", min_value=int(data["Year"].min()), max_value=int(data["Year"].max()), value=(2000, 2015))

filtered_data = data[
    (data["Genre"].isin(genre_filter) if genre_filter else data["Genre"].notnull()) &
    (data["Platform"].isin(platform_filter) if platform_filter else data["Platform"].notnull()) &
    (data["Year"].between(year_filter[0], year_filter[1]))
]

# ---------------------------------------------
# KPI Section
# ---------------------------------------------
st.markdown("<h2>🏆 Key Metrics</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
total_sales = filtered_data["Global_Sales"].sum() if not filtered_data.empty else 0
top_genre = filtered_data.groupby("Genre")["Global_Sales"].sum().idxmax() if not filtered_data.empty else "N/A"
best_selling_game = filtered_data.loc[filtered_data["Global_Sales"].idxmax(), "Name"] if not filtered_data.empty else "N/A"

with col1:
    st.markdown(f"<div class='kpi-box'><div class='kpi-label'>Total Global Sales</div><div class='kpi-value'>{total_sales:.2f}M</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-box'><div class='kpi-label'>Top Genre</div><div class='kpi-value'>{top_genre}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-box'><div class='kpi-label'>Best Game</div><div class='kpi-value'>{best_selling_game}</div></div>", unsafe_allow_html=True)

# ---------------------------------------------
# Charts Section
# ---------------------------------------------
st.markdown("<h2>📊 Visual Insights</h2>", unsafe_allow_html=True)

if not filtered_data.empty:
    # Sales by Year
    sales_by_year = filtered_data.groupby("Year")["Global_Sales"].sum().reset_index()
    fig_year = px.line(sales_by_year, x="Year", y="Global_Sales", title="Global Sales Over the Years", markers=True)
    st.plotly_chart(fig_year, use_container_width=True)

    # Average Sales by Genre
    avg_sales_genre = filtered_data.groupby("Genre")["Global_Sales"].mean().reset_index()
    fig_genre = px.bar(avg_sales_genre, x="Genre", y="Global_Sales", title="Average Sales by Genre", color="Genre")
    st.plotly_chart(fig_genre, use_container_width=True)

    # Heatmap
    sales_columns = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
    correlation = filtered_data[sales_columns].corr()
    fig_corr = px.imshow(correlation, text_auto=True, title="Regional Sales Correlation")
    st.plotly_chart(fig_corr, use_container_width=True)

else:
    st.write("No data available for the selected filters. 🎮")

# ---------------------------------------------
# Footer
# ---------------------------------------------
st.markdown("<div class='footer'>Made with ❤️ by Team 21. Explore more at <a href='#'>www.gaminginsights.com</a>.</div>", unsafe_allow_html=True)
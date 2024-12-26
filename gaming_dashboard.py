import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import base64
import os

# ---------------------------------------------
# Function to encode local GIF or MP4
# ---------------------------------------------
def render_local_file(file_path):
    try:
        if not os.path.isfile(file_path):
            st.error(f"File not found: {file_path}. Please verify the file path and try again.")
            return ""

        with open(file_path, "rb") as f:
            file_data = f.read()

        if file_path.endswith(".gif"):
            mime_type = "image/gif"
        elif file_path.endswith((".jpg", ".jpeg", ".png")):
            mime_type = "image/png"
        else:
            st.error(f"Unsupported file type for {file_path}. Only GIF and image formats (JPG, PNG) are supported.")
            return ""

        encoded_data = f"data:{mime_type};base64,{base64.b64encode(file_data).decode('utf-8')}"
        return encoded_data

    except Exception as e:
        st.error(f"An error occurred while encoding the file {file_path}: {e}")
        return ""



# ---------------------------------------------
# Function to Encode Images for Background
# ---------------------------------------------
def encode_image(image_path):
    """Encodes an image to base64."""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# ---------------------------------------------
# Background Image Slideshow
# ---------------------------------------------
def add_background_slideshow():
    img1 = encode_image("p1.jpg")
    img2 = encode_image("p2.jpg")
    img3 = encode_image("p3.jpg")
    img4 = encode_image("p4.jpg")
    img5 = encode_image("p5.jpg")

    st.markdown(f"""
    <style>
        body {{
            margin: 0;
            padding: 0;
            height: 100%;
            background-size: cover;
            background-repeat: no-repeat;
            animation: slideShow 25s infinite;
        }}
        @keyframes slideShow {{
            0% {{ background-image: url('data:image/jpg;base64,{img1}'); }}
            20% {{ background-image: url('data:image/jpg;base64,{img2}'); }}
            40% {{ background-image: url('data:image/jpg;base64,{img3}'); }}
            60% {{ background-image: url('data:image/jpg;base64,{img4}'); }}
            80% {{ background-image: url('data:image/jpg;base64,{img5}'); }}
            100% {{ background-image: url('data:image/jpg;base64,{img1}'); }}
        }}
        .stApp {{
            background: transparent;
            height: 100%;
        }}
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------
# Filter Section
# ---------------------------------------------
def display_filter_section(data):
    st.markdown(
        """
        <style>
        .stSelectbox > label, .stSlider > label, .stMultiSelect > label {
            font-size: 30px !important;  /* Font size */
            font-weight: bold !important;
            color: #FFFFFF !important;  /* Font color */
            background-color: #39a0ca !important;  /* Light sky blue */
            padding: 10px 15px;  /* Padding */
            border-radius: 5px;  /* Rounded corners */
            font-family: Arial, sans-serif; /* Font style */
        }
        .stSelectbox, .stSlider, .stMultiSelect {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 10px !important;
        }

    
        /* Styling for selected options in filters */
        .stMultiSelect div[data-baseweb="tag"] {
            background-color: rgb(46, 46, 136) !important; /* Dark navy blue */
            color: #FFFFFF !important; /* White text color for better contrast */
            border-radius: 5px; /* Rounded corners */
            padding: 5px 10px; /* Spacing for the selected items */
            font-size: 16px; /* Font size */
            font-weight: bold; /* Bold font */
        }
        .filter-container {
            display: flex;
            background-color:rgb(46, 46, 136) !important;  /* dark navy blue */
            justify-content: space-between;
            gap: 20px;

        }
        .filter-container > div {
            flex: 1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Genre and Platform filters in two columns
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        genres = st.multiselect("Select Genre(s):",  options=data["Genre"].unique(), key="filter_genres_unique"  ) # Unique key for genres 
    with col2:
        platforms = st.multiselect( "Select Platform(s):", options=data["Platform"].unique(),key="filter_platforms_unique") # Unique key for platforms
    st.markdown('</div>', unsafe_allow_html=True)

    # Publisher filter
    publishers = st.multiselect("Select Publisher(s): (Optional)", options=data["Publisher"].unique(),key="filter_publishers_unique"  # Unique key for publishers
    )

    # Year range filter
    year_min = int(data["Year"].min())
    year_max = int(data["Year"].max())
    year_range = st.slider(
        "Select Year Range:",
        min_value=year_min,
        max_value=year_max,
        value=(2000,2020),
        key="filter_year_range_unique"  # Unique key for year range
    )
    # Create boolean filters
    genre_filter = data["Genre"].isin(genres) if genres else pd.Series([True] * len(data), index=data.index)
    platform_filter = data["Platform"].isin(platforms) if platforms else pd.Series([True] * len(data), index=data.index)
    publisher_filter = data["Publisher"].isin(publishers) if publishers else pd.Series([True] * len(data), index=data.index)
    year_filter = data["Year"].between(year_range[0], year_range[1])

    # Combine filters
    combined_filter = genre_filter & platform_filter & publisher_filter & year_filter
    filtered_data = data[combined_filter]

    # Determine if filters are applied (genre or platform must be selected)
    filters_applied = bool(genres or platforms)

    # Determine if filters were applied
    #filters_applied = bool(genres or platforms or publishers or year_range != (year_min, year_max))

    return filtered_data,filters_applied


# ---------------------------------------------
# Display Title Block with Hover Effect
# ---------------------------------------------
def display_title_in_left_block():
    """Displays the title block with letter-by-letter animation and words on new lines."""
    
    st.markdown(
        """
        <style>
            /* Title block styling */
            .title-block {
                background-color: black;
                color: white;
                width: 90%;
                height: 110vh;
                padding: 20px;
                text-align: center;
                border-radius: 10px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }

            /* Title animation */
            @keyframes slide-in {
                0% { opacity: 0; transform: translateY(-30px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            .animated-title {
                font-size: 40px;
                font-weight: bold;
                font-family: 'Arial Black', Gadget, sans-serif;
                color: white;
                line-height: 1.5; /* Spacing between lines */
                text-align: center;
            }

            .animated-title span {
                display: inline-block;
                opacity: 0;
                animation: slide-in 0.8s ease-in-out forwards;
            }

            /* Letter-by-letter delays */
            .animated-title span:nth-child(1) { animation-delay: 0.3s; }
            .animated-title span:nth-child(2) { animation-delay: 0.6s; }
            .animated-title span:nth-child(3) { animation-delay: 0.9s; }
            .animated-title span:nth-child(4) { animation-delay: 1.2s; }
            .animated-title span:nth-child(5) { animation-delay: 1.5s; }
            .animated-title span:nth-child(6) { animation-delay: 1.8s; }
            .animated-title span:nth-child(7) { animation-delay: 2.1s; }
            .animated-title span:nth-child(8) { animation-delay: 2.4s; }
            .animated-title span:nth-child(9) { animation-delay: 2.7s; }
            .animated-title span:nth-child(10) { animation-delay: 3.0s; }
            .animated-title span:nth-child(11) { animation-delay: 3.3s; }

            /* Subtitle animation */
            @keyframes fade-in {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            

            .subtitle {
                font-size: 20px;
                font-family: 'Georgia', serif;
                color: #FFFFFF;
                margin-top: 20px;
                opacity: 0;
                animation: fade-in 2s ease-in-out forwards;
                animation-delay: 2s; /* Delay after title animation */
            }
        </style>
        
        <div class="title-block">
            <div class="animated-title">
                <div>
                    <span>I</span><span>N</span><span>T</span><span>E</span><span>R</span><span>A</span><span>C</span><span>T</span><span>I</span><span>V</span><span>E</span>
                </div>
                <div>
                    <span>G</span><span>A</span><span>M</span><span>I</span><span>N</span><span>G</span>
                </div>
                <div>
                    <span>D</span><span>A</span><span>S</span><span>H</span><span>B</span><span>O</span><span>A</span><span>R</span><span>D</span>
                </div>
            </div>
            <div class="subtitle">Welcome to the gaming world!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------
# Enhanced Layout
# ---------------------------------------------
def enhanced_layout(data):
    """Enhanced layout with title block and visualizations."""
    col1, col2 = st.columns([1, 2])  # 1:2 ratio for left and right sections

    with col1:
        # Title block at the top-left
        display_title_in_left_block()

        # GIFs below the title block
        display_gif_carousel()

    with col2:
        # Add an empty space at the top to leave the right side of the title block empty
        st.markdown("<div style='height: 110vh;'></div>", unsafe_allow_html=True)

        # Filters and visualizations below the empty space
        filtered_data, filters_applied = display_filter_section(data)



        if filters_applied:
            display_visualizations(filtered_data)
                    # Display insights at the top
            display_gaming_insights(filtered_data)

        else:

            st.markdown(
                """
                <div class="animated-text">
                    <span>S</span><span>e</span><span>l</span><span>e</span><span>c</span><span>t</span>
                    <span> </span><span>f</span><span>i</span><span>l</span><span>t</span><span>e</span><span>r</span><span>s</span>
                    <span> </span><span>a</span><span>b</span><span>o</span><span>v</span><span>e</span>
                    <span> </span><span>t</span><span>o</span>
                    <span> </span><span>v</span><span>i</span><span>e</span><span>w</span>
                    <span> </span><span>g</span><span>a</span><span>m</span><span>i</span><span>n</span><span>g</span>
                    <span> </span><span>a</span><span>n</span><span>a</span><span>l</span><span>y</span><span>t</span><span>i</span><span>c</span><span>s</span>.
                </div>
                <style>
                    .animated-text {
                        display: inline-block;
                        font-size: 30px;
                        font-weight: bold;
                        color: white;
                        
                        font-family: 'Arial', sans-serif;
                    }

                    .animated-text span {
                        opacity: 0;
                        display: inline-block;
                        transform: translateY(20px);
                        animation: slide-in 1s forwards;
                    }

                    /* Delays for each letter, starting from 3 seconds */
                    .animated-text span:nth-child(1) { animation-delay: 3.1s; }
                    .animated-text span:nth-child(2) { animation-delay: 3.2s; }
                    .animated-text span:nth-child(3) { animation-delay: 3.3s; }
                    .animated-text span:nth-child(4) { animation-delay: 3.4s; }
                    .animated-text span:nth-child(5) { animation-delay: 3.5s; }
                    .animated-text span:nth-child(6) { animation-delay: 3.6s; }
                    .animated-text span:nth-child(7) { animation-delay: 3.7s; }
                    .animated-text span:nth-child(8) { animation-delay: 3.8s; }
                    .animated-text span:nth-child(9) { animation-delay: 3.9s; }
                    .animated-text span:nth-child(10) { animation-delay: 4.0s; }
                    .animated-text span:nth-child(11) { animation-delay: 4.1s; }
                    .animated-text span:nth-child(12) { animation-delay: 4.2s; }
                    .animated-text span:nth-child(13) { animation-delay: 4.3s; }
                    .animated-text span:nth-child(14) { animation-delay: 4.4s; }
                    .animated-text span:nth-child(15) { animation-delay: 4.5s; }
                    .animated-text span:nth-child(16) { animation-delay: 4.6s; }
                    .animated-text span:nth-child(17) { animation-delay: 4.7s; }
                    .animated-text span:nth-child(18) { animation-delay: 4.8s; }
                    .animated-text span:nth-child(19) { animation-delay: 4.9s; }
                    .animated-text span:nth-child(20) { animation-delay: 5.0s; }
                    .animated-text span:nth-child(21) { animation-delay: 5.1s; }
                    .animated-text span:nth-child(22) { animation-delay: 5.2s; }
                    .animated-text span:nth-child(23) { animation-delay: 5.3s; }
                    .animated-text span:nth-child(24) { animation-delay: 5.4s; }
                    .animated-text span:nth-child(25) { animation-delay: 5.5s; }
                    .animated-text span:nth-child(26) { animation-delay: 5.6s; }
                    .animated-text span:nth-child(27) { animation-delay: 5.7s; }
                    .animated-text span:nth-child(28) { animation-delay: 5.8s; }
                    .animated-text span:nth-child(29) { animation-delay: 5.9s; }
                    .animated-text span:nth-child(30) { animation-delay: 6.0s; }
                    .animated-text span:nth-child(31) { animation-delay: 6.1s; }
                    .animated-text span:nth-child(32) { animation-delay: 6.2s; }
                    .animated-text span:nth-child(33) { animation-delay: 6.3s; }
                    .animated-text span:nth-child(34) { animation-delay: 6.4s; }
                    .animated-text span:nth-child(35) { animation-delay: 6.5s; }
                    .animated-text span:nth-child(36) { animation-delay: 6.6s; }
                    .animated-text span:nth-child(37) { animation-delay: 6.7s; }
                    .animated-text span:nth-child(38) { animation-delay: 6.8s; }
                    .animated-text span:nth-child(39) { animation-delay: 6.9s; }
                    .animated-text span:nth-child(40) { animation-delay: 7.0s; }
                    .animated-text span:nth-child(41) { animation-delay: 7.1s; }
                    .animated-text span:nth-child(42) { animation-delay: 7.2s; }
                    .animated-text span:nth-child(43) { animation-delay: 7.3s; }
                    .animated-text span:nth-child(44) { animation-delay: 7.4s; }
                    .animated-text span:nth-child(45) { animation-delay: 7.5s; }

                    @keyframes slide-in {
                        from {
                            opacity: 0;
                            transform: translateY(20px);
                        }
                        to {
                            opacity: 1;
                            transform: translateY(0);
                        }
                    }
                </style>
                """,
                unsafe_allow_html=True,
            )




# ---------------------------------------------
# GIF Display
# ---------------------------------------------
def display_gif_carousel():

    """Displays a carousel of GIFs."""
    gifs = [
        "g12.gif",  # Sixth GIF
        "g10.gif",  # Sixth GIF
        "g11.gif",  # Second GIF
        "g14.gif",  # Third GIF
    ]
    
    # Add CSS for animations
    st.markdown("""
    <style>
        .gif-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            gap: 100px; /* Adds proper spacing between GIFs */
            margin-top: 20px; /* Adjusts top margin */
            width: 70%; /* Ensures container takes full width */
        }
        .gif-item {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .gif-item img {
            width: 100px; /* Consistent width for all GIFs */
            height: 100px; /* Fixed height for uniformity */
            border-radius: 10px; /* Adds rounded corners */

            animation: zoom-in-out 3s ease-in-out infinite; /* Adds zoom animation */
        }
        @keyframes zoom-in-out {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        
        }
    </style>
    """, unsafe_allow_html=True)

    # Display GIFs with the applied animation
    st.markdown("<div class='gif-container'>", unsafe_allow_html=True)
    for gif in gifs:
        gif_data = render_local_file(gif)
        if gif_data:
            st.markdown(
                f"""
                <div class="gif-item">
                    <img src="{gif_data}" alt="GIF"/>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------
# Data Preprocessing
# ---------------------------------------------
@st.cache_data
def preprocess_data(file_path):
    """Loads and preprocesses the data."""
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()
    if "Global_Sales" not in data.columns:
        data["Global_Sales"] = data[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum(axis=1)
    data.dropna(subset=["Year", "Publisher"], inplace=True)
    data["Year"] = data["Year"].astype(int)
    return data

# ---------------------------------------------
# Function to encode local images to base64
# ---------------------------------------------
def encode_image(image_path):
    """Encodes an image to base64."""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# ---------------------------------------------
import streamlit as st
import plotly.express as px
import pandas as pd
from matplotlib import cm

# Custom color palette to match the background tones
COLOR_PALETTE = ["#6a0dad", "#7f00ff", "#cc99ff", "#4b0082", "#6600cc"]

# Function to display graphs in a grid layout
def display_visualizations(filtered_data):
    """Displays charts with a light color palette and animated headings."""
    st.markdown(
        """
        <style>
        /* Heading animation */
        @keyframes slide-in-left {
            0% {
                opacity: 0;
                transform: translateX(-100%);
            }
            100% {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .graph-heading {
            font-size: 24px;
            font-weight: bold;
            color: white;
            text-align: center;
            background-color: rgba(0, 0, 0, 0.7); /* Black background for visibility */
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
            animation: slide-in-left 1s ease-out;
            animation-delay: 1.5s;
            animation-fill-mode: forwards;
            opacity: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if not filtered_data.empty:
        # Create columns for a 2x2 grid layout
        col1, col2 = st.columns(2)

        with col1:
            # Sales over time
            st.markdown('<div class="graph-heading">Global Sales Over Time</div>', unsafe_allow_html=True)
            sales_by_year = filtered_data.groupby("Year")["Global_Sales"].sum().reset_index()
            fig_year = px.line(
                sales_by_year,
                x="Year",
                y="Global_Sales",
                title="",
                markers=True,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(fig_year, use_container_width=True)

            # Average Global Sales by Year (Matplotlib & Seaborn)
            st.markdown('<div class="graph-heading">Average Sales Per Year</div>', unsafe_allow_html=True)
            avg_sales_by_year = filtered_data.groupby("Year")["Global_Sales"].mean().reset_index()
            plt.figure(figsize=(10, 5))
            sns.barplot(
                x="Year",
                y="Global_Sales",
                data=avg_sales_by_year,
                palette="Purples",
            )
            plt.title("Average Sales Per Year", fontsize=18, pad=20, color="black")
            plt.xlabel("Year", fontsize=14)
            plt.ylabel("Average Sales (in millions)", fontsize=14)
            plt.xticks(rotation=45)
            st.pyplot(plt)

        with col2:
            # Sales by genre
            st.markdown('<div class="graph-heading">Total Sales by Genre</div>', unsafe_allow_html=True)
            sales_by_genre = filtered_data.groupby("Genre")["Global_Sales"].sum().reset_index()
            fig_genre = px.bar(
                sales_by_genre,
                x="Genre",
                y="Global_Sales",
                title="",
                color="Genre",
                color_discrete_sequence=px.colors.sequential.Blues,
            )
            st.plotly_chart(fig_genre, use_container_width=True)

            # Pie Chart for Publishers by Genre
            st.markdown('<div class="graph-heading">Publishers by Genre</div>', unsafe_allow_html=True)
            publishers_by_genre = filtered_data.groupby("Genre")["Publisher"].nunique().reset_index()
            publishers_by_genre.columns = ["Genre", "Publisher_Count"]
            fig_pie = px.pie(
                publishers_by_genre,
                names="Genre",
                values="Publisher_Count",
                title="",
                color_discrete_sequence=px.colors.sequential.Blues,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

def display_gaming_insights(filtered_data):
    """Displays key gaming insights in a center-aligned styled black box with creative transition."""
    # Calculate insights
    total_sales = filtered_data["Global_Sales"].sum()
    top_genre = filtered_data.groupby("Genre")["Global_Sales"].sum().idxmax()
    best_selling_game = filtered_data.loc[filtered_data["Global_Sales"].idxmax(), "Name"]

    # Black box styling and creative transition
    st.markdown(
        f"""
        <style>
        .insights-box {{
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 24px;
            font-weight: bold;
            line-height: 1.8;
            text-align: center;
            padding: 30px;
            border-radius: 15px;
            margin: 50px auto;
            max-width: 600px;
            box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.5);
            animation: slideDown 1.5s ease-in-out;
        }}

        /* Creative slide-down transition */
        @keyframes slideDown {{
            0% {{ opacity: 0; transform: translateY(-50px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>

        <div class="insights-box">
            <p>Key Insights</p>
            <p>- <b>Total Global Sales:</b> {total_sales:.2f}M</p>
            <p>- <b>Top Genre:</b> {top_genre}</p>
            <p>- <b>Best-Selling Game:</b> {best_selling_game}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------
# Main Application
# ---------------------------------------------
def main():
    st.set_page_config(page_title="Interactive Gaming Dashboard", layout="wide")
    add_background_slideshow()
    # Load and preprocess data
    file_path = "vgsales.csv"  # Update with your dataset path
    data = preprocess_data(file_path)
    # Display layout
    enhanced_layout(data)    
if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
data_path = "C:/Users/VIJAYA/Downloads/vgsales.csv"  # Update with your dataset path
data = pd.read_csv(data_path)

# Clean and preprocess the data
data.dropna(subset=["Year", "Publisher"], inplace=True)
data["Year"] = data["Year"].astype(int)

# Sidebar Filters
st.sidebar.header("Filters")
genre_filter = st.sidebar.multiselect("Select Genre", data["Genre"].unique(), default=data["Genre"].unique())
platform_filter = st.sidebar.multiselect("Select Platform", data["Platform"].unique(), default=data["Platform"].unique())
year_filter = st.sidebar.slider("Select Year Range", int(data["Year"].min()), int(data["Year"].max()), (2000, 2015))

# Filter data based on selections
filtered_data = data[
    (data["Genre"].isin(genre_filter)) &
    (data["Platform"].isin(platform_filter)) &
    (data["Year"].between(year_filter[0], year_filter[1]))
]

# Main Dashboard
st.title("Video Game Sales Dashboard")
st.markdown("Explore trends, sales, and insights in the video game industry.")

# Key Performance Indicators
st.header("Key Metrics")
total_sales = filtered_data["Global_Sales"].sum()
top_genre = filtered_data.groupby("Genre")["Global_Sales"].sum().idxmax()
top_game = filtered_data.loc[filtered_data["Global_Sales"].idxmax(), "Name"]

st.metric("Total Global Sales", f"{total_sales:.2f} million")
st.metric("Top Genre", top_genre)
st.metric("Best-Selling Game", top_game)

# Sales Trends by Year
st.header("Sales Trends by Year")
sales_by_year = filtered_data.groupby("Year")["Global_Sales"].sum().reset_index()
fig1 = px.line(sales_by_year, x="Year", y="Global_Sales", title="Global Sales Over the Years")
st.plotly_chart(fig1)

# Average Sales by Genre
st.header("Average Sales by Genre")
avg_sales_genre = filtered_data.groupby("Genre")["Global_Sales"].mean().reset_index()
fig2 = px.bar(avg_sales_genre, x="Genre", y="Global_Sales", title="Average Sales by Genre", color="Genre")
st.plotly_chart(fig2)

# Correlation Heatmap
st.header("Correlation Analysis")
sales_columns = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
correlation = filtered_data[sales_columns].corr()
fig3 = px.imshow(correlation, text_auto=True, title="Correlation Heatmap")
st.plotly_chart(fig3)

# Top Publishers
st.header("Top Publishers by Number of Games")
top_publishers = (
    filtered_data.groupby("Publisher")["Name"].count().reset_index().sort_values("Name", ascending=False).head(10)
)
fig4 = px.bar(top_publishers, x="Publisher", y="Name", title="Top Publishers by Number of Games")
st.plotly_chart(fig4)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by Group 21")






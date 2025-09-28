import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Amazon Music Clustering 🎶", layout="wide")

# -----------------------
# Add Music Theme CSS
# -----------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(120deg, #1DB954 0%, #191414 100%);
        color: white;
    }
    .stApp {
        background-color: #121212;
    }
    h1, h2, h3, h4 {
        color: #1DB954;
    }
    .css-1d391kg {  /* Sidebar */
        background: #191414 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Load clustered dataset
# -----------------------
@st.cache_data
def load_data():
    file_path = "../reports/amazon_music_clusters.csv"
    if not os.path.exists(file_path):
        st.error("❌ Clustered dataset not found. Please run 03_clustering_kmeans.ipynb first.")
        return None
    return pd.read_csv(file_path)

df = load_data()

if df is not None:
    st.title("🎵 Amazon Music Clustering Dashboard")
    st.markdown("Discover your music clusters like a **DJ mixing tracks** 🎧")

    # -----------------------
    # Cluster Selection
    # -----------------------
    clusters = sorted(df['cluster'].unique())
    cluster_choice = st.sidebar.selectbox("🎯 Select Cluster", clusters)

    sub_df = df[df['cluster'] == cluster_choice]

    st.markdown(f"### 📊 Cluster {cluster_choice} Overview")
    st.success(f"🎶 Number of songs in this cluster: **{len(sub_df)}**")

    # -----------------------
    # Cluster Distribution Pie
    # -----------------------
    st.markdown("### 🍩 Cluster Distribution of Songs")
    cluster_counts = df['cluster'].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]
    fig_pie = px.pie(cluster_counts, names="Cluster", values="Count",
                     color="Cluster", hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Bold)
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

    # -----------------------
    # PCA Scatter Plot
    # -----------------------
    if "pc1" in df.columns and "pc2" in df.columns:
        st.markdown("### 🌈 Clusters in PCA Projection")
        fig = px.scatter(
            df, x="pc1", y="pc2", color="cluster",
            hover_data=["name_song", "name_artists"],
            title="2D Projection of Music Clusters 🎼",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_traces(marker=dict(size=8, opacity=0.7, symbol="circle"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ PCA features not found. Please run 04_cluster_profiling.ipynb to generate pc1, pc2.")

    # -----------------------
    # Show Top Songs in Cluster
    # -----------------------
    st.markdown("### 🎤 Example Songs in this Cluster")
    st.dataframe(sub_df[["name_song", "name_artists", "danceability", "energy"]].head(20))

    # -----------------------
    # Cluster Feature Means with Interactive Dropdown
    # -----------------------
    features = [
        'danceability','energy','loudness','speechiness',
        'acousticness','instrumentalness','liveness','valence',
        'tempo','duration_ms'
    ]

    cluster_profile = df.groupby("cluster")[features].mean().reset_index()

    st.markdown("### 🎨 Interactive Feature Comparison")

    # ✅ Multiselect Dropdown
    selected_features = st.multiselect(
        "Select features to visualize 🎼:",
        options=features,
        default=["danceability","energy","valence"]
    )

    if selected_features:
        # Melt only selected features into long format
        cluster_profile_long = cluster_profile.melt(
            id_vars="cluster",
            value_vars=selected_features,
            var_name="Feature",
            value_name="Mean Value"
        )

        # Colorful bar chart
        fig2 = px.bar(
            cluster_profile_long,
            x="Feature", y="Mean Value",
            color="cluster", barmode="group",
            title="📊 Average Feature Values per Cluster",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig2.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor="#191414",
            font=dict(size=14, color="white"),
            legend_title="Cluster",
            hovermode="x unified"
        )

        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("⚠️ Please select at least one feature to display the bar chart.")

# 🎶 Amazon Music Clustering – Final Report

## 1. Project Overview
We clustered ~95,000 songs using audio features (danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms) to discover hidden groupings and enable playlist curation.

---

## 2. Methodology
- **Data Exploration**: Checked distributions, correlations, and outliers.
- **Preprocessing**: Applied log-transform on `duration_ms`, standardized features.
- **Clustering**: Used KMeans with optimal k determined by Elbow + Silhouette.
- **Evaluation Metrics**: Silhouette Score, Davies-Bouldin Index.
- **Profiling**: Analyzed average feature values per cluster.

---

## 3. Results
- **Best k**: 4 (chosen after elbow + silhouette analysis).
- **Cluster Profiles** (high-level interpretation):
  - **Cluster 0**: High danceability, high energy → *Party/Dance tracks*
  - **Cluster 1**: High acousticness, low energy → *Acoustic/Chill tracks*
  - **Cluster 2**: High instrumentalness → *Instrumental/Background tracks*
  - **Cluster 3**: Medium energy, high valence → *Feel-good/Pop tracks*

- **Cluster sizes**: (fill in from `df['cluster'].value_counts()`)

---

## 4. Visualizations
- Elbow method & Silhouette plots
- PCA 2D scatter plot of clusters
- Heatmap of feature means per cluster
- Bar chart of cluster sizes

---

## 5. Deliverables
- `amazon_music_clusters.csv` → Dataset with cluster labels
- `cluster_profile.csv` → Cluster summary stats
- `kmeans_model.pkl` → Saved clustering model
- `scaler.pkl` → Saved StandardScaler
- `slides.pdf` → Presentation slides
- `final_report.md` → This document

---

## 6. Conclusion
The clustering successfully separated tracks into musically meaningful groups. These results can support playlist curation, recommendation systems, and music analytics.


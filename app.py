import streamlit as st
import pandas as pd

st.title(
    "DSS Beach Club Bali"
)

df = pd.read_csv(
    "dataset.csv"
)

st.dataframe(df)

st.subheader(
    "Top Beach Club"
)

top = df.sort_values(
    by="Rating",
    ascending=False
)

st.dataframe(top.head(10))

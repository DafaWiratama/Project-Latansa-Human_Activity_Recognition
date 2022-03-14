import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")


@st.cache
def load_data():
    return pd.read_csv("dataset.csv")


df = load_data().copy()

df.replace(to_replace="STAND2SIT", value="STAND", inplace=True)
df.replace(to_replace="SIT2SLEEP", value="SIT", inplace=True)
df.replace(to_replace="SLEEP2SIT", value="SLEEP", inplace=True)
df.replace(to_replace="SIT2STAND", value="SIT", inplace=True)
df.replace(to_replace="STAND2SLEEP", value="STAND", inplace=True)
df.replace(to_replace="SLEEP2STAND", value="SLEEP", inplace=True)

lower_bound, upper_bound = st.sidebar.slider("Select Range", 0, len(df), (0, len(df)), step=1)
lower_bound, upper_bound = int(lower_bound), int(upper_bound)

n_sample = st.sidebar.slider("Select Range", 1, 1024, step=1, value=256)
n_skip = st.sidebar.slider("N-Skip", 1, 256, step=1, value=25)

df = df[lower_bound:upper_bound]


_df = df.rolling(n_sample).mean()
_df["state"] = df.state


# Reduce the number of rows by averaging and resample for every 10th row
aa = []
for i in range(0, len(_df), n_skip):
    aa.append(_df.iloc[i])

columns = _df.columns
states = _df.state.unique()
_df = pd.DataFrame(aa)
_df.columns = columns


for label in ["accelerometer_x", "accelerometer_y", "accelerometer_z", "gyroscope_x", "gyroscope_y", "gyroscope_z"]:
    data = _df[label]

    # Normalize data into -1 to 1 range
    data = (data - data.min()) / (data.max() - data.min())

    fig = px.scatter(y=data, color=_df.state, labels=states,  title=label)
    fig.update_traces(marker_size=3)
    st.plotly_chart(fig, use_container_width=True)


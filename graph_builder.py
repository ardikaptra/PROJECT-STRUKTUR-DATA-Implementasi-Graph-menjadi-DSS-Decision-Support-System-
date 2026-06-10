import pandas as pd

def build_graph():

    df = pd.read_csv("dataset.csv")

    graph = {
        "START":{}
    }

    for _,row in df.iterrows():

        score = (

            row["Harga"] * 0.3 +

            row["Jarak"] * 0.1 +

            ((100 - row["Rating"]*20) * 0.4) +

            ((100 - row["Fasilitas"]) * 0.2)

        )

        graph["START"][row["BeachClub"]] = round(score,2)

        graph[row["BeachClub"]] = {}

    return graph

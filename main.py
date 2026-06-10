from dijkstra import dijkstra
from path import shortest_path

graph = {

    "Start":{

        "La Brisa":3,
        "Atlas":4,
        "Finns":5,
        "Potato Head":7,
        "Savaya":15
    },

    "La Brisa":{
        "Atlas":1,
        "Finns":2
    },

    "Atlas":{
        "Mari":1,
        "Cafe Del Mar":2
    },

    "Finns":{
        "Cafe Del Mar":1
    },

    "Potato Head":{
        "Savaya":5
    },

    "Mari":{},
    "Cafe Del Mar":{},
    "Savaya":{}
}

hasil = dijkstra(graph,"Start")

print("\n=== DSS BEACH CLUB BALI ===\n")

for club, skor in hasil.items():
    print(club, ":", skor)

cost, path = shortest_path(
    graph,
    "Start",
    "Cafe Del Mar"
)

print("\nJalur Terbaik:")
print(path)

print("\nTotal Cost:")
print(cost)

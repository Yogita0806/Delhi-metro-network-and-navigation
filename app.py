
import json
import streamlit as st
import folium
import networkx as nx
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

# Read the adjacency list and other relevant data from JSON files
with open('all_lines.json', 'r') as fp:
    all_lines = json.load(fp)

with open('Name_To_Node.json', 'r') as fp:
    Name_To_Node = json.load(fp)

with open('adj_list.json', 'r') as fp:
    adj_list = json.load(fp)


# Format : adj_list = {'Dwarka Sector 21': [['Dwarka Sector 8', 1.7], ['IGI Airport', 2.9]], 'Dwarka Sector 8': [['Dwarka Sector 21', 1.7], ['Dwarka Sector 9', 1.0]], 'Dwarka Sector 9': [['Dwarka Sector 8', 1.0], ['Dwarka Sector 10', 1.1]], .....}
# convert adj_list to dictionary of dictionaries
adj_list_dict = {key: {edge[0]: edge[1] for edge in value} for key, value in adj_list.items()}

# Streamlit UI for selecting current and destination stations
st.title('Delhi Metro Route Finder')
# plot whole network in a map 
# Create a Folium map centered around the first station
start_station = list(Name_To_Node.values())[0]
m = folium.Map(location=[start_station['Latitude'], start_station['Longitude']], zoom_start=13)
# Plot the stations on the map
for node_id, info in Name_To_Node.items():
    if len(info['Line'])>1:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="black", icon="info-sign"),
        ).add_to(m)
    elif 'Orange' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="orange", icon="info-sign"),
        ).add_to(m)
    elif 'Green Branch' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="green", icon="info-sign"),
        ).add_to(m)
    elif 'Green' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="green", icon="info-sign"),
        ).add_to(m)
    elif 'Blue Branch' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)
    elif 'Gray' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="gray", icon="info-sign"),
        ).add_to(m)
    elif 'Rapid' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="lightred", icon="info-sign"),
        ).add_to(m)
    elif 'Aqua' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="cadetblue", icon="info-sign"),
        ).add_to(m)
    elif 'Red' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)
    elif 'Pink' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="darkpurple", icon="info-sign"),
        ).add_to(m)
    elif 'Magenta' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="pink", icon="info-sign"),
        ).add_to(m)
    elif 'Violet' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="purple", icon="info-sign"),
        ).add_to(m)
    elif 'Yellow' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="beige", icon="info-sign"),
        ).add_to(m)
    elif 'Blue' in info['Line']:
        folium.Marker(
            location=[info['Latitude'], info['Longitude']],
            popup=f"{info['Name']}",
            tooltip=info['Name'],
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

# Use streamlit_folium to display the map
st.header('Delhi Metro Network Map')
st_folium(m, width=800, height=600)

# mention metro lines and their colors from above 
st.write('**Metro Lines:**')


current_station = st.selectbox('Select Current Station', list(Name_To_Node.keys()))
destination_station = st.selectbox('Select Destination Station', list(Name_To_Node.keys()))

def price(distance):
    if distance < 2:
        return 10
    elif distance < 5:
        return 20
    elif distance < 12:
        return 30
    elif distance < 21:
        return 40
    elif distance < 32:
        return 50
    else:
        return 60
    


# Dijkstra's algorithm to find the shortest path where edge is distance between stations, return path and total distance
def dijkstra_distance(adj_list, start, end):
    G = nx.Graph()
    for node in adj_list:
        for edge in adj_list[node]:
            G.add_edge(node, edge[0], weight=edge[1])
    path = nx.shortest_path(G, start, end, weight='weight')
    distance = nx.shortest_path_length(G, start, end, weight='weight')
    return path, distance

# Get the shortest path between the two stations
path1, distance1 = dijkstra_distance(adj_list, current_station, destination_station)
Station_count1 = len(path1)
cost1 = price(distance1)
# colors1 list 
colors1 = []
for i in range(len(path1)):
    a = path1[i]
    a_color = 'black' if len(Name_To_Node[a]["Line"]) > 1 else Name_To_Node[a]["Line"][0]
    colors1.append(a_color)


def dijkstra_stationCount(adj_list, start, end):
    G = nx.Graph()
    for node in adj_list:
        for edge in adj_list[node]:
            G.add_edge(node, edge[0], weight=1)
    path = nx.shortest_path(G, start, end, weight='weight')
    return path

# Get the shortest path between the two stations
path2 = dijkstra_stationCount(adj_list, current_station, destination_station)
Station_count2 = len(path2)
# find distance 
distance2 = 0
for i in range(len(path2)-1):
    distance2 += adj_list_dict[path2[i]][path2[i+1]]
cost2 = price(distance2)
# colors2 list
colors2 = []
for i in range(len(path2)):
    a = path2[i]
    a_color = 'black' if len(Name_To_Node[a]["Line"]) > 1 else Name_To_Node[a]["Line"][0]
    colors2.append(a_color)


# Display the path on the map using Folium
# Create a Folium map centered around Delhi
m1 = folium.Map(location=[28.7041, 77.1025], zoom_start=11)

# Add the path to the map
for i in range(len(path1)-1):
    a = path1[i]
    b = path1[i+1]
    # Get latitude and longitude of the stations
    a_lat = Name_To_Node[a]["Latitude"]
    a_lon = Name_To_Node[a]["Longitude"]
    a_color = 'black' if len(Name_To_Node[a]["Line"]) > 1 else Name_To_Node[a]["Line"][0]
    b_lat = Name_To_Node[b]["Latitude"]
    b_lon = Name_To_Node[b]["Longitude"]
    b_color = 'black' if len(Name_To_Node[b]["Line"]) > 1 else Name_To_Node[b]["Line"][0]
    
    # Add a line to the map
    folium.PolyLine([(a_lat, a_lon), (b_lat, b_lon)], color='black', weight=5).add_to(m1)

    # Add a marker for the stations
    folium.Marker([a_lat, a_lon], popup=a, icon=folium.Icon(color=a_color)).add_to(m1)
    folium.Marker([b_lat, b_lon], popup=b, icon=folium.Icon(color=b_color)).add_to(m1)


m2 = folium.Map(location=[28.7041, 77.1025], zoom_start=11)

# Add the path to the map
for i in range(len(path2)-1):
    a = path2[i]
    b = path2[i+1]
    # Get latitude and longitude of the stations
    a_lat = Name_To_Node[a]["Latitude"]
    a_lon = Name_To_Node[a]["Longitude"]
    a_color = 'black' if len(Name_To_Node[a]["Line"]) > 1 else Name_To_Node[a]["Line"][0]
    b_lat = Name_To_Node[b]["Latitude"]
    b_lon = Name_To_Node[b]["Longitude"]
    b_color = 'black' if len(Name_To_Node[b]["Line"]) > 1 else Name_To_Node[b]["Line"][0]
    
    # Add a line to the map
    folium.PolyLine([(a_lat, a_lon), (b_lat, b_lon)], color='black', weight=5).add_to(m2)

    # Add a marker for the stations
    folium.Marker([a_lat, a_lon], popup=a, icon=folium.Icon(color=a_color)).add_to(m2)
    folium.Marker([b_lat, b_lon], popup=b, icon=folium.Icon(color=b_color)).add_to(m2)


# Use streamlit_folium to display the map
# st.write('Map:')
# st_folium(m, width=700, height=500)

def display_route(route, total_distance, cost, station_count, route_map, colors):
    st.write(f"**Cost:** {cost}")
    st.write(f"**Total Distance:** {total_distance:.2f} km")
    st.write(f"**Number of Stations:** {station_count}")
    
    st.write("**Route:**")
    for station, color in zip(route, colors):
        st.markdown(f"<span style='color:{color};font-weight:bold;'>{station}</span>", unsafe_allow_html=True)

    # st.write("**Map:**")
    # st_folium(route_map, width=300, height=400)
    folium_static(route_map, width=500, height=500)


col1, col2 = st.columns(2, gap="large")
with col1:
    st.header("Route by Minimum Distance")
    display_route(path1, distance1, cost1, Station_count1, m1, colors1)

with col2:
    st.header("Route by Minimum Stations")
    display_route(path2, distance2, cost2, Station_count2, m2, colors2)


# create a function to find minimum spanning tree 
def min_spanning_tree(adj_list):
    G = nx.Graph()
    for node in adj_list:
        for edge in adj_list[node]:
            G.add_edge(node, edge[0], weight=edge[1])
    T = nx.minimum_spanning_tree(G)
    return T

# Find the minimum spanning tree of the Delhi Metro network
T = min_spanning_tree(adj_list)

# Display the whole network (edges) on the folium map in yellow and highlight the minimum spanning tree edges in red
m3 = folium.Map(location=[28.7041, 77.1025], zoom_start=11)
for node in adj_list:
    for edge in adj_list[node]:
        a = node
        b = edge[0]
        a_lat = Name_To_Node[a]["Latitude"]
        a_lon = Name_To_Node[a]["Longitude"]
        b_lat = Name_To_Node[b]["Latitude"]
        b_lon = Name_To_Node[b]["Longitude"]
        folium.PolyLine([(a_lat, a_lon), (b_lat, b_lon)], color='yellow', weight=5).add_to(m3)

for edge in T.edges:
    a = edge[0]
    b = edge[1]
    a_lat = Name_To_Node[a]["Latitude"]
    a_lon = Name_To_Node[a]["Longitude"]
    b_lat = Name_To_Node[b]["Latitude"]
    b_lon = Name_To_Node[b]["Longitude"]
    folium.PolyLine([(a_lat, a_lon), (b_lat, b_lon)], color='red', weight=5).add_to(m3)

st.header("Minimum Spanning Tree of Delhi Metro Network marked in red")
folium_static(m3, width=800, height=600)
# Create a Folium map centered around Delhi and plot the minimum spanning tree
# m3 = folium.Map(location=[28.7041, 77.1025], zoom_start=11)
# for edge in T.edges:
#     a = edge[0]
#     b = edge[1]
#     a_lat = Name_To_Node[a]["Latitude"]
#     a_lon = Name_To_Node[a]["Longitude"]
#     a_color = 'black' if len(Name_To_Node[a]["Line"]) > 1 else Name_To_Node[a]["Line"][0]
#     b_lat = Name_To_Node[b]["Latitude"]
#     b_lon = Name_To_Node[b]["Longitude"]
#     b_color = 'black' if len(Name_To_Node[b]["Line"]) > 1 else Name_To_Node[b]["Line"][0]
#     # folium.PolyLine([(a_lat, a_lon), (b_lat, b_lon)], color='black', weight=5).add_to(m3)
#     folium.Marker([a_lat, a_lon], popup=a, icon=folium.Icon(color=a_color)).add_to(m3)
#     folium.Marker([b_lat, b_lon], popup=b, icon=folium.Icon(color=b_color)).add_to(m3)

# st.header("Minimum Spanning Tree of Delhi Metro Network")
# folium_static(m3, width=800, height=600)








import streamlit as st
import openrouteservice as ors
import folium
from streamlit_folium import st_folium


st.title("🎈Disaster Response Community")
st.write(
    "Thank You Jack. \n You have been assigned the following route.)."
)


client = ors.Client(key=st.secrets["ORSKEY"])


m = folium.Map(location=[34.04, -118.54], tiles='cartodbpositron', zoom_start=13)

vehicle_locations = [[-118.52253,34.04494],
                     #[-118.47952,34.05835]
                     ]
job_locations = [[-118.50193,34.02933],
                 [-118.49048,34.04762],
                 [-118.54102,34.0501],
                 [-118.54618,34.04558],
                 [-118.545, 34.04],
                 [-118.54, 34.045]]

shipments_pickups = [[-118.50193,34.02933],[-118.48867,34.03733],[-118.50393,34.02833]]

shipment_deliveries = [[-118.54718,34.04558],[-118.54618,34.04558],[-118.54518,34.04558]]



# Assign vehicles to do the jobs
vehicles = []
for idx, coords in enumerate(vehicle_locations):
    vehicles.append(ors.optimization.Vehicle(
        id=idx,
        profile='driving-car',
        start=coords,
        end=coords,
        skills=[1],
        capacity=[2]  # Limit capacity so only 3 jobs can be taken by each vehicle
    ))
    folium.Marker(location=list(reversed(coords)), icon=folium.Icon(icon='truck', prefix='fa')).add_to(m)

# Define jobs to be carried out
# jobs=[]
# for idx, coords in enumerate(job_locations):
#     jobs.append(ors.optimization.Job(
#         id=idx,
#         location=coords,
#         amount=[1]  # Occupies capacity in vehicle
#     ))
#     folium.Marker(location=list(reversed(coords)), icon=folium.Icon(icon='archive', prefix='fa', color='green')).add_to(m)

shipments=[]
for idx, coords in enumerate(zip(shipments_pickups, shipment_deliveries)):
    shipments.append(ors.optimization.Shipment(
        pickup=ors.optimization.ShipmentStep(
            id=idx,
            location=coords[0],
        ),

        delivery=ors.optimization.ShipmentStep(
            id=idx,
            location=coords[1]),
        amount=[1],  # Occupies capacity in vehicle
        skills=[1],
        priority=1
    ))
    folium.Marker(location=list(reversed(coords[0])), icon=folium.Icon(icon='archive', prefix='fa', color='green')).add_to(m)
    folium.Marker(location=list(reversed(coords[1])), icon=folium.Icon(icon='archive', prefix='fa', color='red')).add_to(m)



optimized = client.optimization(
    shipments=shipments,
    vehicles=vehicles,
    geometry=True,  ## will output the geometry,
)

folium.PolyLine(
    locations=[list(reversed(coords)) for coords in ors.convert.decode_polyline(optimized['routes'][0]['geometry'])['coordinates']],
    color='blue'
).add_to(m)


# folium.PolyLine(
#     locations=[list(reversed(coords)) for coords in ors.convert.decode_polyline(optimized['routes'][1]['geometry'])['coordinates']],
#     color='orange'
# ).add_to(m)





# line_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
# pickups = [[34.05,-118.55],
#            [34.04,-118.545],
#            [34.045,-118.54]]
# deliveries = [[34.04,-118.545]]
# base_location = [34.04, -118.54]
#
# m = folium.Map(location=[34.04, -118.54], zoom_start=16)
#
# vehicles = [
#     ors.optimization.Vehicle(id=0,profile='driving-car',start=base_location,capacity=[5])
# ]
#
# # Jobs
# jobs = [ors.optimization.Job(id=index,location=pickups, amount=[1]) for index, pickups in enumerate(list(reversed(pickups)))]
#
# optimized = client.optimization(
#     jobs=jobs,
#     vehicles=vehicles,
#     geometry=True,
# )
#
# for pickup in pickups:
#     folium.Marker(
#         location=list(pickup), icon=folium.Icon(color='red')).add_to(m)
#
# for delivery in deliveries:
#     folium.Marker(
#         location=list(delivery), icon=folium.Icon(color='green')).add_to(m)
#
# # for route in optimized['routes']:
# #     folium.PolyLine(
# #         locations=[(step['location'][1], step['location'][0]) for step in route['geometry']['coordinates']],
# #         color=line_colors.pop(0),
# #         weight=5,
# #         opacity=0.8
# #     ).add_to(m)


# # call to render Folium map in Streamlit
st_data = st_folium(m, width=725)

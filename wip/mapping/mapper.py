# Imports all the libraries we use
import folium
import pandas as pd
import os
import webbrowser



# Sets up the markers on the map
# List of colours can be found here: https://stackoverflow.com/a/41993318
# List of icons can be found here: https://getbootstrap.com/docs/3.3/components/
colour = 'purple'
image = 'screenshot'

# Reads the .csv file and assigns it to a variable
path = pd.read_csv('raw_gps_data.csv')

# Uncomment these to have the values of the Latitude and Longitude columns printed out
#print (path["Latitude"])
#print (path["Longitude"])


# Sets up the map, writes the map parameters to a variable
mapPATH = folium.Map(location=[28.6145,-80.6941]) #,zoom_start=1000)
# Delete the ) , space, and # in front of #,zoom_start=1000) to 
# define a starting zoom. You should also change the Lat & Long
# to a region that is close to where you are mapping.

# Creates the map
for index, row in path.iterrows():
    lat = row["Latitude"]
    lng = row["Longitude"]
    folium.Marker([lat,lng], icon=folium.Icon(color = colour,icon = image)).add_to(mapPATH)

# Saves the map
mapPATH.save(outfile='MappedPath.html')

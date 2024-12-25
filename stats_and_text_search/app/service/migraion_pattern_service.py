import pandas as pd
import folium
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="city_coordinates")

def analyze_group_movement_patterns(group_data):
    df = pd.DataFrame(group_data)

    df['date'] = pd.to_datetime(df['date'].apply(lambda x: f"{x['year']}-{x['month']}-{x['day']}"))

    df[['region', 'country', 'city']] = df['location'].apply(pd.Series)[['region', 'country', 'city']]

    df['location_str'] = df['city'] + ', ' + df['country']

    df['fatalities'] = df['casualties'].apply(lambda x: x['fatalities'])
    df['injuries'] = df['casualties'].apply(lambda x: x['injuries'])

    location_freq = df.groupby(['region', 'country', 'city']).agg(
        incident_count=('date', 'count'),
        first_incident=('date', 'min'),
        last_incident=('date', 'max'),
        total_fatalities=('fatalities', 'sum'),
        total_injuries=('injuries', 'sum')
    ).reset_index()

    location_frequency = {
        f"{row['city']}, {row['country']}": row.to_dict()
        for _, row in location_freq.iterrows()
    }

    return {'location_frequency': location_frequency}

def get_coordinates(city_name):
    location = geolocator.geocode(city_name, timeout=None)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def add_coords(location_frequency: dict):
    result = {}
    for key, value in location_frequency.items():
        city_name = f"{value['city']}, {value['country']}"
        latitude, longitude = get_coordinates(city_name)
        if latitude and longitude:
            result[key] = {
                'region': value['region'],
                'country': value['country'],
                'city': value['city'],
                'latitude': latitude,
                'longitude': longitude,
                'incident_count': value['incident_count'],
                'first_incident': value['first_incident'],
                'last_incident': value['last_incident'],
                'total_fatalities': value['total_fatalities'],
                'total_injuries': value['total_injuries'],
            }
    return result

def create_popup_content(info):
    return f"""
    <div style="max-height: 150px; overflow-y: scroll; width: 200px;">
        <strong>{info['city']}, {info['country']}</strong><br>
        <i>Incidents:</i> {info['incident_count']}<br>
        <i>First Incident:</i> {info['first_incident'].strftime('%Y-%m-%d')}<br>
        <i>Last Incident:</i> {info['last_incident'].strftime('%Y-%m-%d')}<br>
        <i>Fatalities:</i> {info['total_fatalities']}<br>
        <i>Injuries:</i> {info['total_injuries']}
    </div>
    """

def add_marker(map_object, location, info, icon_color, icon_type):
    folium.Marker(
        location=[info['latitude'], info['longitude']],
        popup=create_popup_content(info),
        icon=folium.Icon(icon=icon_type, prefix='fa', color=icon_color)
    ).add_to(map_object)

def draw_incident_line(map_object, coordinates):
    folium.PolyLine(coordinates, color='blue', weight=2.5, opacity=0.7).add_to(map_object)

def create_events_map(data):
    sorted_data = sorted(data.items(), key=lambda x: x[1]['first_incident'])

    m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

    coordinates = []

    for location, info in sorted_data:
        add_marker(m, location, info, 'blue', 'info-sign')
        coordinates.append([info['latitude'], info['longitude']])

    draw_incident_line(m, coordinates)

    add_marker(m, sorted_data[0][0], sorted_data[0][1], 'green', 'arrow-up')
    add_marker(m, sorted_data[-1][0], sorted_data[-1][1], 'red', 'arrow-down')

    return m
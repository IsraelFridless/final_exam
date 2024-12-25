import io

import folium
import pandas as pd
from folium.plugins import HeatMap
from app.repository.mongo_repository.statistics_repository import *
from app.repository.mongo_repository.location_repository import *
import matplotlib.pyplot as plt


def generate_map_q_8(results: List[Dict], location_type: str = "region") -> folium.Map:
    m = folium.Map(location=[20, 0], zoom_start=2)

    for result in results:
        location_name = result.get(location_type, "Unknown Location")
        central_coords = (
            get_central_coords_by_region(location_name)
            if location_type == "region"
            else get_central_coords_by_country(location_name)
        )

        if not central_coords:
            continue

        latitude = central_coords.get("latitude")
        longitude = central_coords.get("longitude")

        top_groups = result.get("topGroups", [])
        group_list_html = "".join(
            f"<li>• <strong>{group['group']}</strong> - {group['eventCount']} events</li>" for group in top_groups
        )
        group_list = f"<ul style='max-height: 150px; overflow-y: auto; margin: 0; padding: 0; list-style-type: disc;'>{group_list_html}</ul>"

        popup_content = (
            f"<strong>Location:</strong> {location_name}<br>"
            f"<strong>Top Groups:</strong><br>{group_list}<br>"
            f"<strong>Group Count:</strong> {result.get('countGroups', 0)}"
        )

        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{location_name} - {result.get('countGroups', 0)} top groups",
        ).add_to(m)

    return m

def generate_map_q_11(results: List[Dict], location_type: str = "region") -> folium.Map:
    m = folium.Map(location=[20, 0], zoom_start=2)

    for result in results:
        location_name = result.get(location_type, "Unknown Location")
        central_coords = (
            get_central_coords_by_region(location_name)
            if location_type == "region"
            else get_central_coords_by_country(location_name)
        )

        if not central_coords:
            continue

        latitude = central_coords.get("latitude")
        longitude = central_coords.get("longitude")

        groups = result.get("groups", [])
        group_list_html = "".join(f"<li>{group}</li>" for group in groups)
        group_list = f"<ul style='max-height: 150px; overflow-y: auto; margin: 0; padding: 0; list-style: none;'>{group_list_html}</ul>"

        popup_content = (
            f"<strong>Location:</strong> {location_name}<br>"
            f"<strong>Target:</strong> {result.get('target', 'Unknown')}<br>"
            f"<strong>Groups:</strong><br>{group_list}<br>"
            f"<strong>Group Count:</strong> {result.get('groupCount', 0)}"
        )

        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{location_name} - {result.get('groupCount', 0)} groups",
        ).add_to(m)

    return m

def generate_map_q_14(results: List[Dict], location_type: str = "region") -> folium.Map:
    m = folium.Map(location=[20, 0], zoom_start=2)

    for result in results:
        location_name = result.get(location_type, "Unknown Location")
        central_coords = (
            get_central_coords_by_region(location_name)
            if location_type == "region"
            else get_central_coords_by_country(location_name)
        )

        if not central_coords:
            continue

        latitude = central_coords.get("latitude")
        longitude = central_coords.get("longitude")

        groups = result.get("groups", [])
        group_list_html = "".join(f"<li>{group}</li>" for group in groups)
        group_list = f"<ul style='max-height: 150px; overflow-y: auto;'>{group_list_html}</ul>"

        popup_content = (
            f"<strong>Location:</strong> {location_name}<br>"
            f"<strong>Attack Type:</strong> {result.get('attack_type', 'Unknown')}<br>"
            f"<strong>Groups:</strong> {group_list}<br>"
            f"<strong>Group Count:</strong> {result.get('groupCount', 0)}"
        )

        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{location_name} ({result.get('groupCount', 0)} groups)",
        ).add_to(m)

    return m

def generate_map_q_16(results: List[Dict], location_type: str = "region") -> folium.Map:
    m = folium.Map(location=[20, 0], zoom_start=2)

    for result in results:
        location_name = result.get(location_type, "Unknown Location")
        central_coords = (
            get_central_coords_by_region(location_name)
            if location_type == "region"
            else get_central_coords_by_country(location_name)
        )

        if not central_coords:
            continue

        latitude = central_coords.get("latitude")
        longitude = central_coords.get("longitude")

        # Format the unique groups into a scrollable list
        unique_groups = result.get("unique_groups", [])
        group_list_html = "".join(f"<li>{group}</li>" for group in unique_groups)
        group_list = f"<ul style='max-height: 150px; overflow-y: auto; margin: 0; padding: 0; list-style: none;'>{group_list_html}</ul>"

        popup_content = (
            f"<strong>Location:</strong> {location_name}<br>"
            f"<strong>Unique Groups:</strong><br>{group_list}<br>"
            f"<strong>Group Count:</strong> {result.get('countGroups', 0)}"
        )

        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{location_name} - {result.get('countGroups', 0)} unique groups",
        ).add_to(m)

    return m

def generate_heatmap_by_date_range(results: List[Dict]) -> folium.Map:
    m = folium.Map(location=[20, 0], zoom_start=2)

    heat_data = []

    for result in results:
        location = result.get("location", {})

        latitude = location.get("latitude")
        longitude = location.get("longitude")

        if latitude is not None and longitude is not None:
            heat_data.append([latitude, longitude])

    if heat_data:
        HeatMap(heat_data, radius=15, blur=20, max_zoom=13).add_to(m)

    return m

def normalize_helper(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

def get_color_helper(normalized_score):
    if normalized_score > 0.5:
        return 'red'
    elif 0.5 > normalized_score > 0.25:
        return 'yellow'
    else:
        return 'green'

def generate_colored_map(results) -> folium.Map:
    m = folium.Map(location=[20, 0], zoom_start=2)

    min_score = min(d['avgCasualtyScore'] for d in results)
    max_score = max(d['avgCasualtyScore'] for d in results)

    for region_data in results:
        region = region_data['region']
        score = region_data['avgCasualtyScore']
        normalized_score = normalize_helper(score, min_score, max_score)

        coords = get_central_coords_by_region(region)
        lat, lon = coords['latitude'], coords['longitude']

        color = get_color_helper(normalized_score)

        popup_content = (
            f"<strong>Region:</strong> {region}<br>"
            f"<strong>Avg Casualty Score:</strong> {score:.2f}"
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(popup_content, max_width=300),
            weight=2
        ).add_to(m)

    return m

def plot_deadliest_attack_types(results: List[Dict]):
    attack_types = [item['attack_type'] for item in results]
    max_deadliness = [item['max_deadliness'] for item in results]

    plt.figure(figsize=(10, 5))
    plt.barh(attack_types, max_deadliness, color='skyblue')
    plt.xlabel('Max Deadliness Score')
    plt.ylabel('Attack Type')
    plt.title('Deadliest Attack Types')
    plt.gca().invert_yaxis()
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plt.close()
    return buffer

def plot_casualties_by_group(results: List[Dict]):
    groups = [item['group'] for item in results]
    casualty_scores = [item['totalCasualtiesScore'] for item in results]

    plt.figure(figsize=(10, 5))
    plt.barh(groups, casualty_scores, color='skyblue')
    plt.xlabel('Total Casualties Score')
    plt.ylabel('Terrorist Group')
    plt.title('Casualties by Terrorist Group')
    plt.gca().invert_yaxis()
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plt.close()
    return buffer

def plot_migration_patterns(results: List[Dict]) -> folium.Map:
    data = []
    for event in results:
        data.append({
            'region': event['region'],
            'country': event['country'],
            'city': event['city'],
            'group': event['group'],
            'year': event['year'],
            'month': event['month'],
            'total_events': event['total_events'],
            'latitude': event.get('latitude'),
            'longitude': event.get('longitude')
        })

    df = pd.DataFrame(data)

    df = df.dropna(subset=['latitude', 'longitude'])

    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=5)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['total_events'] / 2,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"Group: {row['group']}<br>Events: {row['total_events']}<br>Year: {row['year']}<br>Month: {row['month']}"
        ).add_to(m)

    return m

def generate_map_for_textual_search_results(results: List[Dict]) -> folium.Map:
    m = folium.Map(location=[20, 0], zoom_start=2)

    for result in results:
        latitude = result.get("latitude")
        longitude = result.get("longitude")
        result_type = result.get("type")

        if latitude is None or longitude is None:
            continue

        if result_type == "event":
            popup_content = f"""
            <div style="max-width: 300px;">
                <strong>Type:</strong> {result_type}<br>
                <strong>Summary:</strong> {result.get('summary', 'N/A')}<br>
            </div>
            """
        elif result_type == "article":
            popup_content = f"""
            <div style="max-width: 300px;">
                <strong>Type:</strong> {result_type}<br>
                <strong>Title:</strong> {result.get('title', 'N/A')}<br>
                <strong>Body:</strong> {result.get('body', 'N/A')}<br>
            </div>
            """

        iframe = folium.IFrame(popup_content, width=300, height=200)
        popup = folium.Popup(iframe, max_width=300)

        folium.Marker(location=[latitude, longitude], popup=popup).add_to(m)

    return m
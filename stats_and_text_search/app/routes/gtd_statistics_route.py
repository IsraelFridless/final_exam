import base64

from flask import Blueprint, request, jsonify

from app.service.map_and_plot_service import *

gtd_statistics_blueprint = Blueprint('gtd_statistics', __name__)

@gtd_statistics_blueprint.route('/groups_by_location_and_mutual_targets', methods=['GET'])
def groups_by_location_and_mutual_targets_route():
    try:
        location_type = request.args.get('locationType', 'region')
        results = get_groups_by_location_and_mutual_targets(location_type)
        map_content = generate_map_q_11(results, location_type)
        return jsonify({'map_html': map_content._repr_html_()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/groups_by_attack_type_and_location', methods=['GET'])
def groups_by_attack_type_and_location_route():
    try:
        location_type = request.args.get('locationType', 'region')
        results = get_groups_by_attack_type_and_location(location_type)
        map_content = generate_map_q_14(results, location_type)
        return jsonify({'map_html': map_content._repr_html_()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/coactive_groups_by_location', methods=['GET'])
def coactive_groups_by_location_route():
    try:
        location_type = request.args.get('locationType', 'region')
        results = get_coactive_groups_by_location(location_type)
        map_content = generate_map_q_16(results, location_type)
        return jsonify({'map_html': map_content._repr_html_()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/most_active_groups_per_location', methods=['GET'])
def most_active_groups_per_location_route():
    try:
        location_type = request.args.get('locationType', 'region')
        results = get_most_active_groups_per_location(location_type)
        map_content = generate_map_q_8(results, location_type)
        return jsonify({'map_html': map_content._repr_html_()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/coordinates_by_date_range', methods=['GET'])
def coordinates_by_date_range_route():
    try:
        start_year = request.args.get('start_year', 1970)
        start_month = request.args.get('start_month', 1)
        end_year = request.args.get('end_year', 2000)
        end_month = request.args.get('end_month', 1)
        results = get_coordinates_by_date_range(start_year, start_month, end_year, end_month)
        map_content = generate_heatmap_by_date_range(results)
        return jsonify({'map_html': map_content._repr_html_()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/avg_casualty_score_per_region', methods=['GET'])
def avg_casualty_score_per_region_route():
    try:
        results = get_avg_casualty_score_per_region()
        map_content = generate_colored_map(results)
        return jsonify({'map_html': map_content._repr_html_()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/deadliest_attack_type', methods=['GET'])
def deadliest_attack_type_route():
    try:
        limit = int(request.args.get('limit', 5))
        results = get_deadliest_attack_type(limit)
        buffer = plot_deadliest_attack_types(results)

        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        image_url = f"data:image/png;base64,{base64_image}"
        return jsonify({'map_html': image_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/groups_with_highest_casualty_score', methods=['GET'])
def groups_with_highest_casualty_score_route():
    try:
        limit = int(request.args.get('limit', 5))
        results = get_groups_with_highest_casualty_score(limit)
        buffer = plot_casualties_by_group(results)

        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        image_url = f"data:image/png;base64,{base64_image}"
        return jsonify({'map_html': image_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/multiple_groups_involved_in_event', methods=['GET'])
def multiple_groups_involved_in_event_route():
    try:
        result = get_multiple_groups_involved_in_event()
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gtd_statistics_blueprint.route('/group_migration_patterns', methods=['GET'])
def group_migration_patterns_route():
    try:
        results = get_group_migration_patterns()

        map_content = plot_migration_patterns(results)
        return jsonify({'map_html': map_content._repr_html_()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
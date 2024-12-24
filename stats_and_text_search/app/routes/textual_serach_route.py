from flask import Blueprint, request, jsonify

from app.service.map_and_plot_service import *
from app.service.textual_search_service import *

text_search_blueprint = Blueprint('text_search', __name__)

@text_search_blueprint.route('/keywords', methods=['GET'])
def keyword_in_all_data_sources_route():
    try:
        keyword = request.args.get('keyword')
        results = search_keyword_in_all_data_sources(keyword)
        map_content = generate_map_for_textual_search_results(results)
        return jsonify({'map_html': map_content._repr_html_()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@text_search_blueprint.route('/news', methods=['GET'])
def keyword_in_news_articles_route():
    try:
        keyword = request.args.get('keyword')
        results = search_keyword_in_news_articles(keyword)
        map_content = generate_map_for_textual_search_results(results)
        return jsonify({'map_html': map_content._repr_html_()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@text_search_blueprint.route('/historic', methods=['GET'])
def keyword_in_historic_events_route():
    try:
        keyword = request.args.get('keyword')
        results = search_keyword_in_historic_events(keyword)
        map_content = generate_map_for_textual_search_results(results)
        return jsonify({'map_html': map_content._repr_html_()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@text_search_blueprint.route('/combined', methods=['GET'])
def results_by_date_range_all_sources_route():
    try:
        keyword = request.args.get('keyword')
        start_year = request.args.get('start_year', 1970)
        start_month = request.args.get('start_month', 1)
        end_year = request.args.get('end_year', 2000)
        end_month = request.args.get('end_month', 1)
        results = search_results_by_date_range_all_sources(keyword, start_year, start_month, end_year, end_month)
        map_content = generate_map_for_textual_search_results(results)
        return jsonify({'map_html': map_content._repr_html_()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
from flask import Flask, render_template
from flask_cors import CORS


from app.routes.gtd_statistics_route import gtd_statistics_blueprint
from app.routes.textual_serach_route import text_search_blueprint

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.register_blueprint(gtd_statistics_blueprint, url_prefix='/api/statistics')
    app.register_blueprint(text_search_blueprint, url_prefix='/api/search')
    app.run(port=5000, debug=True)
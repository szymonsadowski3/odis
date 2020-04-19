from waitress import serve
from src.rest_api.api import app

serve(app, host='0.0.0.0', port=5000)

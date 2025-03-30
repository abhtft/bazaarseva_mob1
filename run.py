"""
Run script for Kirana Suvidha application
"""
from kirana_suvidha.application import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False) 
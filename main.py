from website import create_app
import os
import logging
import sys

logging.basicConfig(level=logging.INFO)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
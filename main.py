from website import create_app
import os
from chatbot import bot

app = create_app()
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    #bot.__train__()
    app.run(debug=True, port=port)
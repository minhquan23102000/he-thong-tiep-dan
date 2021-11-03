from website import create_app
from chatbot import bot

app = create_app()

if __name__ == '__main__':
    #bot.__train__()
    app.run(debug=True)
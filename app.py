from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.comparisons import levenshtein_distance

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", 
                        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                        database_uri='mongodb+srv://root:oyEoPn39je1xGa38@cluster0-bl24x.mongodb.net/test?retryWrites=true&w=majority',
                        statement_comparison_function=levenshtein_distance,
                        filters=[
                        'chatterbot.filters.RepetitiveResponseFilter'
                        ],
                        logic_adapters=[
                        {
                            'import_path': 'chatterbot.logic.BestMatch',
                            'threshold': 0.85,
                            'default_response': 'I am sorry, but I do not understand.'
                        }])

trainer = ChatterBotCorpusTrainer(english_bot)

# For training the corpus data
# trainer.train("./data/my_corpus/")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))


if __name__ == "__main__":
    app.run()

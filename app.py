""" ChatBot
"""
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import levenshtein_distance
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
APP = Flask(__name__)

ENGLISH_BOT = ChatBot("Chatterbot",
                      storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                      database_uri='mongodb+srv://root:M87xJmecx3MBdZgL@cluster0-bl24x.mongodb.net/test?retryWrites=true&w=majority',# pylint: disable=line-too-long
                      statement_comparison_function=levenshtein_distance,
                      filters=[
                          'chatterbot.filters.RepetitiveResponseFilter'],
                      preprocessors=[
                          'chatterbot.preprocessors.clean_whitespace'],
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch',
                              'threshold': 0.85,
                              'default_response': 'I am sorry, but I do not understand.'
                              }
                          ]
                      )

TRAINER = ChatterBotCorpusTrainer(ENGLISH_BOT)

# For training Custom corpus data
# TRAINER.train("./data/my_corpus/")

# For training English corpus data
# TRAINER.train('chatterbot.corpus.english')

# For training list of conversations
# TRAINER_LIST = ListTrainer(ENGLISH_BOT)
# TRAINER_LIST.train([
#     "How are you?",
#     "I am good.",
#     "That is good to hear.",
#     "Thank you",
#     "You are welcome.",
# ])

@APP.route("/")
def home():
    """
    Home
    """
    return render_template("index.html")

@APP.route("/get")
def get_bot_response():
    """
    Get reply from Bot
    """
    user_text = request.args.get('msg')
    return str(ENGLISH_BOT.get_response(user_text))


if __name__ == "__main__":
    APP.run()

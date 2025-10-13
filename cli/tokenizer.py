import string
from nltk.stem import PorterStemmer

class Tokenizer():
    stopwords = []

    def __init__(self, stopword_file):
        # Stopwords
        with open(stopword_file, "r") as f:
            txt = f.read()
            self.stopwords = txt.splitlines()     


    def __clean_string(self, s) -> str:
        return s.lower().translate(str.maketrans('', '', string.punctuation))


    def __separate_words(self, s) -> list[str]:
        s = " ".join(s.split())
        return s.split(" ")


    def __remove_stopwords(self, query) -> list[str]:
        removed = []
        for token in query:
            if token not in self.stopwords:
                removed.append(token)
        
        return removed


    def tokenize_text(self, text) -> list[str]:
        tokens = []

        # Lower case and remove punctuation
        s = self.__clean_string(text)

        # Convert string to list of words
        words = self.__separate_words(s)
        
        # Remove stopwords
        words = self.__remove_stopwords(words)

        # Stemming
        stemmer = PorterStemmer()
        for word in words:
            tokens.append(stemmer.stem(word, False))

        return tokens
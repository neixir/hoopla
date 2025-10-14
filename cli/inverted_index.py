import os, pickle
from pathlib import Path
from collections import Counter
from tokenizer import Tokenizer

CACHE_DIRECTORY = "cache"
INDEX_FILENAME = "index.pkl"
DOCMAP_FILENAME = "docmap.pkl"
TF_FILENAME = "term_frequencies.pkl"

class InvertedIndex:
    index = {}      # dictionary mapping tokens (strings) to sets of document IDs (integers).
    docmap = {}     # dictionary mapping document IDs to their full document objects.
    term_frequencies = {} # dictionary of document IDs to Counter objects
    
    # counter = Counter()
    tokenizer = Tokenizer("data/stopwords.txt")

    # Tokenize the input text, then add each token to the index with the document ID.
    def __add_document(self, doc_id, text):
        tokenized = self.tokenizer.tokenize_text(text)
        for token in tokenized:
            if token in self.index:
                self.index[token].add(doc_id)
            else:
                self.index[token] = {doc_id}

            # update the term frequencies for each token in the document.
            # For each token, increment its count in the Counter for that document ID.
            if doc_id not in self.term_frequencies:
                self.term_frequencies[doc_id] = Counter()
            self.term_frequencies[doc_id][token] += 1


    # It should get the set of documents for a given token, and return them as a list,
    # sorted in ascending order by document ID.
    # For our purposes, you can assume that the input term is a single word/token
    #  – though you may still want to lowercase it for good measure.
    def get_documents(self, term):
        return sorted(self.index.get(term, []))


    # It should iterate over all the movies and add them to both the index and the docmap.
    def build(self, movies):
        # When adding the movie data to the index with __add_document(), concatenate the title
        # and the description (i.e., f"{m['title']} {m['description']}") and use that as the input text.
        q = len(movies)
        for m in movies:
            print(f"* Adding [{q}]", m["title"])
            doc_id = str(m["id"])
            text = f"{m['title']} {m['description']}"
            self.__add_document(doc_id, text)
            self.docmap[m["id"]] = m    # potser tb doc_id?
            q -= 1


    # It should save the index and docmap attributes to disk using the pickle module's dump function.
    def save(self):
        # Have this method create the cache directory if it doesn't exist (before trying to write files into it).
        directory = Path(CACHE_DIRECTORY)
        directory.mkdir(parents=True, exist_ok=True)
        
        index_file_path = CACHE_DIRECTORY + "/" + INDEX_FILENAME
        with open(index_file_path, "wb") as f:
            pickle.dump(self.index, f)

        docmap_file_path = CACHE_DIRECTORY + "/" + DOCMAP_FILENAME
        with open(docmap_file_path, "wb") as f:
            pickle.dump(self.docmap, f)

        tf_file_path = CACHE_DIRECTORY + "/" + TF_FILENAME
        with open(tf_file_path, "wb") as f:
            pickle.dump(self.term_frequencies, f)


    def load(self):
        # Load index
        index_file_path = CACHE_DIRECTORY + "/" + INDEX_FILENAME
        self.index = self.__load_or_raise(index_file_path)

        # Load docmap
        docmap_file_path = CACHE_DIRECTORY + "/" + DOCMAP_FILENAME
        self.docmap = self.__load_or_raise(docmap_file_path)

        # Load term_frequencies
        tf_file_path = CACHE_DIRECTORY + "/" + TF_FILENAME
        self.term_frequencies = self.__load_or_raise(tf_file_path)


    def get_tf(self, doc_id: str, term: str) -> int:
        tokenized = self.tokenizer.tokenize_text(term)
        if len(tokenized) > 1:
            raise Exception(f"Too many tokens in \"{term}\" ({len(tokenized)})")
        
        return self.term_frequencies.get(doc_id, Counter()).get(tokenized[0], 0)


    def __load_or_raise(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, "rb") as f:
            contents = pickle.load(f)
        
        return contents

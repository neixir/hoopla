import os, pickle
from pathlib import Path
from tokenizer import Tokenizer

# Use the file path/name cache/index.pkl for the index.
# Use the file path/name cache/docmap.pkl for the docmap.
CACHE_DIRECTORY = "cache"
INDEX_FILENAME = "index.pkl"
DOCMAP_FILENAME = "docmap.pkl"

class InvertedIndex:
    index = {}      # a dictionary mapping tokens (strings) to sets of document IDs (integers).
    docmap = {}     # a dictionary mapping document IDs to their full document objects.
    tokenizer = Tokenizer("data/stopwords.txt")

    # Tokenize the input text, then add each token to the index with the document ID.
    def __add_document(self, doc_id, text):
        tokenized = self.tokenizer.tokenize_text(text)
        for token in tokenized:
            if token in self.index:
                self.index[token].add(doc_id)
            else:
                self.index[token] = {doc_id}
            # print(token, self.index[token])


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
            text = f"{m['title']} {m['description']}"
            self.__add_document(m["id"], text)
            self.docmap[m["id"]] = m
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


    def load(self):
        # Load index
        index_file_path = CACHE_DIRECTORY + "/" + INDEX_FILENAME
        self.index = self.__load_or_raise(index_file_path)

        # Load docmap
        docmap_file_path = CACHE_DIRECTORY + "/" + DOCMAP_FILENAME
        self.docmap = self.__load_or_raise(docmap_file_path)


    def __load_or_raise(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, "rb") as f:
            contents = pickle.load(f)
        
        return contents

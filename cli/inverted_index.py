from pathlib import Path
from tokenize import tokenize_text

CACHE_DIRECTORY = "cache"
INDEX_FILENAME = "index.pkl"
DOCMAP_FILENAME = "docmap.pkl"

class InvertedIndex:
    index = {}      # a dictionary mapping tokens (strings) to sets of document IDs (integers).
    docmap = {}     # a dictionary mapping document IDs to their full document objects.

    """
    def __init__(self, index, docmap):
        self.index = index
        self.docmap = docmap
    """

    # Tokenize the input text, then add each token to the index with the document ID.
    def __add_document(self, doc_id, text):
        tokenized = tokenize_text(text)
        pass

    # It should get the set of documents for a given token, and return them as a list,
    # sorted in ascending order by document ID.
    # For our purposes, you can assume that the input term is a single word/token
    #  – though you may still want to lowercase it for good measure.
    def get_documents(self, term):
        pass


    # It should iterate over all the movies and add them to both the index and the docmap.
    def build():
        # When adding the movie data to the index with __add_document(), concatenate the title
        # and the description (i.e., f"{m['title']} {m['description']}") and use that as the input text.
        pass


    # It should save the index and docmap attributes to disk using the pickle module's dump function.
    def save():
        # Use the file path/name cache/index.pkl for the index.
        # Use the file path/name cache/docmap.pkl for the docmap.
        
        # Have this method create the cache directory if it doesn't exist (before trying to write files into it).
        directory = Path(CACHE_DIRECTORY)
        # Check and create
        directory.mkdir(parents=True, exist_ok=True)
        
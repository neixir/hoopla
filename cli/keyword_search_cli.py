#!/usr/bin/env python3

import os
import argparse, json, sys
from tokenizer import Tokenizer
from inverted_index import InvertedIndex

MAX_RESULTS = 5

# Only enable debug mode if an environment variable is set
if os.getenv("DEBUGPY", "0") == "1":
    import debugpy
    debugpy.listen(("0.0.0.0", 5678))
    print("🔍 Waiting for VS Code debugger to attach on port 5678...")
    debugpy.wait_for_client()
    print("✅ Debugger attached.")

def main() -> None:

    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build index")
    #build_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    # Obtenim les pelicules
    movies = {}
    with open("data/movies.json", "r") as f:
        contents = json.load(f)
        movies = contents["movies"]

    # Creem el 'tokenizer'
    tokenizer = Tokenizer("data/stopwords.txt")

    ii = InvertedIndex()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")

            tokenized_query = tokenizer.tokenize_text(args.query)
            print (f"Tokenized query: {tokenized_query}")

            try:
                ii.load()
            except Exception as ex:
                print(ex)
                sys.exit(-1)          
            
            doc_list = []
            for query_token in tokenized_query:
                docs = ii.get_documents(query_token)
                max = MAX_RESULTS - len(doc_list)
                if (len(doc_list) < MAX_RESULTS):   # max > 0
                    doc_list.extend(docs[:max])
                else:
                    break

            for doc in doc_list:
                id = ii.docmap[doc]["id"]
                title = ii.docmap[doc]["title"]                
                print(f"{id:4} {title}")

        case "build":
            # It should build the inverted index and save it to disk.
            # After doing so, it should print a message containing the first ID of the document
            # for the token 'merida' (which should be document 4651, "Brave").
            ii.build(movies)
            ii.save()
            # docs = ii.get_documents('merida')
            # print(f"First document for token 'merida' = {docs[0]}") 

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
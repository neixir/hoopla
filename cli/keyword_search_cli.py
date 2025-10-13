#!/usr/bin/env python3

import argparse, json
from tokenizer import Tokenizer
from inverted_index import InvertedIndex

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

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            tokenized_query = tokenizer.tokenize_text(args.query)

            print (f"Tokenized query: {tokenized_query}\n")
            
            movie_list = []
            for movie in movies:
                tokenized_title = tokenizer.tokenize_text(movie["title"])
                # print (f"Tokenized title: {tokenized_title}")

                token_exists = find_one_token(tokenized_query, tokenized_title)
                if token_exists:
                    movie_list.append(movie["title"])

            # Sort movie_list by movie ID
            movie_list.sort(key=lambda title: next(movie["id"] for movie in movies if movie["title"] == title))

            for title in movie_list[:5]:    
                print(title)
        
        case "build":
            # It should build the inverted index and save it to disk.
            # After doing so, it should print a message containing the first ID of the document
            # for the token 'merida' (which should be document 4651, "Brave").
            ii = InvertedIndex()
            ii.build(movies)
            ii.save()
            docs = ii.get_documents('merida')
            print(f"First document for token 'merida' = {docs[0]}") 

        case _:
            parser.print_help()





def find_one_token(query, title) -> bool:
    for query_token in query:
        # Full word match
        if query_token in title:
            return True
        
        # Partial match
        # for title_token in title:
        #     if query_token in title_token:
        #         return True
    return False


if __name__ == "__main__":
    main()
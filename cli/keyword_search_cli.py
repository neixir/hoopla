#!/usr/bin/env python3

import argparse, json
import string


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
        case _:
            parser.print_help()

    # CH1 L04-L05
    # https://www.boot.dev/lessons/c836a818-eb0b-4d65-94f5-d8fba46db0e1
    movies = {}
    movie_list = []
    with open("data/movies.json", "r") as f:
        contents = json.load(f)
        movies = contents["movies"]
        
        
    # Stopwords
    with open("data/stopwords.txt", "r") as f:
        stopwords = f.read()
        stopwords_list = stopwords.splitlines()     
        
    
    clean_query = clean_string(args.query)
    tokenized_query = tokenize_string(clean_query)
    tokenized_query = remove_stopwords(stopwords_list, tokenized_query)
    
    for movie in movies:
        tokenized_title = tokenize_string(clean_string(movie["title"]))
        tokenized_title = remove_stopwords(stopwords_list, tokenized_title)
        token_exists = find_one_token(tokenized_query, tokenized_title)
        if token_exists:
            movie_list.append(movie["title"])

    # Sort movie_list by movie ID
    movie_list.sort(key=lambda title: next(movie["id"] for movie in movies if movie["title"] == title))

    for title in movie_list[:5]:    
        print(title)


def clean_string(s) -> str:
    return s.lower().translate(str.maketrans('', '', string.punctuation))


def tokenize_string(s) -> list[str]:
    s = " ".join(s.split())
    return s.split(" ")


def find_one_token(query, title) -> bool:
    for token in query:
        if token in title:
            return True
    return False

def remove_stopwords(words, query) -> list[str]:
    removed = []
    for token in query:
        if token not in words:
            removed.append(token)
    
    return removed
            

if __name__ == "__main__":
    main()
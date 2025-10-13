#!/usr/bin/env python3

import argparse, json, string
from nltk.stem import PorterStemmer


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
    stopwords_list = []
    with open("data/stopwords.txt", "r") as f:
        stopwords = f.read()
        stopwords_list = stopwords.splitlines()     
        
    
    tokenized_query = tokenize_string(args.query, stopwords_list)

    print (f"Tokenized query: {tokenized_query}\n")
    
    for movie in movies:
        tokenized_title = tokenize_string(movie["title"], stopwords_list)
        # print (f"Tokenized title: {tokenized_title}")

        token_exists = find_one_token(tokenized_query, tokenized_title)
        if token_exists:
            movie_list.append(movie["title"])

    # Sort movie_list by movie ID
    movie_list.sort(key=lambda title: next(movie["id"] for movie in movies if movie["title"] == title))

    for title in movie_list[:5]:    
        print(title)


def clean_string(s) -> str:
    return s.lower().translate(str.maketrans('', '', string.punctuation))


def separate_words(s) -> list[str]:
    s = " ".join(s.split())
    return s.split(" ")


def remove_stopwords(query, words) -> list[str]:
    removed = []
    for token in query:
        if token not in words:
            removed.append(token)
    
    return removed


def tokenize_string(text, stopwords) -> list[str]:
    tokens = []

    # Lower case and remove punctuation
    s = clean_string(text)

    # Convert string to list of words
    words = separate_words(s)
    
    # Remove stopwords
    words = remove_stopwords(words, stopwords)

    # Stemming
    stemmer = PorterStemmer()
    for word in words:
        tokens.append(stemmer.stem(word, False))

    return tokens


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
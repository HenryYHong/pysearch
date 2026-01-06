import argparse
import json
import sys

from pysearch.indexer import build_index
from pysearch.searcher import search_with_snippets  # adjust if yours lives elsewhere


def load_jsonl(path: str):
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{line_num} invalid JSON: {e}") from e
            if "id" not in obj or "text" not in obj:
                raise ValueError(f"{path}:{line_num} must contain keys 'id' and 'text'")
            docs.append((int(obj["id"]), str(obj["text"])))
    return docs


def print_results(results):
    if not results:
        print("(no results)")
        return
    for rank, r in enumerate(results, start=1):
        print(f"{rank}. doc_id={r['doc_id']}")
        print(f"   {r['snippet']}")
        print()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pysearch", description="Tiny search engine CLI")
    parser.add_argument("path", help="Path to a .jsonl file of documents")
    parser.add_argument("-k", type=int, default=10, help="Number of results to return")
    parser.add_argument("--method", choices=["tf", "tfidf"], default="tf", help="Scoring method")
    parser.add_argument("--window", type=int, default=30, help="Snippet window size")
    parser.add_argument("-q", "--query", help="One-shot query (otherwise interactive if --interactive)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")

    args = parser.parse_args(argv)

    docs = load_jsonl(args.path)
    index, docstore = build_index(docs)

    # one-shot query
    if args.query is not None:
        results = search_with_snippets(
            index, docstore, args.query, k=args.k, method=args.method, window=args.window
        )
        print_results(results)
        return 0

    # interactive
    if args.interactive:
        print("pysearch interactive mode. Type :quit to exit.")
        while True:
            try:
                q = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not q:
                continue
            if q in {":q", ":quit", "quit", "exit"}:
                break
            results = search_with_snippets(
                index, docstore, q, k=args.k, method=args.method, window=args.window
            )
            print_results(results)
        return 0

    # if neither query nor interactive, show help
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

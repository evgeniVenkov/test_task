import argparse
import sys
import work_csv
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", required=True)
    parser.add_argument("--where")
    parser.add_argument("--aggregate")

    return parser.parse_args()

def main():
    args = parse_args()
    result = work_csv.read_csv(args.file)

    if args.where:
        result = work_csv.where_dict(result, args.where)
    if args.aggregate:
        result = work_csv.aggregate(result, args.aggregate)
        print(result)
    table = tabulate(result, headers="keys", tablefmt="grid")
    print(table)
if __name__ == "__main__":
    main()

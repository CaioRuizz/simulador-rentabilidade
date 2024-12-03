#!./.venv/bin/python

import argparse

def main():
    parser = argparse.ArgumentParser(description="ETL Process")
    parser.add_argument('--mode', choices=['initial', 'incremental'], required=True, help="Tipo de carga: inicial ou incremental")
    args = parser.parse_args()

    print(args)

if __name__ == "__main__":
    main()
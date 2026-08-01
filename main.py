import argparse
import json
import logging
from sys import stderr
from typing import Optional

from oj_toolkit.logging.consts import LOG_FORMAT
from oj_toolkit.parsing.consts import TimeFormats

from query_kibana.main import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--api-key',
        default=None,
        type=str,
        required=True,
        help='The API key',
        dest='api_key',
    )
    parser.add_argument(
        '--domain',
        default='example.com',
        type=str,
        required=True,
        help='The FQDN for your API (not full URL)',
    )
    parser.add_argument(
        '--index',
        default='asset-*',
        type=str,
        required=False,
        help='The name of the kibana index to query',
    )
    parser.add_argument(
        '--proxies',
        type=str,
        required=False,
        help="JSON structure specifying 'http' and 'https' proxy URLs",
    )
    parser.add_argument(
        '--log-level',
        type=int,
        required=False,
        help="0 (NOTSET) - 50 (CRITICAL)",
        default=logging.INFO,
        dest='log_level',
    )

    args = parser.parse_args()

    logging.basicConfig(
        format=LOG_FORMAT,
        level=args.log_level,
        datefmt=TimeFormats.date_and_time.value,
        stream=stderr,
    )

    proxies: Optional[dict] = None
    if proxies:
        try:
            proxies: dict = json.loads(args.proxies)
        except Exception as exc_json:
            print(
                f'WARNING: failure parsing proxies: {exc_json}: proxies provided: {proxies}'
            )

    print('[')
    for result in main(domain=args.domain, index=args.index, api_key=args.api_key, proxies=proxies):
        print(f'{json.dumps(result, indent=4)},')
    print(']')

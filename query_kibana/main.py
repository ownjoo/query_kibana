import logging
from typing import Generator, Optional

from oj_toolkit.parsing.types import dig
from oj_toolkit.logging.decorators import timed_generator
from requests import Response, Session
from urllib3 import Retry

from query_kibana.consts import RETRY_COUNT, RETRY_BACKOFF_FACTOR, PAGE_SIZE

logger = logging.getLogger(__name__)

S: Optional[Session] = None

def get_pit(url: str, index: str):
    r: Response = S.post(
        url=url,
        params={
            'method': 'POST',
            'path': f'{index}/_pit?keep_alive=1m'
        },
    )
    r.raise_for_status()
    return dig(src=r.json(), path='id', exp=str)


@timed_generator(log_progress=False, log_level=logging.DEBUG, logger=logger)
def list_results(
        url: str,
        index: str,
        additional_params: Optional[dict] = None,
) -> Generator[dict, None, None]:
    params: dict = {
        'method': 'GET',
        'path': '_search'
    }
    json: dict = {
        'size': PAGE_SIZE,
        'pit': {
            'id': get_pit(url=url, index=index),
            'keep_alive': '1m',
        },
        'sort': [{"_shard_doc": "desc"}],
        'track_total_hits': False,
    }
    if isinstance(additional_params, dict):
        params.update(additional_params)

    last_sort: str = "let's try at least once"
    while last_sort:
        r: Response = S.get(url, params=params, json=json)
        r.raise_for_status()
        hits: list = dig(src=r.json(), path='hits.hits', exp=list, default=[])
        yield from hits
        if last_sort := dig(src=hits, path='[-1].sort[0]', exp=str, default=None):
            json['search_after'] = [last_sort]


def main(
    domain: str,
    api_key: str,
    index: str = 'asset-*',
    proxies: Optional[dict] = None,
) -> Generator[dict, None, None]:
    global S
    S = Session()

    if isinstance(proxies, dict):
        S.proxies = proxies

    headers: dict = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'ApiKey {api_key}',
        'kbn-xsrf': 'true',
    }
    S.headers.update(headers)
    S.verify = False
    for adapter in S.adapters.values():
        adapter.max_retries = Retry(
            total=RETRY_COUNT,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=[429, 502, 503, 504],
            respect_retry_after_header=True,
        )

    return list_results(url=f'{domain}/api/console/proxy', index=index)

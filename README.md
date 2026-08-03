# template_cli

[![License](https://img.shields.io/github/license/ownjoo/query_kibana)](LICENSE)
[![Top language](https://img.shields.io/github/languages/top/ownjoo/query_kibana)](https://github.com/ownjoo/query_kibana) [![Stars](https://img.shields.io/github/stars/ownjoo/query_kibana)](https://github.com/ownjoo/query_kibana/stargazers) [![Forks](https://img.shields.io/github/forks/ownjoo/query_kibana)](https://github.com/ownjoo/query_kibana/forks) [![Issues](https://img.shields.io/github/issues/ownjoo/query_kibana)](https://github.com/ownjoo/query_kibana/issues) [![Pull requests](https://img.shields.io/github/issues-pr/ownjoo/query_kibana)](https://github.com/ownjoo/query_kibana/pulls)
test query API:

# usage
```
$ python path/to/dir/main.py --help
usage: main.py [-h] --client-id CLIENT_ID --client-secret CLIENT_SECRET --domain DOMAIN [--proxies PROXIES]

options:
  -h, --help                     show this help message and exit
  --client-id CLIENT_ID          The client_id of the API key
  --client-secret CLIENT_SECRET  The API key
  --domain DOMAIN                The FQDN for your Crowdstrike account's API (not full URL)
  --proxies PROXIES              JSON structure specifying 'http' and 'https' proxy URLs
```

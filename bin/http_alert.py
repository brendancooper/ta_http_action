# encoding = utf-8
import logging
import json
import re
import requests
import sys

logging.root
logging.root.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s %(message)s')
handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(formatter)
logging.root.addHandler(handler)


def helper_get_requests_func(method):
    method = method.lower()
    if method == "post":
        return requests.post
    elif method == "get":
        return requests.get
    elif method == "delete":
        return requests.delete
    elif method == "patch" :
        return requests.patch
    elif method == "put":
        return requests.put

def process(data):
    configuration = data['configuration']
    results = data['result']

    endpoint = configuration.get('endpoint')
    input_custom_headers = configuration.get('custom_headers')
    payload = configuration.get('payload')
    method = configuration.get('method')
    qs_params = {}
    input_qs_params = configuration.get('qs_params')
    proxies = {}
    proxies['https'] = configuration.get('proxy')
    timeout = 30
    custom_headers = {}
    requests_func = helper_get_requests_func(method)

    if input_custom_headers is not None and len(input_custom_headers) > 0:
        header_dict = input_custom_headers.split(',')
        if len(header_dict) > 0:
            for value in header_dict:
                key, value = value.split('=')
                custom_headers[key]=value
    else:
        custom_headers=None

    if input_qs_params is not None and len(input_qs_params) > 0:
        #logging.error("input_qs_params %s" % input_qs_params)
        params_dict = input_qs_params.split(',')
        #logging.error("params_dict %s" % params_dict)
        if len(params_dict) > 0:
            for value in params_dict:
                key, value = value.split('=')
                qs_params[key]=value
            logging.error("Params %s" % json.dumps(qs_params))
    else:
        qs_params=None

    if not endpoint.startswith("https://"):
        logging.info("ERROR httpalert job={} endpoint={} endpoint does not start https:// ".format(data['sid'],endpoint))
        return

    response = requests_func(endpoint, params=qs_params, data=payload, headers=custom_headers, timeout=timeout,proxies=proxies)
    logging.info("httpalert Job={} endpoint={} status_code={} ".format(data['sid'],endpoint,response.status_code))

if len(sys.argv) > 1 and sys.argv[1] == "--execute":
    data = json.load(sys.stdin)
    process(data)
    pass

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    data = {
        "configuration" : {
            'endpoint' : "https://example.com/post",
            'method' : "post",
            'qs_params' : "test=true",
            'payload' : "This is the body"
        },
        "result" : {
            'count' : "2323",
            'name' : "Hello",
        }
    }
    process(data)

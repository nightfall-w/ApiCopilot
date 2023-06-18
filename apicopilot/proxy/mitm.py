import json
import logging

from mitmproxy import http
from mitmproxy.tools.main import mitmdump

FilterHost = []
ContentType = []


def handle_form(data: str):
    """
    处理 Content-Type:    application/x-www-form-urlencoded
    默认生成的数据 username=admin&password=123456
    :param data: 获取的data 类似这样  username=admin&password=123456
    :return:
    """
    data_dict = {}
    if data.startswith('{') and data.endswith('}'):
        return data
    try:
        for i in data.split('&'):
            data_dict[i.split('=')[0]] = i.split('=')[1]
        return json.dumps(data_dict)
    except IndexError:
        return ''


def request(flow: http.HTTPFlow) -> None:
    if not FilterHost or flow.request.host in FilterHost:
        logging.info(f"符合过滤条件Request URL: {flow.request.url}")


def response(flow: http.HTTPFlow):
    """
    对拦截的请求做response的处理
    :param flow:
    :return:
    """
    if not FilterHost or flow.request.host in FilterHost:
        try:
            token = flow.request.headers["Authorization"]
        except KeyError:
            token = ''
        header = json.dumps({"Authorization": token})
        data = flow.request.text
        method = flow.request.method.lower()
        url = flow.request.url
        try:
            content_type = flow.request.headers['Content-Type']
        except KeyError:
            content_type = ''
        if 'form' in content_type:
            data_type = "data"
        elif 'json' in content_type:
            data_type = 'json'
        else:
            data_type = 'params'
            if '?' in url:
                data = url.split('?')[1]
                data = handle_form(data)
        # 预期结果
        # expect = json.loads(flow.response.text)

        # 日志
        logging.info(url)
        logging.info(header)
        logging.info(content_type)
        logging.info(method)
        logging.info(data)
        logging.info(flow.response.text)
    else:
        pass


def start(port: int, filter_host=None, content_type=None):
    if content_type and isinstance(content_type, list):
        global ContentType
        ContentType = content_type
    if filter_host and isinstance(filter_host, list):
        global FilterHost
        FilterHost = filter_host
    args = ["-s", __file__, "-p", str(port)]
    mitmdump(args)


if __name__ == "__main__":
    start(port=8080)

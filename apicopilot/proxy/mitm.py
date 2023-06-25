import json
import logging
from typing import Optional

from mitmproxy import ctx
from mitmproxy import exceptions
from mitmproxy import http
from mitmproxy.tools.main import mitmdump, mitmweb


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


def start(port: int, filter_host=None, content_type=None):
    logging.info(f'筛选指定host:{filter_host}')
    args = ["-s", __file__, "-p", str(port), "--set", f'filter_domain={filter_host}']
    mitmweb(args)


class ProxyHandle:
    def load(self, loader):
        loader.add_option(
            name="filter_domain",
            typespec=Optional[str],
            default=None,
            help="Add a filter domain list",
        )

    def configure(self, updates):
        if "filter_domain" in updates:
            if ctx.options.filter_domain is not None and not isinstance(eval(ctx.options.filter_domain), list):
                raise exceptions.OptionsError("filter_domain must is list!!!")

    def request(self, flow) -> None:
        if not ctx.options.filter_domain or flow.request.host in eval(ctx.options.filter_domain):
            logging.info(f"符合过滤条件Request URL: {flow.request.url}")

    def response(self, flow):
        """
        对拦截的请求做response的处理
        :param flow:
        :return:
        """
        if True:
            # if not ctx.options.filter_domain or flow.request.host in eval(ctx.options.filter_domain):

            method = flow.request.method.upper()
            url = flow.request.url
            cookie = {"cookie": ""}
            for header_item in flow.request.headers.fields:
                if header_item[0] == b'cookie':
                    cookie['cookie'] += header_item[1].decode() + ';'
            headers = {header_item[0].decode(): header_item[1].decode() for header_item in flow.request.headers.fields
                       if
                       header_item[0] != b'cookie'}
            if cookie['cookie']:
                headers.update(cookie)
            logging.info(url)
            logging.info(method)
            logging.info(headers)
            query = flow.request.query
            body = flow.request.text
            if query:
                query = url.split('?')[1]
                query = handle_form(query)
                logging.info(f'query:{query}')
            if body:
                logging.info(f"body：{body}")

            # 日志
            if url == "https://master.weimob.com/api3/cms/mgr/navigate/batchGetNavigate":
                response_data = r"""{"errcode":"0","errmsg":"处理成功","data":{"pageNum":1,"pageSize":10,"totalCount":18,"pageList":[{"specificationVersion":1,"wid":null,"operationSource":null,"basicInfo":{"merchantId":null,"bosId":null,"vid":null,"vidType":null,"productId":null,"productVersionId":null,"productInstanceId":null,"mallVersionType":null,"cid":null,"globalvid":null,"tcode":"weimob"},"i18n":{"language":null,"timezone":null},"extendInfo":{"source":null,"refer":null,"userIp":null,"ocdAppId":null,"uuid":null,"wxTemplateId":null,"mpScene":null,"deviceInfo":null},"originProductId":null,"originProductInstanceId":null,"bizVid":null,"bizVidType":null,"title":"App式导航-通用什么玩意","style":1,"navigateIconStyle":1,"navigateBackgroundType":null,"navigateBackgroundColor":"#FFFFFF","backgroundRound":3,"colorStyle":1,"colorStyleDTO":{"bgColor":"#FFFFFF","textColor":"#0a57b3","iconColor":"#0a57b3","notSelectBgColor":null,"notSelectTextColor":"#212121","notSelectIconColor":"#212121","systemBgColor":null,"systemTextColor":null,"systemIconColor":null,"systemSelectColor":"#FA2C19","systemNotSelectColor":"#212121"},"menuCount":5,"navigateJson":"{\"items\": [{\"url\": \"\", \"name\": \"首页\", \"sign\": \"\", \"type\": 1, \"image\": {\"url\": \"tabbar-home\", \"type\": 1, \"selectIconUrl\": \"tabbar-home-selected\"}, \"refer\": \"cms-index\", \"title\": \"首页\", \"iconSize\": \"\", \"urlBizId\": null, \"selectedList\": [{\"cid\": 128193553, \"org\": {\"vid\": 6015090063553, \"vidType\": 2, \"accessType\": 1}, \"product\": {\"name\": \"店铺\", \"version\": 30044, \"productId\": 1, \"versionName\": \"店铺-智慧零售标准版\", \"productUniqueId\": \"1-6015090063553-1\", \"productInstanceId\": 1324860553}, \"category\": {\"id\": 276, \"name\": \"功能页面\", \"sort\": 2, \"type\": 1, \"category\": 1, \"parentId\": 0, \"isDeleted\": 0, \"categoryId\": 276, \"subCategory\": [], \"containsPage\": null, \"parentCategory\": null, \"sourceProductId\": 1, \"categoryUniqueId\": \"276-6015090063553-1\"}, \"linkList\": [{\"bizId\": \"215\", \"refer\": \"cms-index\", \"title\": \"首页\", \"bizParam\": {\"cid\": 128193553, \"vid\": 6015090063553, \"bosId\": 4020413689553}, \"children\": [], \"pageName\": \"首页\", \"uniqueId\": \"1-128193553-6015090063553-cms-index-215\", \"canSelect\": true, \"fieldList\": [{\"color\": null, \"field\": \"pageName\", \"value\": \"首页\"}], \"description\": null, \"urlInfolist\": [{\"url\": \"/cms_design/index?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.cms.n.weimob.com/bos/cms/128193553/0/1324860553/design/index?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/qly4I\"}, {\"url\": \"/cms_design/index?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/cms_design/index?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}]}]}], \"decorationUrl\": {\"appId\": \"wxfc73dc3648713d6d\", \"h5Url\": \"https://128193553.cms.n.weimob.com/bos/cms/128193553/0/1324860553/design/index?bizVid=6015090063553\", \"miniUrl\": \"/cms_design/index?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"bizParam\": {\"cid\": 128193553, \"vid\": 6015090063553, \"bosId\": 4020413689553}, \"linkName\": \"首页\", \"linkType\": 1}, \"decorationUrlList\": [{\"url\": \"/cms_design/index?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.cms.n.weimob.com/bos/cms/128193553/0/1324860553/design/index?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/qly4I\"}, {\"url\": \"/cms_design/index?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/cms_design/index?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}], \"subNavigationList\": []}, {\"url\": \"\", \"name\": \"商品分类页\", \"sign\": \"\", \"type\": 1, \"image\": {\"url\": \"tabbar-classify\", \"type\": 1, \"selectIconUrl\": \"tabbar-classify-selected\"}, \"refer\": \"ec-shop-classify\", \"title\": \"分类\", \"iconSize\": \"\", \"urlBizId\": null, \"selectedList\": [{\"cid\": 128193553, \"org\": {\"vid\": 6015090063553, \"vidType\": 2, \"accessType\": 1}, \"product\": {\"name\": \"商城\", \"version\": 12010, \"productId\": 145, \"versionName\": \"商城连锁-PE\", \"productUniqueId\": \"145-6015090063553-1\", \"productInstanceId\": 1324859553}, \"category\": {\"id\": 279, \"name\": \"功能页面\", \"sort\": 1, \"type\": 1, \"category\": 1, \"parentId\": 0, \"isDeleted\": 0, \"categoryId\": 279, \"subCategory\": [], \"containsPage\": null, \"parentCategory\": null, \"sourceProductId\": 145, \"categoryUniqueId\": \"279-6015090063553-1\"}, \"linkList\": [{\"bizId\": \"318\", \"refer\": \"ec-shop-classify\", \"title\": \"商品分类页\", \"bizParam\": {\"cid\": 128193553, \"vid\": 6015090063553, \"bosId\": 4020413689553}, \"children\": [], \"pageName\": \"商品分类页\", \"uniqueId\": \"1-128193553-6015090063553-ec-shop-classify-318\", \"canSelect\": true, \"fieldList\": [{\"color\": null, \"field\": \"pageName\", \"value\": \"商品分类页\"}], \"description\": null, \"urlInfolist\": [{\"url\": \"/ec_shop/classify?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/goods/classify/index?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/e5AXO\"}, {\"url\": \"/ec_shop/classify?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/ec_shop/classify?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}]}]}], \"decorationUrl\": {\"appId\": \"wxfc73dc3648713d6d\", \"h5Url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/goods/classify/index?bizVid=6015090063553\", \"miniUrl\": \"/ec_shop/classify?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"bizParam\": {\"cid\": 128193553, \"vid\": 6015090063553, \"bosId\": 4020413689553}, \"linkName\": \"商品分类页\", \"linkType\": 1}, \"decorationUrlList\": [{\"url\": \"/ec_shop/classify?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/goods/classify/index?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/e5AXO\"}, {\"url\": \"/ec_shop/classify?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/ec_shop/classify?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}], \"subNavigationList\": []}, {\"url\": \"\", \"name\": \"全部商品列表\", \"sign\": \"\", \"type\": 1, \"image\": {\"url\": \"tabbar-news\", \"type\": 1, \"selectIconUrl\": \"tabbar-news-selected\"}, \"refer\": \"ec-goods-list\", \"title\": \"全部商品\", \"iconSize\": \"\", \"urlBizId\": null, \"selectedList\": [{\"cid\": 128193553, \"org\": {\"vid\": 6015090063553, \"vidType\": 2, \"accessType\": 1}, \"product\": {\"name\": \"商城\", \"version\": 12010, \"productId\": 145, \"versionName\": \"商城连锁-PE\", \"productUniqueId\": \"145-6015090063553-1\", \"productInstanceId\": 1324859553}, \"category\": {\"id\": 281, \"name\": \"商品列表\", \"sort\": 2, \"type\": 1, \"category\": 1, \"parentId\": 0, \"isDeleted\": 0, \"categoryId\": 281, \"subCategory\": [], \"containsPage\": null, \"parentCategory\": null, \"sourceProductId\": 145, \"categoryUniqueId\": \"281-6015090063553-1\"}, \"linkList\": [{\"bizId\": \"0\", \"refer\": \"ec-goods-list\", \"title\": \"全部商品列表\", \"bizParam\": {}, \"children\": [], \"uniqueId\": \"1-128193553-6015090063553-ec-goods-list-0\", \"canSelect\": true, \"fieldList\": [{\"color\": null, \"field\": \"name\", \"value\": \"全部商品列表\"}], \"description\": null, \"urlInfolist\": [{\"url\": \"/ec_shop/goods?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/goods/list/index?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/E1x1I\"}, {\"url\": \"/ec_shop/goods?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/ec_shop/goods?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}]}]}], \"decorationUrl\": {\"appId\": \"wxfc73dc3648713d6d\", \"h5Url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/goods/list/index?bizVid=6015090063553\", \"miniUrl\": \"/ec_shop/goods?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"bizParam\": {}, \"linkName\": \"全部商品列表\", \"linkType\": 1}, \"decorationUrlList\": [{\"url\": \"/ec_shop/goods?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/goods/list/index?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/E1x1I\"}, {\"url\": \"/ec_shop/goods?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/ec_shop/goods?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}], \"subNavigationList\": []}, {\"url\": \"\", \"name\": \"购物车\", \"sign\": \"\", \"type\": 1, \"image\": {\"url\": \"tabbar-shopcart\", \"type\": 1, \"selectIconUrl\": \"tabbar-shopcart-selected\"}, \"refer\": \"ec-cart\", \"title\": \"购物车\", \"iconSize\": \"\", \"urlBizId\": null, \"selectedList\": [{\"cid\": 128193553, \"org\": {\"vid\": 6015090063553, \"vidType\": 2, \"accessType\": 1}, \"product\": {\"name\": \"商城\", \"version\": 12010, \"productId\": 145, \"versionName\": \"商城连锁-PE\", \"productUniqueId\": \"145-6015090063553-1\", \"productInstanceId\": 1324859553}, \"category\": {\"id\": 279, \"name\": \"功能页面\", \"sort\": 1, \"type\": 1, \"category\": 1, \"parentId\": 0, \"isDeleted\": 0, \"categoryId\": 279, \"subCategory\": [], \"containsPage\": null, \"parentCategory\": null, \"sourceProductId\": 145, \"categoryUniqueId\": \"279-6015090063553-1\"}, \"linkList\": [{\"bizId\": \"236\", \"refer\": \"ec-cart\", \"title\": \"购物车\", \"bizParam\": {\"cid\": 128193553, \"vid\": 6015090063553, \"bosId\": 4020413689553}, \"children\": [], \"pageName\": \"购物车\", \"uniqueId\": \"1-128193553-6015090063553-ec-cart-236\", \"canSelect\": true, \"fieldList\": [{\"color\": null, \"field\": \"pageName\", \"value\": \"购物车\"}], \"description\": null, \"urlInfolist\": [{\"url\": \"/ec_cart/index?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/cart/index?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/e5AXY\"}, {\"url\": \"/ec_cart/index?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/ec_cart/index?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}]}]}], \"decorationUrl\": {\"appId\": \"wxfc73dc3648713d6d\", \"h5Url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/cart/index?bizVid=6015090063553\", \"miniUrl\": \"/ec_cart/index?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"bizParam\": {\"cid\": 128193553, \"vid\": 6015090063553, \"bosId\": 4020413689553}, \"linkName\": \"购物车\", \"linkType\": 1}, \"decorationUrlList\": [{\"url\": \"/ec_cart/index?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.shop.n.weimob.com/bos/shop/128193553/0/1324859553/cart/index?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/e5AXY\"}, {\"url\": \"/ec_cart/index?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/ec_cart/index?productInstanceId=1324859553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}], \"subNavigationList\": []}, {\"url\": \"\", \"name\": \"用户中心\", \"sign\": \"\", \"type\": 1, \"image\": {\"url\": \"tabbar-my\", \"type\": 1, \"selectIconUrl\": \"tabbar-my-selected\"}, \"refer\": \"cms-usercenter\", \"title\": \"我的\", \"iconSize\": \"\", \"urlBizId\": null, \"selectedList\": [{\"cid\": 128193553, \"org\": {\"vid\": 6015090063553, \"vidType\": 2, \"accessType\": 1}, \"product\": {\"name\": \"店铺\", \"version\": 30044, \"productId\": 1, \"versionName\": \"店铺-智慧零售标准版\", \"productUniqueId\": \"1-6015090063553-1\", \"productInstanceId\": 1324860553}, \"category\": {\"id\": 276, \"name\": \"功能页面\", \"sort\": 2, \"type\": 1, \"category\": 1, \"parentId\": 0, \"isDeleted\": 0, \"categoryId\": 276, \"subCategory\": [], \"containsPage\": null, \"parentCategory\": null, \"sourceProductId\": 1, \"categoryUniqueId\": \"276-6015090063553-1\"}, \"linkList\": [{\"bizId\": \"385\", \"refer\": \"cms-usercenter\", \"title\": \"用户中心\", \"bizParam\": {\"cid\": 128193553, \"vid\": 6015090063553, \"bosId\": 4020413689553}, \"children\": [], \"pageName\": \"用户中心\", \"uniqueId\": \"1-128193553-6015090063553-cms-usercenter-385\", \"canSelect\": true, \"fieldList\": [{\"color\": null, \"field\": \"pageName\", \"value\": \"用户中心\"}], \"description\": null, \"urlInfolist\": [{\"url\": \"/cms_design/usercenter?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.cms.n.weimob.com/bos/cms/128193553/0/1324860553/design/usercenter?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/qly4J\"}, {\"url\": \"/cms_design/usercenter?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/cms_design/usercenter?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}]}]}], \"decorationUrl\": {\"appId\": \"wxfc73dc3648713d6d\", \"h5Url\": \"https://128193553.cms.n.weimob.com/bos/cms/128193553/0/1324860553/design/usercenter?bizVid=6015090063553\", \"miniUrl\": \"/cms_design/usercenter?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"bizParam\": {\"cid\": 128193553, \"vid\": 6015090063553, \"bosId\": 4020413689553}, \"linkName\": \"用户中心\", \"linkType\": 1}, \"decorationUrlList\": [{\"url\": \"/cms_design/usercenter?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": \"wxfc73dc3648713d6d\", \"channel\": 1, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"https://128193553.cms.n.weimob.com/bos/cms/128193553/0/1324860553/design/usercenter?bizVid=6015090063553\", \"appId\": null, \"channel\": 0, \"linkType\": 1, \"shortUrl\": \"http://t.weimob.com/qly4J\"}, {\"url\": \"/cms_design/usercenter?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 21, \"linkType\": 1, \"shortUrl\": null}, {\"url\": \"/cms_design/usercenter?productInstanceId=1324860553&vid=0&bizVid=6015090063553\", \"appId\": null, \"channel\": 25, \"linkType\": 1, \"shortUrl\": null}], \"subNavigationList\": []}], \"style\": 1}","jsonDTO":null,"idList":null,"id":12759411,"pageIdList":null,"isDefault":1,"updateTime":"2022-04-28 23:29:05","isAssociatedPage":1,"pageType":1,"iconStyleType":1,"pageNameList":null}]},"globalTicket":"1687324767.200-0.0.0.0-5887981509","monitorTrackId":null}"""
                flow.response = http.Response.make(
                    200,  # (optional) status code
                    response_data,  # (optional) content
                    {"Content-Type": "application/json;charset=UTF-8"}  # (optional) headers
                )

            logging.info(flow.response.text)
            logging.info('end')


addons = [ProxyHandle()]

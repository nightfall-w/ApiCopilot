"""
存储捕获流量到 MongoDB
"""

from pymongo import MongoClient

DBName = "ApiProxyData"
MongoHost = "127.0.0.1"
MongoPORT = 27017


class MongoEngine:
    """
    mongo引擎 处理与MongoDB的交互
    """

    def __init__(self, db_name=DBName):
        self.db_name = db_name
        self.client = MongoClient(host=MongoHost,
                                  port=MongoPORT,
                                  username=None,
                                  password=None
                                  )
        self.db_handle = self.get_db_handle()

    def get_db_handle(self):
        """
        获取db连接器
        :return: db_handle
        """
        db_handle = self.client[self.db_name]
        return db_handle

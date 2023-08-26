import inspect
import logging

import requests

from ..constants import XStatusCode
from ..exceptions import RetryException, XClientException
from ..helpers import to_text
from ..session.memorystorage import MemoryStorage
from ..settings import Setting
from .base import BaseClient
from . import order


def _is_api_endpoint(obj):
    return isinstance(obj, BaseClient)


class XClient:

    _SESSION_NAME = "X_SESSION"

    # 示例
    order_create = order.OrderCreate()
    order_delete = order.OrderDelete()

    def __new__(cls, *args, **kwargs):
        self = super(XClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(
        self,
        url,
        account,
        password,
        *,
        session_storage=None,
        session_name=None,
        auto_retry=True,
        settings=None,
    ):
        self.url = url
        self.account = account
        self.password = password
        self.session_name = session_name or self._SESSION_NAME
        self.session_storage = session_storage or MemoryStorage()
        self.auto_retry = auto_retry

        self.settings = settings or Setting()

        self._http = requests.session()

    def _post(self, path, **kwargs):
        logger = logging.getLogger(__name__)

        url = f"{self.url}{path}"

        logger.info(f"BEGIN:url:{url}, params:{kwargs}")
        resp = self._http.post(url, **kwargs)
        logger.info(f"END:url:{url}, status:{resp.status_code}, " f"body:{resp.text}")

        try:
            resp.raise_for_status()
        except requests.RequestException:
            raise XClientException(
                errcode=None, errmsg=None, request=resp.request, response=resp
            )

        raw_response = self.settings.raw_response
        return self._handler_result(resp, raw_response=raw_response)

    def _handler_result(self, response, *, raw_response=False):
        if raw_response:
            return response

        resp = response.json()

        code = resp.get("code") or resp.get("status")
        if code in (XStatusCode.SUCCESS,):
            return resp

        if self.auto_retry and code in {XStatusCode.UNAUTHORIZED}:
            # session无效，删除旧session, 重试
            del self.session
            raise RetryException

        errcode = resp.get("responseCode", "")
        errmsg = resp.get("message", "")
        raise XClientException(
            errcode, errmsg, request=response.request, response=response
        )

    @property
    def session(self):
        return to_text(self.session_storage.get(self.session_name))

    @session.setter
    def session(self, value):
        v, ttl = value
        self.session_storage.set(self.session_name, v, ttl=ttl)

    @session.deleter
    def session(self):
        self.session_storage.delete(self.session_name)
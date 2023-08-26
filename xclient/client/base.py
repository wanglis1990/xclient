from retrying import retry

from ..exceptions import RetryException


def need_retry(exception):
    return isinstance(exception, RetryException)


class BaseClient(object):
    def __init__(self, client=None):
        self._client = client

    @retry(stop_max_attempt_number=1, retry_on_exception=need_retry)
    def _post(self, path, **kwargs):
        kwargs.setdefault("timeout", 30)
        kwargs.setdefault("headers", {}).update(Authentication=self.session)
        return self._client._post(path, **kwargs)

    @property
    def company_code(self):
        return self._client.company_code

    @property
    def account(self):
        return self._client.account

    @property
    def password(self):
        return self._client.password

    @property
    def session(self):
        session = self._client.session
        if session:
            return session
        value = self.x_login()
        self._client.session = value
        return value[0]

    @session.deleter
    def session(self):
        del self._client.session

    def login(self):
        """登录X系统"""
        path = "/x/login"  # 根据实际需要修改

        params = {"account": self.account, "password": self.password}
        resp = self._client._post(path, data=params, timeout=30)

        # 根据实际需要修改
        return resp["accessToken"], resp["expiresIn"]

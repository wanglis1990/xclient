from contextlib import contextmanager

from werkzeug.local import Local


class Setting(object):

    timeout = 30

    raw_response = False

    _tls = Local()

    @contextmanager
    def __call__(self, **options):

        for key, value in options.items():
            setattr(self._tls, key, value)

        yield

        for key in options:
            delattr(self._tls, key)

    def __getattribute__(self, key):
        if key != "_tls" and hasattr(self._tls, key):
            return getattr(self._tls, key)
        return super().__getattribute__(key)

import six


def to_text(s, encoding='utf-8'):
    if not s:
        return ''
    if isinstance(s, six.text_type):
        return s
    if isinstance(s, six.binary_type):
        return s.decode(encoding)
    return six.text_type(s)
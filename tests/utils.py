import mock
from oauthlib.common import Request


class BaseTest(object):
    def set_client(self, request):
        request.client = mock.MagicMock()
        request.client.client_id = 'mocked'
        return True

    def make_request(self, response_type='code',
            scope='openid profile email', **kwargs):
        request = Request('https://a.b/path')

        request.scope = scope
        request.client = 'superman'
        request.client_id = 'abcdef'
        request.redirect_uri = 'https://a.b/'
        request.response_type = response_type

        for prop, val in kwargs.items():
            setattr(request, prop, val)

        return request

    def assertListEqual(self, list1, list2):
        return sorted(list1) == sorted(list2)

    def assertHasKeys(self, _dict, keys):
        keys = set(keys)
        dictkeys = set(_dict.keys())

        assert keys.issubset(dictkeys),\
               "Missing keys: %s" % ', '.join(keys.difference(dictkeys))

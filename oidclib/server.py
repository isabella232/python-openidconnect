# -*- coding: utf-8 -*-
from oauthlib.common import Request
from oauthlib.oauth2 import AuthorizationEndpoint

from oidblib.token import BearerToken
from oidclib.grant_types import AuthorizationCodeGrant, TokenEndpoint


class OpenIDConnectServer(AuthorizationEndpoint, TokenEndpoint):
    def __init__(self, request_validator, token_expires_in=None,
            token_generator=None, *args, **kwargs):
        auth_grant = AuthorizationCodeGrant(request_validator)
        # implicit_grant
        # hybrid_grant

        # refresh, etc
        bearer = BearerToken(request_validator, token_generator,
                expires_in=token_expires_in)

        # initializer of all mixins
        AuthorizationEndpoint.__init__(self, default_response_type='code',
                response_types={
                    'auth': auth_grant  # implicit and hybrid
                },
                default_token_type=bearer)
        TokenEndpoint.__init__(self, default_grant_type='authorization_code',
                grant_types={
                    'auth': auth_grant
                },
                default_token_type=bearer)

    def validate_authorization_request(self, uri, http_method='GET', body=None,
            headers=None):
        request = Request(uri, http_method=http_method, body=body, headers=headers)
        request.scopes = None
        flow = self.get_flow(request)
        response_type_handler = self.response_types[flow]
        return response_type_handler.validate_authorization_request(request)

    def get_flow(self, request):
        scopes = set((request.scope or '').split())

        if scopes == {'code'}:
            return 'auth'
        if scopes in [{'id_token'}, {'id_token', 'token'}]:
            return 'implicit'
        else:
            return 'hybrid'

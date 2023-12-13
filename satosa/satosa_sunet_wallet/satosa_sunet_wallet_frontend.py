import logging

from typing import Dict

from urllib.parse import urlencode, urlparse

import satosa.logging_util as lu
from satosa.frontends.base import FrontendModule
from satosa.response import Response


from satosa.internal import InternalData


logger = logging.getLogger(__name__)


class WalletFrontend(FrontendModule):
    """
    SUNET satosa wallet frontend
    """

    def __init__(self, auth_req_callback_func, internal_attributes, config, base_url, name):
        super().__init__(auth_req_callback_func, internal_attributes, base_url, name)

        self.config = config


    def _handle_request_fields(self, request: str) -> Dict[str, str]:
        ret: Dict[str, str] = {}

        if ("&") in request:
            for arg in request.split("&"):
                ret[arg.split("=")[0]] = arg.split("=")[1]
        elif ("=") in request:
            ret[request.split("=")[0]] = request.split("=")[1]

        return ret

    def handle_authn_request(self, context):
        """
        Handle an authentication request and pass it on to the backend.
        :type context: satosa.context.Context
        :rtype: oic.utils.http_util.Response

        :param context: the current context
        :return: HTTP response to the client
        """
        # internal_req = self._handle_authn_request(context)
        # if not isinstance(internal_req, InternalData):
        #     return internal_req
        #return self.auth_req_callback_func(context, internal_req)


        request = urlencode(context.request)
        msg = "vvv Authn req from client: {}".format(request)
        logline = lu.LOG_FMT.format(id=lu.get_session_id(context.state), message=msg)
        logger.debug(logline)
        print(logline)


        request_args = self._handle_request_fields(request)
        
        # client_id = authn_req["client_id"]
        # context.state[self.name] = {"oidc_request": request}
        # subject_type = self.provider.clients[client_id].get("subject_type", "pairwise")
        # client_name = self.provider.clients[client_id].get("client_name")
        # if client_name:
        #     # TODO should process client names for all languages, see OIDC Registration, Section 2.1
        #     requester_name = [{"lang": "en", "text": client_name}]
        # else:
        #     requester_name = None



        client_id = request_args["client_id"]
        client_name = request_args["client_name"]
        client_number = request_args["client_number"]
        subject_type = request_args["subject_type"]
        if client_name:
            requester_name = [{"lang": "en", "text": client_name}]
        else:
            requester_name = None


        internal_req = InternalData(
            subject_type=subject_type,
            requester=client_id,
            requester_name=requester_name,
            # attributes={"name": requester_name, "number": client_number},
            attributes={"name": client_name, "number": client_number},
        )

        if not isinstance(internal_req, InternalData):
            return internal_req
        return self.auth_req_callback_func(context, internal_req)
        
    def handle_authn_response(self, context, internal_resp):
        """
        See super class method satosa.frontends.base.FrontendModule#handle_authn_response
        :type context: satosa.context.Context
        :type internal_response: satosa.internal.InternalData
        :rtype: satosa.response.Response
        """
        raise NotImplementedError()

    def handle_backend_error(self, exception):
        """
        See super class satosa.frontends.base.FrontendModule
        :type exception: satosa.exception.SATOSAError
        :rtype: satosa.response.Response
        """
        raise NotImplementedError()

    def register_endpoints(self, backend_names):
        """
        See super class satosa.frontends.base.FrontendModule
        :type backend_names: list[str]
        :rtype: list[(str, ((satosa.context.Context, Any) -> satosa.response.Response, Any))]
        :raise ValueError: if more than one backend is configured
        """
        url_map = [("^{}".format(self.name), self.handle_authn_request)]

        return url_map

    def ping_endpoint(self, context):
        """
        :type context: satosa.context.Context
        :rtype: satosa.response.Response
        """
        msg = "Ping returning 200 OK"
        logline = lu.LOG_FMT.format(id=lu.get_session_id(context.state), message=msg)
        logger.debug(logline)

        msg = " "
        return Response(msg)

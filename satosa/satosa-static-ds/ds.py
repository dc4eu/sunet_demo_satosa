import logging
from base64 import urlsafe_b64encode as b64encode
from base64 import urlsafe_b64decode as b64decode
from json import dumps as json_dumps
from json import loads as json_loads
from re import sub as reg_replace

from satosa.context import Context
from satosa.internal import InternalData
from satosa.micro_services.base import RequestMicroService
from satosa.response import Redirect


logger = logging.getLogger(__name__)
BACKEND_TYPE_SAML = "saml"


class DS(RequestMicroService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ds_uri = config["ds_uri"]
        self.response_endpoint = config["response_endpoint"]
        self.choices = config.get("choices", [])

    def process(self, context, data):
        logger.info({
            "msg": "Static discovery choices",
            "choices": self.choices,
        })

        if not self.choices:
            return super().process(context, data)

        logger.info({
            "msg": "Redirecting to discovery",
            "choices": self.choices,
        })

        context.state[self.name] = {
            "internal": data.to_dict()
        }
        choices_serialized = json_dumps(self.choices).encode("utf-8")
        choices_encoded = b64encode(choices_serialized).decode("utf-8")
        url_path = "{uri}/{payload}".format(uri=self.ds_uri, payload=choices_encoded)
        return Redirect(url_path)

    def register_endpoints(self):
        url_map = [
            (
                "^{endpoint}/.*".format(endpoint=self.response_endpoint),
                self.response_handler,
            ),
        ]
        return url_map

    def response_handler(self, context):
        data_serialized = context.state.get(self.name, {}).get("internal", {})
        data = InternalData.from_dict(data_serialized)

        response_encoded = reg_replace(r"^{endpoint}/".format(endpoint=self.response_endpoint), "", context._path, count=1)
        response_decoded = b64decode(response_encoded).decode("utf-8")
        # XXX response_data = json_loads(response_decoded)
        selection = next((b for b in self.choices if b["id"] == response_decoded), None)

        logger.info({
            "msg": "Response from discovery",
            "selection": selection,
        })

        context.target_backend = selection["backend"]
        if selection.get("type") == BACKEND_TYPE_SAML:
            context.decorate(Context.KEY_TARGET_ENTITYID, selection["id"])
        return super().process(context, data)

def main():
    print("test1111")

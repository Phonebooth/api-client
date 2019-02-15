import logging
from json import JSONDecodeError
from xml.etree import ElementTree

from requests import Response

from apiclient.exceptions import ClientUnexpectedError

LOG = logging.getLogger(__name__)


class BaseResponseHandler:
    """Parses the response according to the strategy set."""

    @staticmethod
    def get_request_data(response: Response):
        raise NotImplementedError


class RequestsResponseHandler(BaseResponseHandler):
    """Return the original requests response."""

    @staticmethod
    def get_request_data(response: Response) -> Response:
        return response


class JsonResponseHandler(BaseResponseHandler):
    """Attempt to return the decoded response data as json."""

    @staticmethod
    def get_request_data(response: Response) -> dict:
        try:
            response_json = response.json()
        except JSONDecodeError as error:
            LOG.error("Unable to decode response data to json. data=%s", response.text)
            raise ClientUnexpectedError(
                f"Unable to decode response data to json. data='{response.text}'"
            ) from error
        return response_json


class XmlResponseHandler(BaseResponseHandler):
    """Attempt to return the decoded response to an xml Element."""

    @staticmethod
    def get_request_data(response: Response) -> ElementTree.Element:
        try:
            xml_element = ElementTree.fromstring(response.text)
        except ElementTree.ParseError as error:
            LOG.error("Unable to parse response data to xml. data=%s", response.text)
            raise ClientUnexpectedError(
                f"Unable to parse response data to xml. data='{response.text}'"
            ) from error
        return xml_element
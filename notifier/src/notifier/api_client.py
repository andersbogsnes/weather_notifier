from typing import Optional, Any

import attr
import httpx
from typing import Protocol


@attr.define()
class ApiAuth:
    """
    Represents the authentication method of the API

    Parameters
    ----------
    api_key
        The API key used to authenticate to the API
    """

    api_key: str = attr.field(repr=False)


JsonResponseType = dict[str, Any] | list[dict[str, Any]]


class ApiClientInterface(Protocol):
    """
    Represent the Interface an APIClient should satisfy
    """

    auth: ApiAuth

    def get(self, endpoint: str, params: Optional[dict] = None) -> JsonResponseType:
        ...


@attr.define()
class ApiClient:
    """
    An API client for fetching data from Web APIs
    """

    base_url: str
    auth: ApiAuth = None

    def _client(self) -> httpx.Client:
        """Returns the client used to communicate with the API"""
        return httpx.Client(base_url=self.base_url)

    def get(self, endpoint: str, params: Optional[dict] = None) -> JsonResponseType:
        """
        Gets the JSON data from an HTTP endpoint

        Parameters
        ----------
        endpoint
            The endpoint to get data from
        params
            Any query parameters that should be sent to the API

        Raises
        ------
        HTTPStatusError
            Raised if the server returns either 4xx or 5xx status codes

        Returns
        -------
        JsonResponseType
            The API response converted to a dict or list of dicts
        """
        params = {} if params is None else params
        with self._client() as c:
            r = c.get(endpoint, params=params)
        r.raise_for_status()
        return r.json()

from typing import Optional

import attr
import httpx


@attr.s(auto_attribs=True)
class ApiClient:
    base_url: str

    def _client(self) -> httpx.Client:
        return httpx.Client(base_url=self.base_url)

    def get(self, endpoint: str, params: Optional[dict] = None):
        params = {} if params is None else params
        with self._client() as c:
            r = c.get(endpoint, params=params)
        r.raise_for_status()
        return r.json()

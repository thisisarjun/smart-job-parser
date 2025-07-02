from typing import Any

import httpx


class HttpBaseClient:
    def __init__(self, base_url: str, headers: dict[str, Any] | None = None, timeout: float = 30.0):
        self.base_url = base_url
        self.default_headers = headers or {}
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers=self.default_headers,
            timeout=timeout,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> httpx.Response:
        try:
            merged_headers = {**self.default_headers, **(headers or {})}
            response = await self.client.get(url, params=params, headers=merged_headers)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise e
        return response

    async def post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> httpx.Response:
        try:
            merged_headers = {**self.default_headers, **(headers or {})}
            response = await self.client.post(url, json=json, data=data, headers=merged_headers)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise e
        return response

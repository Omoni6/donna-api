import httpx
from typing import Optional, Dict, Any

async def make_http_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
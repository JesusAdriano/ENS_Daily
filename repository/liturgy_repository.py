import json
from typing import Any, Dict, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen


class LiturgyRepository:
    def __init__(
        self,
        url: str = "https://liturgia.up.railway.app/",
        timeout: float = 5.0,
    ) -> None:
        self.url = url
        self.timeout = timeout

    def get_today(self) -> Optional[Dict[str, Any]]:
        request = Request(self.url, headers={"Accept": "application/json"})

        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = json.load(response)
        except (OSError, URLError, ValueError, TimeoutError):
            return None

        if not isinstance(payload, dict):
            return None

        evangelho = payload.get("evangelho")
        if not isinstance(evangelho, dict):
            return None

        text = evangelho.get("texto")
        if not isinstance(text, str) or not text.strip():
            return None

        return {
            "data": payload.get("data", ""),
            "liturgia": payload.get("liturgia", ""),
            "referencia": evangelho.get("referencia", ""),
            "titulo": evangelho.get("titulo", "Evangelho"),
            "texto": text,
        }

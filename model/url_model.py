from __future__ import annotations

from pydantic import BaseModel


class URLModel(BaseModel):
    title: str
    url: str

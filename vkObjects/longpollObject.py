# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = longpoll_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Response:
    key: str
    server: str
    ts: int

    @staticmethod
    def from_dict(obj: Any) -> 'Response':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        server = from_str(obj.get("server"))
        ts = from_int(obj.get("ts"))
        return Response(key, server, ts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["server"] = from_str(self.server)
        result["ts"] = from_int(self.ts)
        return result


@dataclass
class Longpoll:
    response: Response

    @staticmethod
    def from_dict(obj: Any) -> 'Longpoll':
        assert isinstance(obj, dict)
        response = Response.from_dict(obj.get("response"))
        return Longpoll(response)

    def to_dict(self) -> dict:
        result: dict = {}
        result["response"] = to_class(Response, self.response)
        return result


def longpoll_from_dict(s: Any) -> Longpoll:
    return Longpoll.from_dict(s)


def longpoll_to_dict(x: Longpoll) -> Any:
    return to_class(Longpoll, x)

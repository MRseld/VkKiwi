# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = longpolldata_object_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, Union, TypeVar, Type, Callable, cast


T = TypeVar("T")


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class UpdateClass:
    emoji: Optional[int] = None
    geo_provider: Optional[int] = None
    title: Optional[str] = None
    geo: Optional[str] = None
    attach1_type: Optional[str] = None
    attach2_type: Optional[str] = None
    attach3_type: Optional[str] = None
    attach4_type: Optional[str] = None
    attach5_type: Optional[str] = None
    attach6_type: Optional[str] = None
    attach7_type: Optional[str] = None
    attach8_type: Optional[str] = None
    attach9_type: Optional[str] = None
    attach10_type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'UpdateClass':
        assert isinstance(obj, dict)
        emoji = from_union([from_none, lambda x: int(from_str(x))], obj.get("emoji"))
        geo_provider = from_union([from_none, lambda x: int(from_str(x))], obj.get("geo_provider"))
        title = from_union([from_str, from_none], obj.get("title"))
        geo = from_union([from_str, from_none], obj.get("geo"))
        attach1_type = from_union([from_str, from_none], obj.get("attach1_type"))
        attach2_type = from_union([from_str, from_none], obj.get("attach2_type"))
        attach3_type = from_union([from_str, from_none], obj.get("attach3_type"))
        attach4_type = from_union([from_str, from_none], obj.get("attach4_type"))
        attach5_type = from_union([from_str, from_none], obj.get("attach5_type"))
        attach6_type = from_union([from_str, from_none], obj.get("attach6_type"))
        attach7_type = from_union([from_str, from_none], obj.get("attach7_type"))
        attach8_type = from_union([from_str, from_none], obj.get("attach8_type"))
        attach9_type = from_union([from_str, from_none], obj.get("attach9_type"))
        attach10_type = from_union([from_str, from_none], obj.get("attach10_type"))
        return UpdateClass(emoji, geo_provider, title, geo, attach1_type, attach2_type, attach3_type, attach4_type, attach5_type, attach6_type, attach7_type, attach8_type, attach9_type, attach10_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["emoji"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.emoji)
        result["geo_provider"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.geo_provider)
        result["title"] = from_union([from_str, from_none], self.title)
        result["geo"] = from_union([from_str, from_none], self.geo)
        result["attach1_type"] = from_union([from_str, from_none], self.attach1_type)
        result["attach2_type"] = from_union([from_str, from_none], self.attach2_type)
        result["attach3_type"] = from_union([from_str, from_none], self.attach3_type)
        result["attach4_type"] = from_union([from_str, from_none], self.attach4_type)
        result["attach5_type"] = from_union([from_str, from_none], self.attach5_type)
        result["attach6_type"] = from_union([from_str, from_none], self.attach6_type)
        result["attach7_type"] = from_union([from_str, from_none], self.attach7_type)
        result["attach8_type"] = from_union([from_str, from_none], self.attach8_type)
        result["attach9_type"] = from_union([from_str, from_none], self.attach9_type)
        result["attach10_type"] = from_union([from_str, from_none], self.attach10_type)
        return result


@dataclass
class LongpolldataObject:
    ts: int
    updates: List[List[Union[UpdateClass, int, str]]]

    @staticmethod
    def from_dict(obj: Any) -> 'LongpolldataObject':
        assert isinstance(obj, dict)
        ts = from_int(obj.get("ts"))
        updates = from_list(lambda x: from_list(lambda x: from_union([from_int, UpdateClass.from_dict, from_str], x), x), obj.get("updates"))
        return LongpolldataObject(ts, updates)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ts"] = from_int(self.ts)
        result["updates"] = from_list(lambda x: from_list(lambda x: from_union([from_int, lambda x: to_class(UpdateClass, x), from_str], x), x), self.updates)
        return result


def longpolldata_object_from_dict(s: Any) -> LongpolldataObject:
    return LongpolldataObject.from_dict(s)


def longpolldata_object_to_dict(x: LongpolldataObject) -> Any:
    return to_class(LongpolldataObject, x)

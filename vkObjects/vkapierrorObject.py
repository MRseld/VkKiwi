# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = vkapi_error_object_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, Union, Any, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class ValueEnum(Enum):
    EMPTY = ""
    MESSAGES_GET_CONVERSATIONSS = "messages.getConversationss"
    THE_5103 = "5.103"


class RequestParam:
    key: Optional[str]
    value: Union[ValueEnum, int, None]

    def __init__(self, key: Optional[str], value: Union[ValueEnum, int, None]) -> None:
        self.key = key
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'RequestParam':
        assert isinstance(obj, dict)
        key = from_union([from_str, from_none], obj.get("key"))
        value = from_union([from_none, lambda x: from_union([ValueEnum, lambda x: int(x)], from_str(x))], obj.get("value"))
        return RequestParam(key, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_union([from_str, from_none], self.key)
        result["value"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: to_enum(ValueEnum, (lambda x: is_type(ValueEnum, x))(x)))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.value)
        return result


class Error:
    error_code: Optional[int]
    error_msg: Optional[str]
    request_params: Optional[List[RequestParam]]

    def __init__(self, error_code: Optional[int], error_msg: Optional[str], request_params: Optional[List[RequestParam]]) -> None:
        self.error_code = error_code
        self.error_msg = error_msg
        self.request_params = request_params

    @staticmethod
    def from_dict(obj: Any) -> 'Error':
        assert isinstance(obj, dict)
        error_code = from_union([from_int, from_none], obj.get("error_code"))
        error_msg = from_union([from_str, from_none], obj.get("error_msg"))
        request_params = from_union([lambda x: from_list(RequestParam.from_dict, x), from_none], obj.get("request_params"))
        return Error(error_code, error_msg, request_params)

    def to_dict(self) -> dict:
        result: dict = {}
        result["error_code"] = from_union([from_int, from_none], self.error_code)
        result["error_msg"] = from_union([from_str, from_none], self.error_msg)
        result["request_params"] = from_union([lambda x: from_list(lambda x: to_class(RequestParam, x), x), from_none], self.request_params)
        return result


class VkapiErrorObject:
    error: Optional[Error]

    def __init__(self, error: Optional[Error]) -> None:
        self.error = error

    @staticmethod
    def from_dict(obj: Any) -> 'VkapiErrorObject':
        assert isinstance(obj, dict)
        error = from_union([Error.from_dict, from_none], obj.get("error"))
        return VkapiErrorObject(error)

    def to_dict(self) -> dict:
        result: dict = {}
        result["error"] = from_union([lambda x: to_class(Error, x), from_none], self.error)
        return result


def vkapi_error_object_from_dict(s: Any) -> VkapiErrorObject:
    return VkapiErrorObject.from_dict(s)


def vkapi_error_object_to_dict(x: VkapiErrorObject) -> Any:
    return to_class(VkapiErrorObject, x)

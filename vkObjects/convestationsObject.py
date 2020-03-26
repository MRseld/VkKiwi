# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = convestation_from_dict(json.loads(json_string))

from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from enum import Enum


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
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
    


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class Group:
    id: Optional[int]
    name: Optional[str]
    screen_name: Optional[str]
    is_closed: Optional[int]
    type: Optional[str]
    is_admin: Optional[int]
    is_member: Optional[int]
    is_advertiser: Optional[int]
    photo_50: Optional[str]
    photo_100: Optional[str]
    photo_200: Optional[str]

    def __init__(self, id: Optional[int], name: Optional[str], screen_name: Optional[str], is_closed: Optional[int], type: Optional[str], is_admin: Optional[int], is_member: Optional[int], is_advertiser: Optional[int], photo_50: Optional[str], photo_100: Optional[str], photo_200: Optional[str]) -> None:
        self.id = id
        self.name = name
        self.screen_name = screen_name
        self.is_closed = is_closed
        self.type = type
        self.is_admin = is_admin
        self.is_member = is_member
        self.is_advertiser = is_advertiser
        self.photo_50 = photo_50
        self.photo_100 = photo_100
        self.photo_200 = photo_200

    @staticmethod
    def from_dict(obj: Any) -> 'Group':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        screen_name = from_union([from_str, from_none], obj.get("screen_name"))
        is_closed = from_union([from_int, from_none], obj.get("is_closed"))
        type = from_union([from_str, from_none], obj.get("type"))
        is_admin = from_union([from_int, from_none], obj.get("is_admin"))
        is_member = from_union([from_int, from_none], obj.get("is_member"))
        is_advertiser = from_union([from_int, from_none], obj.get("is_advertiser"))
        photo_50 = from_union([from_str, from_none], obj.get("photo_50"))
        photo_100 = from_union([from_str, from_none], obj.get("photo_100"))
        photo_200 = from_union([from_str, from_none], obj.get("photo_200"))
        return Group(id, name, screen_name, is_closed, type, is_admin, is_member, is_advertiser, photo_50, photo_100, photo_200)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["screen_name"] = from_union([from_str, from_none], self.screen_name)
        result["is_closed"] = from_union([from_int, from_none], self.is_closed)
        result["type"] = from_union([from_str, from_none], self.type)
        result["is_admin"] = from_union([from_int, from_none], self.is_admin)
        result["is_member"] = from_union([from_int, from_none], self.is_member)
        result["is_advertiser"] = from_union([from_int, from_none], self.is_advertiser)
        result["photo_50"] = from_union([from_str, from_none], self.photo_50)
        result["photo_100"] = from_union([from_str, from_none], self.photo_100)
        result["photo_200"] = from_union([from_str, from_none], self.photo_200)
        return result


class CanWrite:
    allowed: Optional[bool]

    def __init__(self, allowed: Optional[bool]) -> None:
        self.allowed = allowed

    @staticmethod
    def from_dict(obj: Any) -> 'CanWrite':
        assert isinstance(obj, dict)
        allowed = from_union([from_bool, from_none], obj.get("allowed"))
        return CanWrite(allowed)

    def to_dict(self) -> dict:
        result: dict = {}
        result["allowed"] = from_union([from_bool, from_none], self.allowed)
        return result


class ACL:
    can_change_info: Optional[bool]
    can_change_invite_link: Optional[bool]
    can_change_pin: Optional[bool]
    can_invite: Optional[bool]
    can_promote_users: Optional[bool]
    can_see_invite_link: Optional[bool]
    can_moderate: Optional[bool]
    can_copy_chat: Optional[bool]

    def __init__(self, can_change_info: Optional[bool], can_change_invite_link: Optional[bool], can_change_pin: Optional[bool], can_invite: Optional[bool], can_promote_users: Optional[bool], can_see_invite_link: Optional[bool], can_moderate: Optional[bool], can_copy_chat: Optional[bool]) -> None:
        self.can_change_info = can_change_info
        self.can_change_invite_link = can_change_invite_link
        self.can_change_pin = can_change_pin
        self.can_invite = can_invite
        self.can_promote_users = can_promote_users
        self.can_see_invite_link = can_see_invite_link
        self.can_moderate = can_moderate
        self.can_copy_chat = can_copy_chat

    @staticmethod
    def from_dict(obj: Any) -> 'ACL':
        assert isinstance(obj, dict)
        can_change_info = from_union([from_bool, from_none], obj.get("can_change_info"))
        can_change_invite_link = from_union([from_bool, from_none], obj.get("can_change_invite_link"))
        can_change_pin = from_union([from_bool, from_none], obj.get("can_change_pin"))
        can_invite = from_union([from_bool, from_none], obj.get("can_invite"))
        can_promote_users = from_union([from_bool, from_none], obj.get("can_promote_users"))
        can_see_invite_link = from_union([from_bool, from_none], obj.get("can_see_invite_link"))
        can_moderate = from_union([from_bool, from_none], obj.get("can_moderate"))
        can_copy_chat = from_union([from_bool, from_none], obj.get("can_copy_chat"))
        return ACL(can_change_info, can_change_invite_link, can_change_pin, can_invite, can_promote_users, can_see_invite_link, can_moderate, can_copy_chat)

    def to_dict(self) -> dict:
        result: dict = {}
        result["can_change_info"] = from_union([from_bool, from_none], self.can_change_info)
        result["can_change_invite_link"] = from_union([from_bool, from_none], self.can_change_invite_link)
        result["can_change_pin"] = from_union([from_bool, from_none], self.can_change_pin)
        result["can_invite"] = from_union([from_bool, from_none], self.can_invite)
        result["can_promote_users"] = from_union([from_bool, from_none], self.can_promote_users)
        result["can_see_invite_link"] = from_union([from_bool, from_none], self.can_see_invite_link)
        result["can_moderate"] = from_union([from_bool, from_none], self.can_moderate)
        result["can_copy_chat"] = from_union([from_bool, from_none], self.can_copy_chat)
        return result


class ChatSettingsPhoto:
    photo_50: Optional[str]
    photo_100: Optional[str]
    photo_200: Optional[str]

    def __init__(self, photo_50: Optional[str], photo_100: Optional[str], photo_200: Optional[str]) -> None:
        self.photo_50 = photo_50
        self.photo_100 = photo_100
        self.photo_200 = photo_200

    @staticmethod
    def from_dict(obj: Any) -> 'ChatSettingsPhoto':
        assert isinstance(obj, dict)
        photo_50 = from_union([from_str, from_none], obj.get("photo_50"))
        photo_100 = from_union([from_str, from_none], obj.get("photo_100"))
        photo_200 = from_union([from_str, from_none], obj.get("photo_200"))
        return ChatSettingsPhoto(photo_50, photo_100, photo_200)

    def to_dict(self) -> dict:
        result: dict = {}
        result["photo_50"] = from_union([from_str, from_none], self.photo_50)
        result["photo_100"] = from_union([from_str, from_none], self.photo_100)
        result["photo_200"] = from_union([from_str, from_none], self.photo_200)
        return result


class Action:
    type: Optional[str]
    url: Optional[str]

    def __init__(self, type: Optional[str], url: Optional[str]) -> None:
        self.type = type
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Action':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Action(type, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class Button:
    title: Optional[str]
    action: Optional[Action]

    def __init__(self, title: Optional[str], action: Optional[Action]) -> None:
        self.title = title
        self.action = action

    @staticmethod
    def from_dict(obj: Any) -> 'Button':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        action = from_union([Action.from_dict, from_none], obj.get("action"))
        return Button(title, action)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["action"] = from_union([lambda x: to_class(Action, x), from_none], self.action)
        return result


class Size:
    type: Optional[str]
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]

    def __init__(self, type: Optional[str], url: Optional[str], width: Optional[int], height: Optional[int]) -> None:
        self.type = type
        self.url = url
        self.width = width
        self.height = height

    @staticmethod
    def from_dict(obj: Any) -> 'Size':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        return Size(type, url, width, height)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["url"] = from_union([from_str, from_none], self.url)
        result["width"] = from_union([from_int, from_none], self.width)
        result["height"] = from_union([from_int, from_none], self.height)
        return result


class LinkPhoto:
    id: Optional[int]
    album_id: Optional[int]
    owner_id: Optional[int]
    sizes: Optional[List[Size]]
    text: Optional[str]
    date: Optional[int]
    access_key: Optional[str]

    def __init__(self, id: Optional[int], album_id: Optional[int], owner_id: Optional[int], sizes: Optional[List[Size]], text: Optional[str], date: Optional[int], access_key: Optional[str]) -> None:
        self.id = id
        self.album_id = album_id
        self.owner_id = owner_id
        self.sizes = sizes
        self.text = text
        self.date = date
        self.access_key = access_key

    @staticmethod
    def from_dict(obj: Any) -> 'LinkPhoto':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        album_id = from_union([from_int, from_none], obj.get("album_id"))
        owner_id = from_union([from_int, from_none], obj.get("owner_id"))
        sizes = from_union([lambda x: from_list(Size.from_dict, x), from_none], obj.get("sizes"))
        text = from_union([from_str, from_none], obj.get("text"))
        date = from_union([from_int, from_none], obj.get("date"))
        access_key = from_union([from_str, from_none], obj.get("access_key"))
        return LinkPhoto(id, album_id, owner_id, sizes, text, date, access_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["album_id"] = from_union([from_int, from_none], self.album_id)
        result["owner_id"] = from_union([from_int, from_none], self.owner_id)
        result["sizes"] = from_union([lambda x: from_list(lambda x: to_class(Size, x), x), from_none], self.sizes)
        result["text"] = from_union([from_str, from_none], self.text)
        result["date"] = from_union([from_int, from_none], self.date)
        result["access_key"] = from_union([from_str, from_none], self.access_key)
        return result


class Link:
    url: Optional[str]
    title: Optional[str]
    caption: Optional[str]
    description: Optional[str]
    photo: Optional[LinkPhoto]
    button: Optional[Button]

    def __init__(self, url: Optional[str], title: Optional[str], caption: Optional[str], description: Optional[str], photo: Optional[LinkPhoto], button: Optional[Button]) -> None:
        self.url = url
        self.title = title
        self.caption = caption
        self.description = description
        self.photo = photo
        self.button = button

    @staticmethod
    def from_dict(obj: Any) -> 'Link':
        assert isinstance(obj, dict)
        url = from_union([from_str, from_none], obj.get("url"))
        title = from_union([from_str, from_none], obj.get("title"))
        caption = from_union([from_str, from_none], obj.get("caption"))
        description = from_union([from_str, from_none], obj.get("description"))
        photo = from_union([LinkPhoto.from_dict, from_none], obj.get("photo"))
        button = from_union([Button.from_dict, from_none], obj.get("button"))
        return Link(url, title, caption, description, photo, button)

    def to_dict(self) -> dict:
        result: dict = {}
        result["url"] = from_union([from_str, from_none], self.url)
        result["title"] = from_union([from_str, from_none], self.title)
        result["caption"] = from_union([from_str, from_none], self.caption)
        result["description"] = from_union([from_str, from_none], self.description)
        result["photo"] = from_union([lambda x: to_class(LinkPhoto, x), from_none], self.photo)
        result["button"] = from_union([lambda x: to_class(Button, x), from_none], self.button)
        return result


class Answer:
    id: Optional[int]
    text: Optional[str]
    votes: Optional[int]
    rate: Optional[float]

    def __init__(self, id: Optional[int], text: Optional[str], votes: Optional[int], rate: Optional[float]) -> None:
        self.id = id
        self.text = text
        self.votes = votes
        self.rate = rate

    @staticmethod
    def from_dict(obj: Any) -> 'Answer':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        text = from_union([from_str, from_none], obj.get("text"))
        votes = from_union([from_int, from_none], obj.get("votes"))
        rate = from_union([from_float, from_none], obj.get("rate"))
        return Answer(id, text, votes, rate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["text"] = from_union([from_str, from_none], self.text)
        result["votes"] = from_union([from_int, from_none], self.votes)
        result["rate"] = from_union([to_float, from_none], self.rate)
        return result


class Point:
    color: Optional[str]
    position: Optional[int]

    def __init__(self, color: Optional[str], position: Optional[int]) -> None:
        self.color = color
        self.position = position

    @staticmethod
    def from_dict(obj: Any) -> 'Point':
        assert isinstance(obj, dict)
        color = from_union([from_str, from_none], obj.get("color"))
        position = from_union([from_int, from_none], obj.get("position"))
        return Point(color, position)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_union([from_str, from_none], self.color)
        result["position"] = from_union([from_int, from_none], self.position)
        return result


class Background:
    angle: Optional[int]
    color: Optional[str]
    id: Optional[int]
    name: Optional[str]
    points: Optional[List[Point]]
    type: Optional[str]

    def __init__(self, angle: Optional[int], color: Optional[str], id: Optional[int], name: Optional[str], points: Optional[List[Point]], type: Optional[str]) -> None:
        self.angle = angle
        self.color = color
        self.id = id
        self.name = name
        self.points = points
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Background':
        assert isinstance(obj, dict)
        angle = from_union([from_int, from_none], obj.get("angle"))
        color = from_union([from_str, from_none], obj.get("color"))
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        points = from_union([lambda x: from_list(Point.from_dict, x), from_none], obj.get("points"))
        type = from_union([from_str, from_none], obj.get("type"))
        return Background(angle, color, id, name, points, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["angle"] = from_union([from_int, from_none], self.angle)
        result["color"] = from_union([from_str, from_none], self.color)
        result["id"] = from_union([from_int, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["points"] = from_union([lambda x: from_list(lambda x: to_class(Point, x), x), from_none], self.points)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


class Friend:
    id: Optional[int]

    def __init__(self, id: Optional[int]) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> 'Friend':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        return Friend(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        return result


class Poll:
    id: Optional[int]
    owner_id: Optional[int]
    created: Optional[int]
    question: Optional[str]
    votes: Optional[int]
    answers: Optional[List[Answer]]
    anonymous: Optional[bool]
    multiple: Optional[bool]
    answer_ids: Optional[List[int]]
    end_date: Optional[int]
    closed: Optional[bool]
    is_board: Optional[bool]
    can_edit: Optional[bool]
    can_vote: Optional[bool]
    can_report: Optional[bool]
    can_share: Optional[bool]
    author_id: Optional[int]
    background: Optional[Background]
    friends: Optional[List[Friend]]

    def __init__(self, id: Optional[int], owner_id: Optional[int], created: Optional[int], question: Optional[str], votes: Optional[int], answers: Optional[List[Answer]], anonymous: Optional[bool], multiple: Optional[bool], answer_ids: Optional[List[int]], end_date: Optional[int], closed: Optional[bool], is_board: Optional[bool], can_edit: Optional[bool], can_vote: Optional[bool], can_report: Optional[bool], can_share: Optional[bool], author_id: Optional[int], background: Optional[Background], friends: Optional[List[Friend]]) -> None:
        self.id = id
        self.owner_id = owner_id
        self.created = created
        self.question = question
        self.votes = votes
        self.answers = answers
        self.anonymous = anonymous
        self.multiple = multiple
        self.answer_ids = answer_ids
        self.end_date = end_date
        self.closed = closed
        self.is_board = is_board
        self.can_edit = can_edit
        self.can_vote = can_vote
        self.can_report = can_report
        self.can_share = can_share
        self.author_id = author_id
        self.background = background
        self.friends = friends

    @staticmethod
    def from_dict(obj: Any) -> 'Poll':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        owner_id = from_union([from_int, from_none], obj.get("owner_id"))
        created = from_union([from_int, from_none], obj.get("created"))
        question = from_union([from_str, from_none], obj.get("question"))
        votes = from_union([from_int, from_none], obj.get("votes"))
        answers = from_union([lambda x: from_list(Answer.from_dict, x), from_none], obj.get("answers"))
        anonymous = from_union([from_bool, from_none], obj.get("anonymous"))
        multiple = from_union([from_bool, from_none], obj.get("multiple"))
        answer_ids = from_union([lambda x: from_list(from_int, x), from_none], obj.get("answer_ids"))
        end_date = from_union([from_int, from_none], obj.get("end_date"))
        closed = from_union([from_bool, from_none], obj.get("closed"))
        is_board = from_union([from_bool, from_none], obj.get("is_board"))
        can_edit = from_union([from_bool, from_none], obj.get("can_edit"))
        can_vote = from_union([from_bool, from_none], obj.get("can_vote"))
        can_report = from_union([from_bool, from_none], obj.get("can_report"))
        can_share = from_union([from_bool, from_none], obj.get("can_share"))
        author_id = from_union([from_int, from_none], obj.get("author_id"))
        background = from_union([Background.from_dict, from_none], obj.get("background"))
        friends = from_union([lambda x: from_list(Friend.from_dict, x), from_none], obj.get("friends"))
        return Poll(id, owner_id, created, question, votes, answers, anonymous, multiple, answer_ids, end_date, closed, is_board, can_edit, can_vote, can_report, can_share, author_id, background, friends)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["owner_id"] = from_union([from_int, from_none], self.owner_id)
        result["created"] = from_union([from_int, from_none], self.created)
        result["question"] = from_union([from_str, from_none], self.question)
        result["votes"] = from_union([from_int, from_none], self.votes)
        result["answers"] = from_union([lambda x: from_list(lambda x: to_class(Answer, x), x), from_none], self.answers)
        result["anonymous"] = from_union([from_bool, from_none], self.anonymous)
        result["multiple"] = from_union([from_bool, from_none], self.multiple)
        result["answer_ids"] = from_union([lambda x: from_list(from_int, x), from_none], self.answer_ids)
        result["end_date"] = from_union([from_int, from_none], self.end_date)
        result["closed"] = from_union([from_bool, from_none], self.closed)
        result["is_board"] = from_union([from_bool, from_none], self.is_board)
        result["can_edit"] = from_union([from_bool, from_none], self.can_edit)
        result["can_vote"] = from_union([from_bool, from_none], self.can_vote)
        result["can_report"] = from_union([from_bool, from_none], self.can_report)
        result["can_share"] = from_union([from_bool, from_none], self.can_share)
        result["author_id"] = from_union([from_int, from_none], self.author_id)
        result["background"] = from_union([lambda x: to_class(Background, x), from_none], self.background)
        result["friends"] = from_union([lambda x: from_list(lambda x: to_class(Friend, x), x), from_none], self.friends)
        return result


class WallAttachment:
    type: Optional[str]
    poll: Optional[Poll]

    def __init__(self, type: Optional[str], poll: Optional[Poll]) -> None:
        self.type = type
        self.poll = poll

    @staticmethod
    def from_dict(obj: Any) -> 'WallAttachment':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        poll = from_union([Poll.from_dict, from_none], obj.get("poll"))
        return WallAttachment(type, poll)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["poll"] = from_union([lambda x: to_class(Poll, x), from_none], self.poll)
        return result


class Comments:
    count: Optional[int]
    can_post: Optional[int]
    groups_can_post: Optional[bool]

    def __init__(self, count: Optional[int], can_post: Optional[int], groups_can_post: Optional[bool]) -> None:
        self.count = count
        self.can_post = can_post
        self.groups_can_post = groups_can_post

    @staticmethod
    def from_dict(obj: Any) -> 'Comments':
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        can_post = from_union([from_int, from_none], obj.get("can_post"))
        groups_can_post = from_union([from_bool, from_none], obj.get("groups_can_post"))
        return Comments(count, can_post, groups_can_post)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([from_int, from_none], self.count)
        result["can_post"] = from_union([from_int, from_none], self.can_post)
        result["groups_can_post"] = from_union([from_bool, from_none], self.groups_can_post)
        return result


class Likes:
    count: Optional[int]
    user_likes: Optional[int]
    can_like: Optional[int]
    can_publish: Optional[int]

    def __init__(self, count: Optional[int], user_likes: Optional[int], can_like: Optional[int], can_publish: Optional[int]) -> None:
        self.count = count
        self.user_likes = user_likes
        self.can_like = can_like
        self.can_publish = can_publish

    @staticmethod
    def from_dict(obj: Any) -> 'Likes':
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        user_likes = from_union([from_int, from_none], obj.get("user_likes"))
        can_like = from_union([from_int, from_none], obj.get("can_like"))
        can_publish = from_union([from_int, from_none], obj.get("can_publish"))
        return Likes(count, user_likes, can_like, can_publish)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([from_int, from_none], self.count)
        result["user_likes"] = from_union([from_int, from_none], self.user_likes)
        result["can_like"] = from_union([from_int, from_none], self.can_like)
        result["can_publish"] = from_union([from_int, from_none], self.can_publish)
        return result


class PostSource:
    type: Optional[str]

    def __init__(self, type: Optional[str]) -> None:
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'PostSource':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        return PostSource(type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        return result


class Reposts:
    count: Optional[int]
    user_reposted: Optional[int]

    def __init__(self, count: Optional[int], user_reposted: Optional[int]) -> None:
        self.count = count
        self.user_reposted = user_reposted

    @staticmethod
    def from_dict(obj: Any) -> 'Reposts':
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        user_reposted = from_union([from_int, from_none], obj.get("user_reposted"))
        return Reposts(count, user_reposted)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([from_int, from_none], self.count)
        result["user_reposted"] = from_union([from_int, from_none], self.user_reposted)
        return result


class Views:
    count: Optional[int]

    def __init__(self, count: Optional[int]) -> None:
        self.count = count

    @staticmethod
    def from_dict(obj: Any) -> 'Views':
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        return Views(count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([from_int, from_none], self.count)
        return result


class Wall:
    id: Optional[int]
    from_id: Optional[int]
    to_id: Optional[int]
    date: Optional[int]
    post_type: Optional[str]
    text: Optional[str]
    marked_as_ads: Optional[int]
    attachments: Optional[List[WallAttachment]]
    post_source: Optional[PostSource]
    comments: Optional[Comments]
    likes: Optional[Likes]
    reposts: Optional[Reposts]
    views: Optional[Views]
    is_favorite: Optional[bool]
    access_key: Optional[str]

    def __init__(self, id: Optional[int], from_id: Optional[int], to_id: Optional[int], date: Optional[int], post_type: Optional[str], text: Optional[str], marked_as_ads: Optional[int], attachments: Optional[List[WallAttachment]], post_source: Optional[PostSource], comments: Optional[Comments], likes: Optional[Likes], reposts: Optional[Reposts], views: Optional[Views], is_favorite: Optional[bool], access_key: Optional[str]) -> None:
        self.id = id
        self.from_id = from_id
        self.to_id = to_id
        self.date = date
        self.post_type = post_type
        self.text = text
        self.marked_as_ads = marked_as_ads
        self.attachments = attachments
        self.post_source = post_source
        self.comments = comments
        self.likes = likes
        self.reposts = reposts
        self.views = views
        self.is_favorite = is_favorite
        self.access_key = access_key

    @staticmethod
    def from_dict(obj: Any) -> 'Wall':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        from_id = from_union([from_int, from_none], obj.get("from_id"))
        to_id = from_union([from_int, from_none], obj.get("to_id"))
        date = from_union([from_int, from_none], obj.get("date"))
        post_type = from_union([from_str, from_none], obj.get("post_type"))
        text = from_union([from_str, from_none], obj.get("text"))
        marked_as_ads = from_union([from_int, from_none], obj.get("marked_as_ads"))
        attachments = from_union([lambda x: from_list(WallAttachment.from_dict, x), from_none], obj.get("attachments"))
        post_source = from_union([PostSource.from_dict, from_none], obj.get("post_source"))
        comments = from_union([Comments.from_dict, from_none], obj.get("comments"))
        likes = from_union([Likes.from_dict, from_none], obj.get("likes"))
        reposts = from_union([Reposts.from_dict, from_none], obj.get("reposts"))
        views = from_union([Views.from_dict, from_none], obj.get("views"))
        is_favorite = from_union([from_bool, from_none], obj.get("is_favorite"))
        access_key = from_union([from_str, from_none], obj.get("access_key"))
        return Wall(id, from_id, to_id, date, post_type, text, marked_as_ads, attachments, post_source, comments, likes, reposts, views, is_favorite, access_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["from_id"] = from_union([from_int, from_none], self.from_id)
        result["to_id"] = from_union([from_int, from_none], self.to_id)
        result["date"] = from_union([from_int, from_none], self.date)
        result["post_type"] = from_union([from_str, from_none], self.post_type)
        result["text"] = from_union([from_str, from_none], self.text)
        result["marked_as_ads"] = from_union([from_int, from_none], self.marked_as_ads)
        result["attachments"] = from_union([lambda x: from_list(lambda x: to_class(WallAttachment, x), x), from_none], self.attachments)
        result["post_source"] = from_union([lambda x: to_class(PostSource, x), from_none], self.post_source)
        result["comments"] = from_union([lambda x: to_class(Comments, x), from_none], self.comments)
        result["likes"] = from_union([lambda x: to_class(Likes, x), from_none], self.likes)
        result["reposts"] = from_union([lambda x: to_class(Reposts, x), from_none], self.reposts)
        result["views"] = from_union([lambda x: to_class(Views, x), from_none], self.views)
        result["is_favorite"] = from_union([from_bool, from_none], self.is_favorite)
        result["access_key"] = from_union([from_str, from_none], self.access_key)
        return result


class PinnedMessageAttachment:
    type: Optional[str]
    wall: Optional[Wall]
    link: Optional[Link]

    def __init__(self, type: Optional[str], wall: Optional[Wall], link: Optional[Link]) -> None:
        self.type = type
        self.wall = wall
        self.link = link

    @staticmethod
    def from_dict(obj: Any) -> 'PinnedMessageAttachment':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        wall = from_union([Wall.from_dict, from_none], obj.get("wall"))
        link = from_union([Link.from_dict, from_none], obj.get("link"))
        return PinnedMessageAttachment(type, wall, link)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["wall"] = from_union([lambda x: to_class(Wall, x), from_none], self.wall)
        result["link"] = from_union([lambda x: to_class(Link, x), from_none], self.link)
        return result


class Keyboard:
    one_time: Optional[bool]
    author_id: Optional[int]
    buttons: Optional[List[Any]]

    def __init__(self, one_time: Optional[bool], author_id: Optional[int], buttons: Optional[List[Any]]) -> None:
        self.one_time = one_time
        self.author_id = author_id
        self.buttons = buttons

    @staticmethod
    def from_dict(obj: Any) -> 'Keyboard':
        assert isinstance(obj, dict)
        one_time = from_union([from_bool, from_none], obj.get("one_time"))
        author_id = from_union([from_int, from_none], obj.get("author_id"))
        buttons = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("buttons"))
        return Keyboard(one_time, author_id, buttons)

    def to_dict(self) -> dict:
        result: dict = {}
        result["one_time"] = from_union([from_bool, from_none], self.one_time)
        result["author_id"] = from_union([from_int, from_none], self.author_id)
        result["buttons"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.buttons)
        return result


class PinnedMessage:
    id: Optional[int]
    date: Optional[int]
    from_id: Optional[int]
    peer_id: Optional[int]
    text: Optional[str]
    attachments: Optional[List[PinnedMessageAttachment]]
    fwd_messages: Optional[List[Any]]
    conversation_message_id: Optional[int]
    keyboard: Optional[Keyboard]

    def __init__(self, id: Optional[int], date: Optional[int], from_id: Optional[int], peer_id: Optional[int], text: Optional[str], attachments: Optional[List[PinnedMessageAttachment]], fwd_messages: Optional[List[Any]], conversation_message_id: Optional[int], keyboard: Optional[Keyboard]) -> None:
        self.id = id
        self.date = date
        self.from_id = from_id
        self.peer_id = peer_id
        self.text = text
        self.attachments = attachments
        self.fwd_messages = fwd_messages
        self.conversation_message_id = conversation_message_id
        self.keyboard = keyboard

    @staticmethod
    def from_dict(obj: Any) -> 'PinnedMessage':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        date = from_union([from_int, from_none], obj.get("date"))
        from_id = from_union([from_int, from_none], obj.get("from_id"))
        peer_id = from_union([from_int, from_none], obj.get("peer_id"))
        text = from_union([from_str, from_none], obj.get("text"))
        attachments = from_union([lambda x: from_list(PinnedMessageAttachment.from_dict, x), from_none], obj.get("attachments"))
        fwd_messages = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("fwd_messages"))
        conversation_message_id = from_union([from_int, from_none], obj.get("conversation_message_id"))
        keyboard = from_union([Keyboard.from_dict, from_none], obj.get("keyboard"))
        return PinnedMessage(id, date, from_id, peer_id, text, attachments, fwd_messages, conversation_message_id, keyboard)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["date"] = from_union([from_int, from_none], self.date)
        result["from_id"] = from_union([from_int, from_none], self.from_id)
        result["peer_id"] = from_union([from_int, from_none], self.peer_id)
        result["text"] = from_union([from_str, from_none], self.text)
        result["attachments"] = from_union([lambda x: from_list(lambda x: to_class(PinnedMessageAttachment, x), x), from_none], self.attachments)
        result["fwd_messages"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.fwd_messages)
        result["conversation_message_id"] = from_union([from_int, from_none], self.conversation_message_id)
        result["keyboard"] = from_union([lambda x: to_class(Keyboard, x), from_none], self.keyboard)
        return result


class ChatSettings:
    owner_id: Optional[int]
    title: Optional[str]
    state: Optional[str]
    acl: Optional[ACL]
    members_count: Optional[int]
    pinned_message: Optional[PinnedMessage]
    photo: Optional[ChatSettingsPhoto]
    admin_ids: Optional[List[int]]
    active_ids: Optional[List[int]]

    def __init__(self, owner_id: Optional[int], title: Optional[str], state: Optional[str], acl: Optional[ACL], members_count: Optional[int], pinned_message: Optional[PinnedMessage], photo: Optional[ChatSettingsPhoto], admin_ids: Optional[List[int]], active_ids: Optional[List[int]]) -> None:
        self.owner_id = owner_id
        self.title = title
        self.state = state
        self.acl = acl
        self.members_count = members_count
        self.pinned_message = pinned_message
        self.photo = photo
        self.admin_ids = admin_ids
        self.active_ids = active_ids

    @staticmethod
    def from_dict(obj: Any) -> 'ChatSettings':
        assert isinstance(obj, dict)
        owner_id = from_union([from_int, from_none], obj.get("owner_id"))
        title = from_union([from_str, from_none], obj.get("title"))
        state = from_union([from_str, from_none], obj.get("state"))
        acl = from_union([ACL.from_dict, from_none], obj.get("acl"))
        members_count = from_union([from_int, from_none], obj.get("members_count"))
        pinned_message = from_union([PinnedMessage.from_dict, from_none], obj.get("pinned_message"))
        photo = from_union([ChatSettingsPhoto.from_dict, from_none], obj.get("photo"))
        admin_ids = from_union([lambda x: from_list(from_int, x), from_none], obj.get("admin_ids"))
        active_ids = from_union([lambda x: from_list(from_int, x), from_none], obj.get("active_ids"))
        return ChatSettings(owner_id, title, state, acl, members_count, pinned_message, photo, admin_ids, active_ids)

    def to_dict(self) -> dict:
        result: dict = {}
        result["owner_id"] = from_union([from_int, from_none], self.owner_id)
        result["title"] = from_union([from_str, from_none], self.title)
        result["state"] = from_union([from_str, from_none], self.state)
        result["acl"] = from_union([lambda x: to_class(ACL, x), from_none], self.acl)
        result["members_count"] = from_union([from_int, from_none], self.members_count)
        result["pinned_message"] = from_union([lambda x: to_class(PinnedMessage, x), from_none], self.pinned_message)
        result["photo"] = from_union([lambda x: to_class(ChatSettingsPhoto, x), from_none], self.photo)
        result["admin_ids"] = from_union([lambda x: from_list(from_int, x), from_none], self.admin_ids)
        result["active_ids"] = from_union([lambda x: from_list(from_int, x), from_none], self.active_ids)
        return result


class TypeEnum(Enum):
    CHAT = "chat"
    USER = "user"


class Peer:
    id: Optional[int]
    type: Optional[TypeEnum]
    local_id: Optional[int]

    def __init__(self, id: Optional[int], type: Optional[TypeEnum], local_id: Optional[int]) -> None:
        self.id = id
        self.type = type
        self.local_id = local_id

    @staticmethod
    def from_dict(obj: Any) -> 'Peer':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        type = from_union([TypeEnum, from_none], obj.get("type"))
        local_id = from_union([from_int, from_none], obj.get("local_id"))
        return Peer(id, type, local_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["type"] = from_union([lambda x: to_enum(TypeEnum, x), from_none], self.type)
        result["local_id"] = from_union([from_int, from_none], self.local_id)
        return result


class PushSettings:
    disabled_forever: Optional[bool]
    no_sound: Optional[bool]

    def __init__(self, disabled_forever: Optional[bool], no_sound: Optional[bool]) -> None:
        self.disabled_forever = disabled_forever
        self.no_sound = no_sound

    @staticmethod
    def from_dict(obj: Any) -> 'PushSettings':
        assert isinstance(obj, dict)
        disabled_forever = from_union([from_bool, from_none], obj.get("disabled_forever"))
        no_sound = from_union([from_bool, from_none], obj.get("no_sound"))
        return PushSettings(disabled_forever, no_sound)

    def to_dict(self) -> dict:
        result: dict = {}
        result["disabled_forever"] = from_union([from_bool, from_none], self.disabled_forever)
        result["no_sound"] = from_union([from_bool, from_none], self.no_sound)
        return result


class Conversation:
    peer: Optional[Peer]
    last_message_id: Optional[int]
    in_read: Optional[int]
    out_read: Optional[int]
    unread_count: Optional[int]
    push_settings: Optional[PushSettings]
    can_write: Optional[CanWrite]
    chat_settings: Optional[ChatSettings]

    def __init__(self, peer: Optional[Peer], last_message_id: Optional[int], in_read: Optional[int], out_read: Optional[int], unread_count: Optional[int], push_settings: Optional[PushSettings], can_write: Optional[CanWrite], chat_settings: Optional[ChatSettings]) -> None:
        self.peer = peer
        self.last_message_id = last_message_id
        self.in_read = in_read
        self.out_read = out_read
        self.unread_count = unread_count
        self.push_settings = push_settings
        self.can_write = can_write
        self.chat_settings = chat_settings

    @staticmethod
    def from_dict(obj: Any) -> 'Conversation':
        assert isinstance(obj, dict)
        peer = from_union([Peer.from_dict, from_none], obj.get("peer"))
        last_message_id = from_union([from_int, from_none], obj.get("last_message_id"))
        in_read = from_union([from_int, from_none], obj.get("in_read"))
        out_read = from_union([from_int, from_none], obj.get("out_read"))
        unread_count = from_union([from_int, from_none], obj.get("unread_count"))
        push_settings = from_union([PushSettings.from_dict, from_none], obj.get("push_settings"))
        can_write = from_union([CanWrite.from_dict, from_none], obj.get("can_write"))
        chat_settings = from_union([ChatSettings.from_dict, from_none], obj.get("chat_settings"))
        return Conversation(peer, last_message_id, in_read, out_read, unread_count, push_settings, can_write, chat_settings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["peer"] = from_union([lambda x: to_class(Peer, x), from_none], self.peer)
        result["last_message_id"] = from_union([from_int, from_none], self.last_message_id)
        result["in_read"] = from_union([from_int, from_none], self.in_read)
        result["out_read"] = from_union([from_int, from_none], self.out_read)
        result["unread_count"] = from_union([from_int, from_none], self.unread_count)
        result["push_settings"] = from_union([lambda x: to_class(PushSettings, x), from_none], self.push_settings)
        result["can_write"] = from_union([lambda x: to_class(CanWrite, x), from_none], self.can_write)
        result["chat_settings"] = from_union([lambda x: to_class(ChatSettings, x), from_none], self.chat_settings)
        return result


class FwdMessageAttachment:
    type: Optional[str]
    photo: Optional[LinkPhoto]

    def __init__(self, type: Optional[str], photo: Optional[LinkPhoto]) -> None:
        self.type = type
        self.photo = photo

    @staticmethod
    def from_dict(obj: Any) -> 'FwdMessageAttachment':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        photo = from_union([LinkPhoto.from_dict, from_none], obj.get("photo"))
        return FwdMessageAttachment(type, photo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["photo"] = from_union([lambda x: to_class(LinkPhoto, x), from_none], self.photo)
        return result


class FwdMessage:
    date: Optional[int]
    from_id: Optional[int]
    text: Optional[str]
    attachments: Optional[List[FwdMessageAttachment]]
    conversation_message_id: Optional[int]
    peer_id: Optional[int]
    id: Optional[int]

    def __init__(self, date: Optional[int], from_id: Optional[int], text: Optional[str], attachments: Optional[List[FwdMessageAttachment]], conversation_message_id: Optional[int], peer_id: Optional[int], id: Optional[int]) -> None:
        self.date = date
        self.from_id = from_id
        self.text = text
        self.attachments = attachments
        self.conversation_message_id = conversation_message_id
        self.peer_id = peer_id
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> 'FwdMessage':
        assert isinstance(obj, dict)
        date = from_union([from_int, from_none], obj.get("date"))
        from_id = from_union([from_int, from_none], obj.get("from_id"))
        text = from_union([from_str, from_none], obj.get("text"))
        attachments = from_union([lambda x: from_list(FwdMessageAttachment.from_dict, x), from_none], obj.get("attachments"))
        conversation_message_id = from_union([from_int, from_none], obj.get("conversation_message_id"))
        peer_id = from_union([from_int, from_none], obj.get("peer_id"))
        id = from_union([from_int, from_none], obj.get("id"))
        return FwdMessage(date, from_id, text, attachments, conversation_message_id, peer_id, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_union([from_int, from_none], self.date)
        result["from_id"] = from_union([from_int, from_none], self.from_id)
        result["text"] = from_union([from_str, from_none], self.text)
        result["attachments"] = from_union([lambda x: from_list(lambda x: to_class(FwdMessageAttachment, x), x), from_none], self.attachments)
        result["conversation_message_id"] = from_union([from_int, from_none], self.conversation_message_id)
        result["peer_id"] = from_union([from_int, from_none], self.peer_id)
        result["id"] = from_union([from_int, from_none], self.id)
        return result


class LastMessage:
    date: Optional[int]
    from_id: Optional[int]
    id: Optional[int]
    out: Optional[int]
    peer_id: Optional[int]
    text: Optional[str]
    conversation_message_id: Optional[int]
    fwd_messages: Optional[List[FwdMessage]]
    important: Optional[bool]
    random_id: Optional[int]
    attachments: Optional[List[Any]]
    is_hidden: Optional[bool]
    update_time: Optional[int]

    def __init__(self, date: Optional[int], from_id: Optional[int], id: Optional[int], out: Optional[int], peer_id: Optional[int], text: Optional[str], conversation_message_id: Optional[int], fwd_messages: Optional[List[FwdMessage]], important: Optional[bool], random_id: Optional[int], attachments: Optional[List[Any]], is_hidden: Optional[bool], update_time: Optional[int]) -> None:
        self.date = date
        self.from_id = from_id
        self.id = id
        self.out = out
        self.peer_id = peer_id
        self.text = text
        self.conversation_message_id = conversation_message_id
        self.fwd_messages = fwd_messages
        self.important = important
        self.random_id = random_id
        self.attachments = attachments
        self.is_hidden = is_hidden
        self.update_time = update_time

    @staticmethod
    def from_dict(obj: Any) -> 'LastMessage':
        assert isinstance(obj, dict)
        date = from_union([from_int, from_none], obj.get("date"))
        from_id = from_union([from_int, from_none], obj.get("from_id"))
        id = from_union([from_int, from_none], obj.get("id"))
        out = from_union([from_int, from_none], obj.get("out"))
        peer_id = from_union([from_int, from_none], obj.get("peer_id"))
        text = from_union([from_str, from_none], obj.get("text"))
        conversation_message_id = from_union([from_int, from_none], obj.get("conversation_message_id"))
        fwd_messages = from_union([lambda x: from_list(FwdMessage.from_dict, x), from_none], obj.get("fwd_messages"))
        important = from_union([from_bool, from_none], obj.get("important"))
        random_id = from_union([from_int, from_none], obj.get("random_id"))
        attachments = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("attachments"))
        is_hidden = from_union([from_bool, from_none], obj.get("is_hidden"))
        update_time = from_union([from_int, from_none], obj.get("update_time"))
        return LastMessage(date, from_id, id, out, peer_id, text, conversation_message_id, fwd_messages, important, random_id, attachments, is_hidden, update_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_union([from_int, from_none], self.date)
        result["from_id"] = from_union([from_int, from_none], self.from_id)
        result["id"] = from_union([from_int, from_none], self.id)
        result["out"] = from_union([from_int, from_none], self.out)
        result["peer_id"] = from_union([from_int, from_none], self.peer_id)
        result["text"] = from_union([from_str, from_none], self.text)
        result["conversation_message_id"] = from_union([from_int, from_none], self.conversation_message_id)
        result["fwd_messages"] = from_union([lambda x: from_list(lambda x: to_class(FwdMessage, x), x), from_none], self.fwd_messages)
        result["important"] = from_union([from_bool, from_none], self.important)
        result["random_id"] = from_union([from_int, from_none], self.random_id)
        result["attachments"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.attachments)
        result["is_hidden"] = from_union([from_bool, from_none], self.is_hidden)
        result["update_time"] = from_union([from_int, from_none], self.update_time)
        return result


class Item:
    conversation: Optional[Conversation]
    last_message: Optional[LastMessage]

    def __init__(self, conversation: Optional[Conversation], last_message: Optional[LastMessage]) -> None:
        self.conversation = conversation
        self.last_message = last_message

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        conversation = from_union([Conversation.from_dict, from_none], obj.get("conversation"))
        last_message = from_union([LastMessage.from_dict, from_none], obj.get("last_message"))
        return Item(conversation, last_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["conversation"] = from_union([lambda x: to_class(Conversation, x), from_none], self.conversation)
        result["last_message"] = from_union([lambda x: to_class(LastMessage, x), from_none], self.last_message)
        return result


class OnlineInfo:
    visible: Optional[bool]
    is_online: Optional[bool]
    last_seen: Optional[int]
    app_id: Optional[int]
    is_mobile: Optional[bool]

    def __init__(self, visible: Optional[bool], is_online: Optional[bool], last_seen: Optional[int], app_id: Optional[int], is_mobile: Optional[bool]) -> None:
        self.visible = visible
        self.is_online = is_online
        self.last_seen = last_seen
        self.app_id = app_id
        self.is_mobile = is_mobile

    @staticmethod
    def from_dict(obj: Any) -> 'OnlineInfo':
        assert isinstance(obj, dict)
        visible = from_union([from_bool, from_none], obj.get("visible"))
        is_online = from_union([from_bool, from_none], obj.get("is_online"))
        last_seen = from_union([from_int, from_none], obj.get("last_seen"))
        app_id = from_union([from_int, from_none], obj.get("app_id"))
        is_mobile = from_union([from_bool, from_none], obj.get("is_mobile"))
        return OnlineInfo(visible, is_online, last_seen, app_id, is_mobile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["visible"] = from_union([from_bool, from_none], self.visible)
        result["is_online"] = from_union([from_bool, from_none], self.is_online)
        result["last_seen"] = from_union([from_int, from_none], self.last_seen)
        result["app_id"] = from_union([from_int, from_none], self.app_id)
        result["is_mobile"] = from_union([from_bool, from_none], self.is_mobile)
        return result


class Profile:
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    is_closed: Optional[bool]
    can_access_closed: Optional[bool]
    sex: Optional[int]
    screen_name: Optional[str]
    photo_50: Optional[str]
    photo_100: Optional[str]
    online: Optional[int]
    online_info: Optional[OnlineInfo]
    online_app: Optional[int]
    online_mobile: Optional[int]

    def __init__(self, id: Optional[int], first_name: Optional[str], last_name: Optional[str], is_closed: Optional[bool], can_access_closed: Optional[bool], sex: Optional[int], screen_name: Optional[str], photo_50: Optional[str], photo_100: Optional[str], online: Optional[int], online_info: Optional[OnlineInfo], online_app: Optional[int], online_mobile: Optional[int]) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_closed = is_closed
        self.can_access_closed = can_access_closed
        self.sex = sex
        self.screen_name = screen_name
        self.photo_50 = photo_50
        self.photo_100 = photo_100
        self.online = online
        self.online_info = online_info
        self.online_app = online_app
        self.online_mobile = online_mobile

    @staticmethod
    def from_dict(obj: Any) -> 'Profile':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        first_name = from_union([from_str, from_none], obj.get("first_name"))
        last_name = from_union([from_str, from_none], obj.get("last_name"))
        is_closed = from_union([from_bool, from_none], obj.get("is_closed"))
        can_access_closed = from_union([from_bool, from_none], obj.get("can_access_closed"))
        sex = from_union([from_int, from_none], obj.get("sex"))
        screen_name = from_union([from_str, from_none], obj.get("screen_name"))
        photo_50 = from_union([from_str, from_none], obj.get("photo_50"))
        photo_100 = from_union([from_str, from_none], obj.get("photo_100"))
        online = from_union([from_int, from_none], obj.get("online"))
        online_info = from_union([OnlineInfo.from_dict, from_none], obj.get("online_info"))
        online_app = from_union([from_int, from_none], obj.get("online_app"))
        online_mobile = from_union([from_int, from_none], obj.get("online_mobile"))
        return Profile(id, first_name, last_name, is_closed, can_access_closed, sex, screen_name, photo_50, photo_100, online, online_info, online_app, online_mobile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["first_name"] = from_union([from_str, from_none], self.first_name)
        result["last_name"] = from_union([from_str, from_none], self.last_name)
        result["is_closed"] = from_union([from_bool, from_none], self.is_closed)
        result["can_access_closed"] = from_union([from_bool, from_none], self.can_access_closed)
        result["sex"] = from_union([from_int, from_none], self.sex)
        result["screen_name"] = from_union([from_str, from_none], self.screen_name)
        result["photo_50"] = from_union([from_str, from_none], self.photo_50)
        result["photo_100"] = from_union([from_str, from_none], self.photo_100)
        result["online"] = from_union([from_int, from_none], self.online)
        result["online_info"] = from_union([lambda x: to_class(OnlineInfo, x), from_none], self.online_info)
        result["online_app"] = from_union([from_int, from_none], self.online_app)
        result["online_mobile"] = from_union([from_int, from_none], self.online_mobile)
        return result


class Response:
    count: Optional[int]
    items: Optional[List[Item]]
    unread_count: Optional[int]
    profiles: Optional[List[Profile]]
    groups: Optional[List[Group]]

    def __init__(self, count: Optional[int], items: Optional[List[Item]], unread_count: Optional[int], profiles: Optional[List[Profile]], groups: Optional[List[Group]]) -> None:
        self.count = count
        self.items = items
        self.unread_count = unread_count
        self.profiles = profiles
        self.groups = groups

    @staticmethod
    def from_dict(obj: Any) -> 'Response':
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        items = from_union([lambda x: from_list(Item.from_dict, x), from_none], obj.get("items"))
        unread_count = from_union([from_int, from_none], obj.get("unread_count"))
        profiles = from_union([lambda x: from_list(Profile.from_dict, x), from_none], obj.get("profiles"))
        groups = from_union([lambda x: from_list(Group.from_dict, x), from_none], obj.get("groups"))
        return Response(count, items, unread_count, profiles, groups)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([from_int, from_none], self.count)
        result["items"] = from_union([lambda x: from_list(lambda x: to_class(Item, x), x), from_none], self.items)
        result["unread_count"] = from_union([from_int, from_none], self.unread_count)
        result["profiles"] = from_union([lambda x: from_list(lambda x: to_class(Profile, x), x), from_none], self.profiles)
        result["groups"] = from_union([lambda x: from_list(lambda x: to_class(Group, x), x), from_none], self.groups)
        return result


class Convestation:
    response: Optional[Response]

    def __init__(self, response: Optional[Response]) -> None:
        self.response = response

    @staticmethod
    def from_dict(obj: Any) -> 'Convestation':
        assert isinstance(obj, dict)
        response = from_union([Response.from_dict, from_none], obj.get("response"))
        return Convestation(response)

    def to_dict(self) -> dict:
        result: dict = {}
        result["response"] = from_union([lambda x: to_class(Response, x), from_none], self.response)
        return result


def convestation_from_dict(s: Any) -> Convestation:
    return Convestation.from_dict(s)


def convestation_to_dict(x: Convestation) -> Any:
    return to_class(Convestation, x)

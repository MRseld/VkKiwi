# -*- coding: utf-8 -*-
import json

import requests

import settings


def VkApiCallMethod(method: str, params: list):
    _params = ""
    for i in params:
        print(i)
        _params = _params + i + "&"

    requestsUrl = settings.api_domain_name + method + "?" + _params + "access_token=" + settings.access_token + "&v=" + settings.api_version
    print(requestsUrl)
    response = requests.get(requestsUrl).text
    error = None
    # print(response)
    return response


class Messages():
    def send(self, peer_id, text):
        return json.loads(
            VkApiCallMethod("messages.send", ["random_id=1", "peer_id=" + str(peer_id), "message=" + str(text)]))

    def get(self, count, offset, extended):
        return json.loads(VkApiCallMethod("messages.getConversations",
                                          ["extended=" + str(extended), "count=" + str(count),
                                           "offset=" + str(offset)]))

    def getHistory(self, count:int, offset:int, peer_id:int, rev:int, extended:int):
        return json.loads(VkApiCallMethod("messages.getHistory",
                                          ["count=" + str(count), "offset=" + str(offset), "peer_id=" + str(peer_id),
                                           "rev=" + str(rev), "extended=" + str(extended)]))


class Audios():
    def get(self, count: int, offset: int, owner_id: int = None, albumID: int = None):
        if (owner_id != None):

            if (albumID != None):
                return json.loads(VkApiCallMethod(
                    "audio.get", [
                        "owner_id=" + str(owner_id),
                        "offset=" + str(offset),
                        "count=" + str(count),
                        "album_id=" + str(albumID)
                    ]
                ))

            return json.loads(VkApiCallMethod(
                "audio.get", [
                    "owner_id=" + str(owner_id),
                    "offset=" + str(offset),
                    "count=" + str(count)
                ]
            ))

        else:
            if (albumID != None):
                return json.loads(VkApiCallMethod(
                    "audio.get", [
                        "offset=" + str(offset),
                        "count=" + str(count),
                        "album_id=" + str(albumID)
                    ]
                ))

            return json.loads(VkApiCallMethod(
                "audio.get", [
                    "offset=" + str(offset),
                    "count=" + str(count)

                ]
            ))

    def getAlbums(self, count, offset, owner_id=None):
        if (owner_id != None):
            return json.loads(VkApiCallMethod(
                "audio.getPlaylists", [
                    "owner_id=" + str(owner_id),
                    "offset=" + str(offset),
                    "count=" + str(count)
                ]
            ))
        else:
            return json.loads(VkApiCallMethod(
                "audio.getPlaylists", [
                    "owner_id=" + str(settings.userid),
                    "offset=" + str(offset),
                    "count=" + str(count)
                ]
            ))

    def getById(self, owner_id, audio_id):
        return json.loads(VkApiCallMethod("audio.getById", [
            "audios=" + str(owner_id) + "_" + str(audio_id)
        ]
                                          ))


class LongPoll():
    _longpolldata = None

    _server = None
    _key = None
    _ts = None
    _mode = None

    def getLongPollServer(self):

        longpoll = json.loads(VkApiCallMethod("messages.getLongPollServer", ["lp_version=3"]))
        self.setKey(longpoll["response"]["key"])
        self.setTs(longpoll["response"]["ts"])
        self.setServer(longpoll["response"]["server"])

    def RequestServer(self):
        request = requests.get("https://" + self.getServer() + "?act=a_check&key=" + str(self.getKey()) + "&ts=" + str(
            self.getTs()) + "&wait=25&mode=" + str(self.getMode()) + "&version=3").text
        self._longpolldata = json.loads(request)
        if "Failed" in self._longpolldata:
            self.getLongPollServer()
        else:
            self.setTs(self._longpolldata["ts"])

    def getLongPolldata(self):
        return self._longpolldata

    def update(self):
        pass

    def setKey(self, value):
        self._key = value

    def setTs(self, value):
        self._ts = value

    def setServer(self, value):
        self._server = value

    def setMode(self, value):
        self._mode = value

    def getKey(self):
        return self._key

    def getTs(self):
        return self._ts

    def getServer(self):
        return self._server

    def getMode(self):
        return self._mode

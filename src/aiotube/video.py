from ._threads import _Thread
from ._http import _get_video_data
from ._rgxs import _VideoPatterns as rgx
from typing import List, Optional, Dict, Any

class Video:

    HEAD = 'https://www.youtube.com/watch?v='

    def __init__(self, video_id: str):

        if 'watch?v=' in video_id:
            ids = video_id.split('=')
            self._id = ids[-1]
            self._url = video_id

        elif 'youtu.be/' in video_id:
            ids = video_id.split('/')
            self._id = ids[-1]
            self._url = self.HEAD + self._id

        else:
            self._id = video_id
            self._url = self.HEAD + self._id

    @property
    def url(self) -> str:
        return self._url

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> Optional[str]:
        """
        :return: the title of the video
        """
        raw = _get_video_data(self._id)
        data = rgx.title.findall(raw)
        return data[0] if data else None

    @property
    def views(self) -> Optional[str]:
        """
        :return: total views the video got so far
        """
        raw = _get_video_data(self._id)
        data = rgx.views.findall(raw)
        return data[0][:-6] if data else None

    @property
    def likes(self) -> Optional[str]:
        """
        :return: total likes the video got so far
        """
        raw = _get_video_data(self._id)
        data = rgx.likes.findall(raw)
        return data[0] if data else None

    @property
    def duration(self) -> Optional[float]:
        """
        :return: total duration of  the video in seconds
        """
        raw = _get_video_data(self._id)
        data = rgx.duration.findall(raw)
        return int(data[0]) / 1000 if data else None

    @property
    def upload_date(self) -> Optional[str]:
        """
        :return: the date on which the video has been uploaded
        """
        raw = _get_video_data(self._id)
        data = rgx.upload_date.findall(raw)
        return data[0] if data else None

    @property
    def author(self) -> Optional[str]:
        """
        :return: the id of the channel from which the video belongs
        """
        raw = _get_video_data(self._id)
        data = rgx.author_id.findall(raw)
        return data[0] if data else None

    @property
    def description(self) -> Optional[str]:
        """
        :return: description provided with the video
        """
        raw = _get_video_data(self._id)
        data = rgx.description.findall(raw)
        return data[0].replace('\\n', '\n') if data else None

    @property
    def thumbnail(self) -> Optional[str]:
        """
        :return: _url of the thumbnail of the video
        """
        raw = _get_video_data(self._id)
        data = rgx.thumbnail.findall(raw)
        return data[0] if data else None

    @property
    def tags(self) -> Optional[List[str]]:
        """
        :return: list of tags used in video meta-data
        """
        raw = _get_video_data(self._id)
        data = rgx.tags.findall(raw)
        return data[0].split(',') if data else None

    @property
    def streamed(self) -> bool:
        if rgx.is_streamed.search(_get_video_data(self._id)):
            return True
        return False

    @property
    def info(self) -> Dict[str, Any]:
        """
        :return: dict containing the whole info of the video
        """
        raw = _get_video_data(self._id)

        def _get_data(pattern):
            data = pattern.findall(raw)
            return data[0] if len(data) > 0 else None

        patterns = [
            rgx.title, rgx.views, rgx.likes, rgx.duration, rgx.author_id,
            rgx.upload_date, rgx.thumbnail, rgx.tags, rgx.description
        ]

        data = _Thread.run(_get_data, patterns)

        return {
            'title': data[0],
            'id': self._id,
            'views': data[1][:-6] if data[1] else None,
            'likes': data[2],
            'duration': int(data[3]) / 1000 if data[3] else None,
            'author': data[4],
            'upload_date': data[5],
            'url': self._url,
            'thumbnail': data[6],
            'tags': data[7].split(','),
            'description': data[8].replace('\\n', '\n') if data[8] else None,
        }

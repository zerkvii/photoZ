import json


class Error:
    def __init__(self, type, info):
        """
        :param type: int{0:'success',1:'warning',2:'error'}
        :param info: str
        """
        self.__index = {0: 'success', 1: 'warning', 2: 'error'}
        self.__type = type
        self.__info = info

    def _to_json(self):
        json_dict = {
            'type': self.__index[self.__type],
            'info': self.__info
        }
        return json.dumps(json_dict)


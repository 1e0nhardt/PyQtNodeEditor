from collections import OrderedDict
import typing


class Serializable(object):
    
    def __init__(self) -> None:
        self.id = id(self)
    
    def serialize(self):
        raise NotImplementedError()
    
    def deserialize(self, data: OrderedDict, hashmap: typing.Optional[dict] = ..., restore_id: bool = True):
        raise NotImplementedError()
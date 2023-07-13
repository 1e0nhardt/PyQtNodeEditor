class Serializable(object):
    
    def __init__(self) -> None:
        self.id = id(self)
    
    def serialize(self):
        raise NotImplemented()
    
    def deserialize(self, data, hashmap={}):
        raise NotImplemented()
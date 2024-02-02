from abc import ABC, abstractmethod

"""
class AutoStorage:
    __counter = 0
    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)
        
    , AutoStorage
"""

class Validated(ABC):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        instance.__dict__[self.name] = value

    def __get__(self, instance, value):
        return instance.__dict__[self.name]

    def __set_name__(self, owner, name):
        self.name = name

    @abstractmethod
    def validate(self, instance, value):
        """возвращает проверенное значение или возбуждает ValueError"""

class Quantity(Validated):
    """число >0"""
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value

class Discrete(Validated):
    """число 1 или 0"""
    def validate(self, instance, value):
        if not (value == 0 or value == 1):
            raise ValueError('value must be 0 or 1')
        return value

class NonBlank(Validated):
    """строка содержит хотя бы один непробельный символ"""
    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value

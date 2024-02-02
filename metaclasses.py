from abc import ABCMeta, abstractmethod
from decorators import logged

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonABCMeta(ABCMeta):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class AbstractDatabaseClient(metaclass=SingletonABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.index = ""  # table
        self.index_to_map_dict = {}
        self.query_settings = {}
        self.query = {}

    @abstractmethod
    def connect(self):
        """
        make connection to database
        :return (bool, msg): 
        """

    @abstractmethod
    def check_index(self, index, map):
        """
        check pum index/table with map in database
        :param index: 
        :param map: 
        :return (bool, msg): 
        """

    @abstractmethod
    def write(self, index, HL_list, S_list, signals):
        """
        write to database for selected index/table
        :param index: 
        :param HL_list: 
        :param S_list: 
        :param signals: 
        :return: 
        """

    @abstractmethod
    def form_query(self, query_settings):
        """
        form query from query_settings for search
        :param query_settings: 
        :return: 
        """

    @abstractmethod
    def search(self, query_settings):
        """
        get data for query
        :param query: 
        :param query_settings: 
        :return: 
        """

    @abstractmethod
    def get_recent(self, index):
        """
        get recent row for index/table
        :param index: 
        :return: 
        """

class AbstractQuery(metaclass=SingletonABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.index = ""  # table
        self.index_to_map_dict = {}
        self.query_settings = {}
        self.query = {}

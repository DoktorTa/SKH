from abc import ABCMeta, abstractmethod


class IFSWork(metaclass=ABCMeta):
    """
        Интерфейс который определяет методы работы с файловыми системами

        Metods:
        ~~~~~~~~~~~~~~~~~~
            **read**
            **cd**
            **get_root**
            **get_pwd**
    """

    @abstractmethod
    def read(self, dir_now: str, num_in_dir: int, count: int, pointer: int) -> (str, list, int, int):
        """
            Прочесть данный блок||кластер файловой системы.
        """
        print("read abc metod: read block file")

    @abstractmethod
    def cd(self, dir_now: str, num_in_dir: int) -> (list, int):
        """
            Реализует перемешение по директориям в файловой системе в лучших традициях командной строки.
        """
        print("cd abc metod: move on directory")

    @property
    @abstractmethod
    def root(self) -> list:
        """
            Возврашает содержимое корневого котолога файловой системы.
        """
        print("get root directory")
        return []

    @property
    @abstractmethod
    def pwd(self) -> str:
        """
            Возврашает имя текушего каталога.
        """
        print("get pwd directory")
        return ""

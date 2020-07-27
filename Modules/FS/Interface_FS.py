from abc import ABCMeta, abstractmethod


class IFSWork(metaclass=ABCMeta):
    """
        Интерфейс который определяет методы работы с файловыми системами
    """

    @abstractmethod
    def read(self):
        """
            Прочесть данный блок||кластер файловой системы.
        """
        print("read abc metod: read block file")

    @abstractmethod
    def cd(self):
        """
            Реализует перемешение по директориям в файловой системе в лучших традициях командной строки.
        """
        print("cd abc metod: move on directory")

    @abstractmethod
    def get_root(self):
        """
            Возврашает содержимое корневого котолога файловой системы.
        """
        print("get root directory")

    @abstractmethod
    def get_pwd(self):
        """
            Возврашает имя текушего каталога.
        """
        print("get pwd directory")

from abc import ABCMeta, abstractmethod


class IExecutableFile(metaclass=ABCMeta):

    @abstractmethod
    def get_header(self) -> dict:
        """
            Метод возврашает словарь который должен удовлетворять:
                key           value
                "extension" - Расширение файла.
                "border"    - Порядок байт.
                "bitclass"  - Разрядность системы.
                "amachine"  - Архитектура платформы на которой создан файл.
        """

    @abstractmethod
    def get_table_header(self) -> list:
        """
            Метод должен возвращать лист из листов произвольной длинны,
             в котором в необходимом вам формате соритированы записи в таблице
              заголовков.
        """

    @abstractmethod
    def get_section_table(self) -> list:
        """
            Метод должен возвращать лист из листов произвольной длинны,
             в котором в необходимом вам формате соритированы записи в таблице
              секций.
        """

from abc import ABCMeta, abstractmethod


class IExecutableFile(metaclass=ABCMeta):

    @abstractmethod
    def get_hendler(self) -> dict:
        """
            Метод возврашает словарь который должен удовлетворять:
                key           value
                "extension" - Расширение файла.
                "border"    - Порядок байт.
                "bitclass"  - Разрядность системы.
                "amachine"  - Архитектура аппаратной платформы на которой создан файл.
        """

    @abstractmethod
    def get_table_hendler(self) -> list:
        """
            Метод должен возвращать лист из листов произвольной длинны,
             в котором в необходимом вам формате соритированы записи в таблице заголовков.
        """

    def get_section_table(self) -> list:
        """
            Метод должен возвращать лист из листов произвольной длинны,
             в котором в необходимом вам формате соритированы записи в таблице секций.
        """

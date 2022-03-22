from abc import abstractmethod
from typing import List

from src.embedded_project.main.dir_reader.file_model import FileModel


class DirReaderApi:
    """
    Base interface for the directory reader api.
    """
    @abstractmethod
    def read_files(self) -> List[FileModel]:
        """
        Returns all files within the provided directory.
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """
        rm -rf the provided directory then re-create it.
        """
        raise NotImplementedError

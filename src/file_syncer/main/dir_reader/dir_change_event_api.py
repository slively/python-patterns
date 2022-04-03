from queue import Queue

from src.file_syncer.main.dir_reader.directory_model import DirectoryChangesModel


class DirChangeEventApi:
    """
    A simple interface for sending directory change events.
    Default implementation is a no-op.
    """

    def send_event(self, event: DirectoryChangesModel) -> None:
        pass


class DirChangeEventQueue(DirChangeEventApi):
    """
    A change event implementation that just puts messages on a queue.
    """

    def __init__(self, queue: Queue) -> None:
        self.queue = queue

    def send_event(self, event: DirectoryChangesModel) -> None:
        self.queue.put(event)

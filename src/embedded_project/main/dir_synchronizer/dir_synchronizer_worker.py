from logging import getLogger
from queue import Queue
from typing import Optional

from src.embedded_project.main.dir_synchronizer.dir_synchronizer_api import (
    DirSynchronizerApi,
)
from src.utils.worker_utils import BaseWorker

log = getLogger(__name__)


class DirSynchronizerWorker(BaseWorker):
    """
    A worker that reads from a queue and synchronizes directory changes.
    """

    def __init__(
        self,
        stop_timeout_seconds: Optional[float],
        api: DirSynchronizerApi,
        queue: Queue,
    ) -> None:
        super().__init__(stop_timeout_seconds)
        self.api = api
        self.queue = queue

    def _run(self) -> None:
        """
        Polls the queue and sends events to the api.
        """
        log.info("Starting directory synchronizer worker.")
        while self.running:
            changes = self.queue.get()  # wait for an event
            self.api.sync(changes)  # sync it

from unittest import TestCase
from src.file_syncer.tests.test_utils import runIfFileSystem


@runIfFileSystem()
class DirSynchronizerCtrlTest(TestCase):
    def test_synchronizes_file_changes(self) -> None:
        pass

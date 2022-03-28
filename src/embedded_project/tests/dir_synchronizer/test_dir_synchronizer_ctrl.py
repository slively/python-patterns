from unittest import TestCase
from src.embedded_project.tests.test_utils import runIfFileSystem


@runIfFileSystem()
class DirSynchronizerCtrlTest(TestCase):
    def test_synchronizes_file_changes(self) -> None:
        pass

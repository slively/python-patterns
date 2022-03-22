from time import sleep
from unittest import TestCase
from unittest.mock import create_autospec
from src.embedded_project.main.dir_reader.dir_reader_api import DirReaderApi
from src.embedded_project.main.dir_reader.file_model import FileModel
from src.embedded_project.main.worker.worker import Worker
from src.utils.sleep_utils import sleep_until


test_loop_delay_seconds = .1
two_loops = test_loop_delay_seconds * 2

class WorkerTest(TestCase):
    def test_correct_detects_changes_in_directory(self) -> None:
        api = create_autospec(DirReaderApi)
        api.read_files.return_value = []

        with Worker(stop_timeout_seconds=.5, loop_delay_seconds=test_loop_delay_seconds, api=api) as w:
            # no files yet
            self.assertEqual(0, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(0, w.deleted_file_count)
            

            # 1 new file shows up
            api.read_files.return_value = [
                FileModel(name = "name.txt", path="name.txt", is_dir=False, contents="")
            ]
            sleep_until(lambda: w.new_file_count == 1)
            self.assertEqual(1, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(0, w.deleted_file_count)

            # 1 new file shows up and 1 deleted
            api.read_files.return_value = [
                FileModel(name = "name2.txt", path="name2.txt", is_dir=False, contents="name2")
            ]
            sleep_until(lambda: w.deleted_file_count == 1)
            self.assertEqual(2, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(1, w.deleted_file_count)

            # 1 file changed
            api.read_files.return_value = [
                FileModel(name = "name2.txt", path="name2.txt", is_dir=False, contents="name2 changed")
            ]
            sleep_until(lambda: w.changed_file_count == 1)
            self.assertEqual(2, w.new_file_count)
            self.assertEqual(1, w.changed_file_count)
            self.assertEqual(1, w.deleted_file_count)

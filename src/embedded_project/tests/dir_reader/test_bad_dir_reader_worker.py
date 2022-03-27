import os
from unittest import TestCase
from src.embedded_project.main.dir_reader.dir_reader_worker_bad import (
    BadDirReaderWorker,
)
from src.utils.file_utils import clean_and_remake_dir
from src.utils.logger_utils import basic_logging
from src.utils.sleep_utils import sleep_until

basic_logging()
test_dir = os.path.join(os.path.dirname(__file__), "tmp")


class WorkerTest(TestCase):
    def setUp(self) -> None:
        clean_and_remake_dir(test_dir)

    def test_correct_detects_changes_in_directory(self) -> None:
        w = BadDirReaderWorker(dir=test_dir)

        try:
            w.start()

            # no files yet
            self.assertEqual(0, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(0, w.deleted_file_count)

            # 1 new file shows up with no contents
            first_file = os.path.join(test_dir, "name.txt")
            with open(first_file, "w+") as f:
                f.write("contents")
            sleep_until(lambda: w.new_file_count == 1)
            self.assertEqual(1, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(0, w.deleted_file_count)

            # 1 new file shows up and 1 deleted
            second_file = os.path.join(test_dir, "name2.txt")
            with open(second_file, "w+") as f:
                f.write("name2")

            sleep_until(lambda: w.new_file_count == 2)
            os.remove(first_file)
            sleep_until(lambda: w.deleted_file_count == 1)
            self.assertEqual(2, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(1, w.deleted_file_count)

            # 1 file changed
            with open(second_file, "w+") as f:
                f.write("name2 changed")
            sleep_until(lambda: w.changed_file_count == 1)
            self.assertEqual(2, w.new_file_count)
            self.assertEqual(1, w.changed_file_count)
            self.assertEqual(1, w.deleted_file_count)

        finally:
            w.stop()

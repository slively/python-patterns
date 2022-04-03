from unittest import TestCase
from src.file_syncer.main.dir_reader.directory_model import DirectoryModel
from src.file_syncer.main.dir_reader.file_model import FileModel


class DirectoryModelTest(TestCase):
    def test_directory_with_no_changes(self) -> None:
        first = DirectoryModel(files=[])
        second = DirectoryModel(files=[])

        self.assertFalse(first.diff(second).changes_detected)

    def test_directory_with_new_file(self) -> None:
        first = DirectoryModel(files=[])
        second = DirectoryModel(
            files=[
                FileModel(name="name.txt", path="name.txt", is_dir=False, contents="")
            ],
        )

        self.assertTrue(first.diff(second).changes_detected)
        self.assertEqual(second.files, first.diff(second).new_files)

        third = DirectoryModel(
            files=[
                FileModel(name="name2.txt", path="name2.txt", is_dir=False, contents=""),
                FileModel(
                    name="name.txt", path="name.txt", is_dir=False, contents=""
                ),
            ],
        )

        self.assertEqual(third.files, first.diff(third).new_files)

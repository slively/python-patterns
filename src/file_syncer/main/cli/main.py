from src.file_syncer.main.cli.diff_command import DiffCommand
from src.file_syncer.main.cli.list_command import ListCommand
from src.file_syncer.main.cli.reset_command import ResetCommand
from src.utils.main.cli_utils import RootCliCommand
from src.utils.main.logger_utils import basic_logging

basic_logging()


def run() -> None:
    cli = RootCliCommand(description="CLI for example embedded project.")
    cli.subcommands(
        commands=[
            ListCommand(
                name="list", description="List files currently in the directory."
            ),
            DiffCommand(
                name="diff", description="Diff files between directories."
            ),
            ResetCommand(
                name="reset", description="Reset files currently in the directory."
            ),
        ]
    )
    cli.run()


if __name__ == "__main__":
    run()

from src.embedded_project.main.cli.list_command import ListCommand
from src.embedded_project.main.cli.reset_command import ResetCommand
from src.utils.cli_utils import RootCliCommand
from src.utils.logger_utils import basic_logging

basic_logging()


def run() -> None:
    cli = RootCliCommand(description="CLI for example embedded project.")
    cli.subcommands(
        commands=[
            ListCommand(
                name="list", description="List files currently in the directory."
            ),
            ResetCommand(
                name="reset", description="Reset files currently in the directory."
            ),
        ]
    )
    cli.run()


if __name__ == "__main__":
    run()

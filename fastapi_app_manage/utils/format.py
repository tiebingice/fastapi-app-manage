from black import format_file_in_place, Mode
from pathlib import Path


def format_directory_with_black():
    path = Path("app")

    for file_path in path.rglob('*.py'):
        try:
            changed = format_file_in_place(
                file_path,
                fast=False,
                mode=Mode(),
            )
        except Exception as e:
            print(f"Error formatting {file_path} with Black: {e}")

    format_file_in_place(
        Path("main.py"),
        fast=False,
        mode=Mode(),
    )

    format_file_in_place(
        Path("settings.py"),
        fast=False,
        mode=Mode(),
    )

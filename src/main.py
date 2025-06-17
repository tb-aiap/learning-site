"""Main module for static site generator."""

import argparse
import shutil
from pathlib import Path

from markdown_html import generate_pages_recursive


def clear_folder_contents(path: Path | str) -> None:
    print(f"deleting all files in {path}")
    path: Path = Path(path)

    for file in path.iterdir():
        if file.is_file():
            print(file, "is a file unlinking it.")
            file.unlink()
        elif file.is_dir():
            print(file, "is a dir, using shutil.rmtree()")
            shutil.rmtree(file)
        else:
            raise Exception(f"error identifying {file} as file or dir.")

    print(f"{path} is cleared")
    if len(list(path.iterdir())) != 0:
        raise Exception("there are still some files inside.")


def copy_folder_contents(from_path: Path | str, to_path: Path | str) -> None:
    print(f"copying all files in from {from_path} to {to_path}")

    from_path: Path = Path(from_path)
    to_path: Path = Path(to_path)

    if not to_path.is_dir():
        print(f"{to_path} doesnt exist, creating it.")
        to_path.mkdir(parents=True, exist_ok=True)

    for file in from_path.iterdir():
        if file.is_file():
            print(f"copying {file} to {to_path}")
            shutil.copy(file, to_path)
        elif file.is_dir():
            new_to_path = Path(to_path, file.name)
            copy_folder_contents(file, new_to_path)


def main(basepath: str) -> None:
    """Main entry point for sh files."""

    clear_folder_contents("./static")
    copy_folder_contents("./static", "./docs")

    generate_pages_recursive(
        dir_path_content="./content",
        template_path="./template.html",
        dest_dir_path="./docs",
        basepath=basepath,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "basepath",
        nargs="?",
        default="/",
        help="base path to generate the website pages",
    )
    args = parser.parse_args()

    main(args.basepath)

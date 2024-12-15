# import faulthandler
# faulthandler.enable()

from __future__ import print_function

import builtins as __builtin__
import logging
import os

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Column
from rich.theme import Theme

from modules import launch_utils  # noqa: E402

args = launch_utils.args
python = launch_utils.python
git = launch_utils.git
index_url = launch_utils.index_url
dir_repos = launch_utils.dir_repos

commit_hash = launch_utils.commit_hash
git_tag = launch_utils.git_tag

run = launch_utils.run
is_installed = launch_utils.is_installed
repo_dir = launch_utils.repo_dir

run_pip = launch_utils.run_pip
check_run_python = launch_utils.check_run_python
git_clone = launch_utils.git_clone
git_pull_recursive = launch_utils.git_pull_recursive
list_extensions = launch_utils.list_extensions
run_extension_installer = launch_utils.run_extension_installer
prepare_environment = launch_utils.prepare_environment
configure_for_tests = launch_utils.configure_for_tests
start = launch_utils.start


def set_rich():
    loglevel = os.environ.get("SD_WEBUI_LOG_LEVEL", "INFO").upper()
    console = Console(theme=Theme({"logging.level.ok": "green"}))
    level_ok = 25
    logging.addLevelName(level_ok, "OK")

    formatter = logging.Formatter(
        "%(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    handler = RichHandler(
        level=loglevel,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        console=console,
        show_time=False,
    )
    handler.setFormatter(formatter)
    logging.root.setLevel(loglevel)
    logging.root.handlers = [handler]
    # print_log = logging.getLogger()
    print_default = __builtin__.print
    __builtin__.print = lambda *args, **kwargs: (
        logging.root.log(level=level_ok, msg=" ".join(map(str, args)))
        if loglevel
        else print_default(*args, **kwargs)
    )
    progress = Progress(
        TextColumn("{task.id}", justify="right"),
        TextColumn("[progress.description]{task.description}"),
        ":",
        BarColumn(),
        MofNCompleteColumn(table_column=Column(justify="center")),
        "·",
        TimeElapsedColumn(),
        "->",
        TimeRemainingColumn(),
        TextColumn("{task.fields[info_1]}", justify="right"),
        TextColumn("{task.fields[info_2]}", justify="right"),
        console=console,
    )
    return progress


progress = set_rich()


def main():
    if args.dump_sysinfo:
        filename = launch_utils.dump_sysinfo()

        print(f"Sysinfo saved as {filename}. Exiting...")

        exit(0)

    launch_utils.startup_timer.record("initial startup")

    with launch_utils.startup_timer.subcategory("prepare environment"):
        if not args.skip_prepare_environment:
            prepare_environment()

    if args.test_server:
        configure_for_tests()

    if args.forge_ref_a1111_home:
        launch_utils.configure_forge_reference_checkout(args.forge_ref_a1111_home)

    start()


if __name__ == "__main__":
    main()

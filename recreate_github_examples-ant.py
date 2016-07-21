#! Py -3
"Tools for updating Github example-code repository"
from pathlib import Path
import sys
import os
import shutil
from betools import CmdLine
import config


def insert_copyright(lines):
    if "Copyright.txt" in lines[1]:
        return lines
    if lines[0][0] == "#":
        cmt = "#"
    else:
        cmt = "//"
    return [lines[0],
            cmt + " (c)2016 MindView LLC: see Copyright.txt\n",
            cmt + " We make no guarantees that this code is fit for any purpose.\n",
            cmt + " Visit http://mindviewinc.com/Books/OnJava/ for more book information.\n",
            ] + lines[1:]


@CmdLine('A')
def add_copyright():
    "Ensure copyright line is in all github example files"
    print("Ensuring copyright")
    candidates = \
        list(config.github_code_dir.rglob("*.java")) + \
        list(config.github_code_dir.rglob("*.py")) + \
        list(config.github_code_dir.rglob("*.cpp")) + \
        list(config.github_code_dir.rglob("*.go"))
    for c in candidates:
        with c.open() as code:
            lines = code.readlines()
        if lines[0].startswith("// ") or lines[0].startswith("# "):
            if "Copyright.txt" not in lines[1]:
                copyrighted = insert_copyright(lines)
                with c.open('w') as crighted:
                    crighted.writelines(copyrighted)


exclude = [
    "build.gradle",
    "gradlew",
    "gradlew.bat",
    "gradle",
    "appveyor.yml"
]

@CmdLine('c')
def clean_github_dir():
    "Clean github example code directory"
    print("Removing old github files >>>>>>>>>>>>")
    for f in (
            x for x in config.github_code_dir.glob("*")
            if not x.stem.startswith(".")
            and x.name not in exclude):
        print("removing: ", f.name)
        if f.is_dir():
            shutil.rmtree(str(f))
        else:
            f.unlink()


@CmdLine('e')
def copy_examples():
    "Copy example tree into github example code directory"
    print("Copying new github files >>>>>>>>>>>>")
    for di in (x for x in config.example_dir.glob("*")):
        print(di.name)
        if di.is_dir():
            shutil.copytree(str(di), str(config.github_code_dir / di.name))
        else:
            shutil.copyfile(str(di), str(config.github_code_dir / di.name))


@CmdLine('r')
def recreate_github_example_directory():
    """
    Extract code and antfiles, erase old github examples and copy new ones.
    Ensure copyright info is on each file.
    """
    examples_cmd = config.tools_dir / "Examples.py"
    os.system("python " + str(examples_cmd) + " -e" )
    clean_github_dir()
    copy_examples()
    add_copyright()


if __name__ == '__main__':
    CmdLine.run()
# py -3
# -*- coding: utf8 -*-
"""
Common tools for ebook building
"""
from pathlib import Path
import sys
import shutil
import config
import time

try:
    import psutil
except ImportError:
    print("""
    Download psutil wheel from:
    http://www.lfd.uci.edu/~gohlke/pythonlibs/#psutil
    Then run:
    pip install psutil-4.1.0-cp35-cp35m-win32.whl
    (you may need to substitute the latest version number)
    """)
    sys.exit(1)


def close_viewer():
    "Close PDF and eBook viewer"
    for p in psutil.process_iter():
        if p.name() == "PDFXCview.exe" or p.name() == "FoxitReader.exe" :
            print("Closing PDF Viewer")
            p.terminate()
        if p.name() == "ebook-viewer.exe":
            print("Closing eBook Viewer")
            p.terminate()


def populate_ebook_build_dir(target_dir):
    shutil.copytree(
        str(config.img_dir),
        str(target_dir / "images"))
    def copy(src):
        shutil.copy(src, target_dir)
    [copy(font) for font in config.fonts.glob("*")]
    copy(config.cover)
    copy(config.css)
    copy(config.metadata)
    copy(config.ebookResources / "chapter.png")
    copy(config.ebookResources / "subhead.png")
    copy(config.ebookResources / "level-2.png")
    copy(config.ebookResources / "onjava.tex")
    copy(config.ebookResources / "onjava.cls")


def remove_dir(target_dir):
    try:
        if target_dir.exists():
            print("Removing {}".format(target_dir))
            shutil.rmtree(str(target_dir))
            time.sleep(1)
    except:
        print("Error: could not remove {}".format(target_dir))
        sys.exit(1);


def recreate_build_dir(target_dir):
    "Create and populate a fresh build_dir"
    remove_dir(target_dir)
    target_dir.mkdir()
    populate_ebook_build_dir(target_dir)


def ensure_ebook_build_dir(target_dir):
    """
    Prepare ebook_build_dir for a build
    """
    if not target_dir.exists():
        target_dir.mkdir()
    # Use images dir as an indicator that "populate" hasn't been run:
    if not (target_dir / "images").exists():
        populate_ebook_build_dir(target_dir)
    shutil.copy(config.css, target_dir)
    print("css refreshed")
    if (target_dir / "epub_files").exists():
        shutil.rmtree(str(target_dir / "epub_files"))


def combine_markdown_files(source_dir, target_file):
    """
    Put markdown files together
    """
    assembled = ""
    for md in source_dir.glob("[0-9][0-9]_*.md"):
        print(str(md.name), end=", ")
        with md.open(encoding="utf8") as chapter:
            assembled += chapter.read() + "\n"
    with target_file.open('w', encoding="utf8") as book:
        book.write(assembled)
    print("\n\n")

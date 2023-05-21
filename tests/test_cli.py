from random import sample
import pytest
from minigit import data, base
import os
from pathlib import Path
import shutil

SAMPLE_PATH = Path("tests/sample/").resolve()


@pytest.fixture()
def tmp_folder_with_sample_data(tmp_path_factory):
    base_path = tmp_path_factory.mktemp("data", numbered=True)
    os.chdir(base_path)
    print(str(base_path))
    shutil.copytree(str(SAMPLE_PATH), str(base_path), dirs_exist_ok=True)
    return base_path


def test_init(tmp_folder_with_sample_data):
    """
    Test that the CLI init command works
    """
    data.init()
    assert Path(".minigit").exists() is True


def test_hash_object(tmp_folder_with_sample_data):
    """
    Test that the hash-object command works
    """
    cats_txt_hash = "caae3328bffd50ed72545610d781136e958591c597a527a8a46f87b2e5090ffc"
    data.init()
    hash = data.hash_object(Path("cats.txt").read_bytes())
    assert hash == cats_txt_hash
    assert Path(".minigit/objects/" + hash).exists() is True


def test_get_object(tmp_folder_with_sample_data):
    """
    Test that the get-object command works
    """
    data.init()
    hash = data.hash_object((SAMPLE_PATH / "cats.txt").read_bytes())
    assert data.get_object(hash) == Path(SAMPLE_PATH / "cats.txt").read_bytes()


def test_write_tree(tmp_folder_with_sample_data):
    """
    Test the write-tree command works based on the hash of the tree of the data from the sample data
    """
    data.init()
    sample_tree_hash = "b08eb8781a8d467556c78a384cb5048dc820f9d1c1ed5f7f769d0d5a6011a911"
    base_tree_hash = base.write_tree()
    assert sample_tree_hash == base_tree_hash


def test_read_tree(tmp_folder_with_sample_data):
    """
    Test that the read-tree command works
    """
    tmp_dir_files = []
    sample_dir_files = []
    data.init()
    # Write the tree to the minitgit object store
    tree_oid = base.write_tree()
    # Read the tree from the minitgit object store
    base.read_tree(tree_oid)
    for entry in Path(".").glob("*"):
        # Ignore .minigit folder
        if ".minigit" in entry.parts:
            continue
        tmp_dir_files.append(entry.relative_to(Path(".")))

    for entry in Path(SAMPLE_PATH).glob("*"):
        sample_dir_files.append(entry.relative_to(Path(SAMPLE_PATH)))
    assert tmp_dir_files == sample_dir_files

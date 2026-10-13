"""Tests for minigit branch."""

from minigit.refs import read_ref


def test_list_empty(repo, run):
    result = run("branch")
    assert result.code == 0
    assert result.out == ""


def test_list_after_commit(repo, run, write):
    write("a.txt", "a\n")
    run("add", "a.txt")
    run("commit", "-m", "first")
    result = run("branch")
    assert result.code == 0
    assert result.out == "* main\n"


def test_create_branch(repo, run, write):
    write("a.txt", "a\n")
    run("add", "a.txt")
    run("commit", "-m", "first")
    result = run("branch", "feature")
    assert result.code == 0
    assert result.out == ""
    result = run("branch")
    assert "* main" in result.out
    assert "  feature" in result.out


def test_create_with_start_point(repo, run, write):
    write("a.txt", "a\n")
    run("add", "a.txt")
    run("commit", "-m", "first")
    result = run("branch", "old-work", "HEAD")
    assert result.code == 0
    assert read_ref(repo, "refs/heads/old-work") == read_ref(repo, "HEAD")


def test_duplicate_branch(repo, run, write):
    write("a.txt", "a\n")
    run("add", "a.txt")
    run("commit", "-m", "first")
    run("branch", "feature")
    result = run("branch", "feature")
    assert result.code == 128
    assert "already exists" in result.err


def test_invalid_names(repo, run, write):
    write("a.txt", "a\n")
    run("add", "a.txt")
    run("commit", "-m", "first")
    for bad in ["", "has space", "has..dots", "ends/", "ends.lock"]:
        result = run("branch", bad)
        assert result.code == 128
        assert "invalid branch name" in result.err


def test_no_commits(repo, run):
    result = run("branch", "feature")
    assert result.code == 128
    assert "no commits yet" in result.err

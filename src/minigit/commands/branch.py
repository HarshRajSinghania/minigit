"""minigit branch: list and create branches."""

from minigit.errors import MinigitError
from minigit.refs import current_branch, iter_refs, read_ref, resolve, update_ref

NAME = "branch"
HELP = "List or create branches"


def configure(parser):
    parser.add_argument("name", nargs="?", help="name of the branch to create")
    parser.add_argument("start_point", nargs="?", help="commit to start the branch at (default: HEAD)")


def _is_valid_name(name: str) -> bool:
    if not name or " " in name or ".." in name or name.startswith("-") or name.endswith("/") or name.endswith(".lock"):
        return False
    return True


def run(args, repo):
    if args.name is None:
        # List branches
        branches = iter_refs(repo, "refs/heads")
        if not branches:
            return 0
        current = current_branch(repo)
        for name in sorted(branches):
            prefix = "* " if name == current else "  "
            print(f"{prefix}{name}")
        return 0

    # Create branch
    name = args.name
    if not _is_valid_name(name):
        raise MinigitError(f"invalid branch name: {name}")

    if read_ref(repo, f"refs/heads/{name}") is not None:
        raise MinigitError(f"a branch named '{name}' already exists")

    start = args.start_point or "HEAD"
    try:
        sha = resolve(repo, start)
    except MinigitError as e:
        if "does not point to a commit yet" in str(e) or "unknown revision" in str(e):
            raise MinigitError("no commits yet") from e
        raise

    update_ref(repo, f"refs/heads/{name}", sha)
    return 0

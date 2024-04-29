import pygit2

from dac.source import Source


class MyRemoteCallbacks(pygit2.RemoteCallbacks):

    def credentials(self, url, username_from_url, allowed_types):
        if allowed_types & pygit2.enums.CredentialType.USERNAME:
            return pygit2.Username("git")
        elif allowed_types & pygit2.enums.CredentialType.SSH_KEY:
            return pygit2.Keypair("git", "id_rsa.pub", "id_rsa", "")
        else:
            return None


class Git(Source):
    def init(self):
        # from git import Repo  # pip install gitpython
        # Repo.clone_from(git_url, repo_dir)

        print("Cloning gitstore over ssh with the username in the URL")
        keypair = pygit2.Keypair("git", "/home/x/.ssh/id_rsa.pub", "/home/x/.ssh/id_rsa", "")
        callbacks = pygit2.RemoteCallbacks(credentials=keypair)
        pygit2.clone_repository("ssh://git@core.r3d.sh:7999/x/gitstore.git", "temp.git",
                                callbacks=callbacks)

    def update(self):
        # import git  # pip install gitpython
        # git.Git("/your/directory/to/clone").clone("git://gitorious.org/git-python/mainline.git")
        pass


import time
import git
import os

SSH_KEY_PUBLIC = os.path.expanduser('~/.ssh/id_rsa.pub')
SSH_KEY_PRIVATE = os.path.expanduser('~/.ssh/id_rsa')

# # Example usage
repo_path = "ssh://git@core.r3d.sh:7999/x/gitstore.git"
local_path = "test1.git"
remote_name = "origin"
branch_name = "main"
check_interval = 10


def check_repo():
    print("checking repo")
    return "checked"


def lsremote(url):
    remote_refs = {}
    g = git.cmd.Git()
    for ref in g.ls_remote(url).split('\n'):
        hash_ref_list = ref.split('\t')
        remote_refs[hash_ref_list[1]] = hash_ref_list[0]
    return remote_refs


def monitoring():
    print(f"monitoring {repo_path}@{branch_name}")

    # Clone repo to monit
    if not os.path.isdir(f"{local_path}-{branch_name}"):
        git.Repo.clone_from(repo_path, f"{local_path}-{branch_name}", branch=branch_name, depth=1)

    repo = git.Repo(f"{local_path}-{branch_name}")

    last_commit = lsremote(repo_path)['HEAD']
    while True:
        current_commit = lsremote(repo_path)['HEAD']
        if last_commit != current_commit:
            print(f"change detected {current_commit}, pulling from repo")
            repo.remotes['origin'].pull()
            last_commit = current_commit

            commit_files = [file for file in repo.git.show(last_commit, name_only=True, format="%n").splitlines() if file]
            print("files affected by change:", commit_files)

        time.sleep(check_interval)

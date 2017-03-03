from subprocess import call
from os import chdir

tag = "4.0.6"

repos = []
fpLibTable = []

## Copy most-recent libtable into same dir
with open("fp-lib-table.for-github") as f:
    fpLibTable = f.readlines()

for line in fpLibTable:
    if "uri ${KIGITHUB}/" in line:
        repos.append(line.split("uri ${KIGITHUB}/")[1].split(")(options")[0])

for repo in repos:
    print("Tagging repo:", repo)
    repoUrl = "https://github.com/KiCad/" + repo + ".git"
    call(["git", "clone", repoUrl])
    chdir(repo)
    call(["git", "tag", tag])
    call(["git", "push", "--tags"])
    chdir("..")
    #call(["rm", "-rf", repo])
    #break

# Developer Support Guide

* [Git Operations of GitBack](#git-operations-of-gitback)
* [Troubleshooting](#troubleshooting)

## Git Operations of GitBack

Each operation in GitBack maps to one or more Git commands. Refer to the following table for details.

| Operation | Git Commands in Sequence |
-|-
Checkout | `clone` if URL is provided. `checkout main` and `pull` if checking out existing local repository.
New Branch | `checkout main`, a `pull main`, and finally `checkout -b <provided branch name>`. If there are existing changes already, a `stash` is performed before those commands and then a `stash pop` is attempted after those commands.
Save Snapshot | `add .` followed by a `commit -m "<provided message>"`
Publish | `push origin <branch>`


# Troubleshooting

Errors encountered during the usage of GitBack can result either a corrupted state of the local Git repository, or a bug in the Python code that composes GitBack. **Both cases will present as a Python error**. Fatal Python errors will result in a crash of the app. In any case but the last, GitBack *should* report an error to the user in yellow or red text (depending on severity) for 10 seconds.

GitBack keeps comprehensive usage and error logs each time it is used. On windows, these logs are located at `C:\Users\<username>\AppData\Local\GitBack\GitBack\logs\logs\`. **Note that `AppData` is a hidden folder, and you must first enable `View → Show → Hidden items` in file explorer before it is visible.**

In most cases, the error will likely result from the user attempting to create a branch after they had already began working, *and* the changes they are making conflict with the contents of main. **This is a merge conflict. If you are an ASEI developer, you should have received training on how to handle this.** If you have not, reach out to Carter Dugan or Pat Santucci.

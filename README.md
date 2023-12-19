# DLim_api

Can be installed using pip or built with docker

*TODO*
Installation instructions
API endpoints + explanation
CUDA (platform dependant)
CUDA (docker)
args
explanation

## Version Bumping through PR titles
My repository uses an automated versioning system that relies on the naming convention of the pull request titles. When you merge a pull request into the dev branch, the version number of the project is automatically bumped and a new tag is created, based on the prefix in your PR title.

The version number follows the MAJOR.MINOR.FIX format, where:

MAJOR version increments indicate significant changes or enhancements in the project, often including breaking changes. MINOR version increments indicate backwards-compatible new features or enhancements. FIX version increments indicate backwards-compatible bug fixes or minor changes. To specify the type of changes you have made in your pull request, prefix your PR title with one of the following:

major: - to increment the MAJOR version (e.g., from 1.0.0 to 2.0.0). minor: - to increment the MINOR version (e.g., from 0.1.0 to 0.2.0). fix: - to increment the FIX version (e.g., from 0.0.1 to 0.0.2). For example, if you have made a minor change, your PR title could be: minor: Add new feature XYZ.

If your PR title does not include any of the specified prefixes, the GitHub Action will not increment the version or create a new tag. This can be useful for non-functional changes like updates to documentation or code refactoring that don't require a version bump.

When your PR is merged into main, the GitHub Action will increment the version according to the prefix in the PR title and create a new tag.

Please ensure you follow this convention to maintain a well-structured and meaningful version history for my project.

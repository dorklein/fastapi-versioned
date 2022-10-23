#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

VERSION_RULE=${1:?"Usage: ./scripts/bumpversion.sh <version rule>"}

git fetch origin
git checkout -B main
git reset --soft origin/main
POETRY_OUTPUT=$(poetry version "$VERSION_RULE" 2>&1)
NEW_VERSION=$( perl -ne 'if (/Bumping version from \d+\.\d+\.\d+ to (\d+\.\d+\.\d+)/) { print $1 . "\n" }' <<< "$POETRY_OUTPUT" )
git commit ./pyproject.toml -m "Bumped version to $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Bumped version to $NEW_VERSION"
git push
git push --tags
gh release create "v$NEW_VERSION" --generate-notes

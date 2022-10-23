#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

VERSION_RULE=${1:?"Usage: ./scripts/bumpversion.sh <version rule>"}

git fetch origin
git checkout -B master
git reset --soft origin/master
POETRY_OUTPUT=$(poetry version "$VERSION_RULE" 2>&1)
NEW_VERSION=$( perl -ne 'if (/Bumping version from \d+\.\d+\.\d+ to (\d+\.\d+\.\d+)/) { print $1 . "\n" }' <<< "$POETRY_OUTPUT" )
git tag -a "v$NEW_VERSION" -m "Bumped version to $NEW_VERSION"
git push
git push --tags

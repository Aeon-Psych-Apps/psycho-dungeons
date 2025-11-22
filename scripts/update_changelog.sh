#!/usr/bin/env bash
set -euo pipefail

CHANGELOG="CHANGELOG.md"

# 1. Determine the last processed commit reference
if grep -q "LAST_PROCESSED" "$CHANGELOG"; then
    LAST=$(grep 'LAST_PROCESSED:' "$CHANGELOG" | sed 's/.*LAST_PROCESSED: //' | tail -1)
else
    echo "No LAST_PROCESSED marker found. Using merge-base with main"
    git fetch origin main:refs/remotes/origin/main
    LAST=$(git merge-base HEAD origin/main)
fi

echo "Using last commit: $LAST"

# 2. Gather commits newer than LAST and exclude workflow/changelog automation
COMMITS=$(git log "${LAST}..HEAD" --reverse --no-merges --pretty=format:"%H%x09%s%x09%b" \
          | grep -v -E "(Update changelog|\[skip ci\]|update_build_patch\.yml|build_patch\.yml|update_changelog\.sh)")

if [ -z "$COMMITS" ]; then
    echo "No new commits to add to changelog"
    exit 0
fi

added=""
changed=""
deprecated=""
removed=""
fixed=""
security=""
misc=""

# 3. Categorize commits
while IFS=$'\t' read -r hash subject body; do
    # lowercase for routing
    ls=$(echo "$subject" | tr '[:upper:]' '[:lower:]')
    # strip prefixes like FEATURE:, FIX:, PATCH: etc
    clean_subject=$(echo "$subject" | sed -E 's/^[a-z ]+:[ ]*//I')
    entry="- $clean_subject"

    case "$ls" in
        feature:* )      added="$added$entry"$'\n' ;;
        patch:*|changed:* ) changed="$changed$entry"$'\n' ;;
        deprecated:* )   deprecated="$deprecated$entry"$'\n' ;;
        removed:*|remove:*|delete:* ) removed="$removed$entry"$'\n' ;;
        fix:*|fixed:* )  fixed="$fixed$entry"$'\n' ;;
        security:* )     security="$security$entry"$'\n' ;;
        * )              misc="$misc$entry"$'\n' ;;
    esac

    NEW_LAST=$hash
done <<< "$COMMITS"

# 4. Ensure changelog header block exists
if ! grep -q "## \[Unreleased\]" "$CHANGELOG"; then
cat <<EOF > "$CHANGELOG.tmp"
# Changelog
All notable changes will be documented here.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
### Misc

EOF
    cat "$CHANGELOG" >> "$CHANGELOG.tmp"
    mv "$CHANGELOG.tmp" "$CHANGELOG"
fi

# 5. Insert items under correct headers
awk -v ADD="$added" \
    -v CHG="$changed" \
    -v DEP="$deprecated" \
    -v REM="$removed" \
    -v FIX="$fixed" \
    -v SEC="$security" \
    -v MSC="$misc" '
/### Added/      { print; if(ADD!="") print ADD; next }
/### Changed/    { print; if(CHG!="") print CHG; next }
/### Deprecated/ { print; if(DEP!="") print DEP; next }
/### Removed/    { print; if(REM!="") print REM; next }
/### Fixed/      { print; if(FIX!="") print FIX; next }
/### Security/   { print; if(SEC!="") print SEC; next }
/### Misc/       { print; if(MSC!="") print MSC; next }
{print}
' "$CHANGELOG" > "$CHANGELOG.new"

mv "$CHANGELOG.new" "$CHANGELOG"

# 6. Remove previous marker and append the new one
sed -i '/LAST_PROCESSED/d' "$CHANGELOG"
echo "<!-- LAST_PROCESSED: $NEW_LAST -->" >> "$CHANGELOG"
echo "Changelog updated through commit $NEW_LAST"

#!/usr/bin/env bash
set -euo pipefail

CHANGELOG="CHANGELOG.md"

echo "[DEBUG] Starting changelog update"

# 1. Determine last processed commit
if grep -q "LAST_PROCESSED" "$CHANGELOG"; then
    LAST=$(grep -oP '(?<=LAST_PROCESSED: )[0-9a-f]+' "$CHANGELOG" | tail -1)
else
    echo "[DEBUG] No LAST_PROCESSED marker. Using merge-base"
    git fetch origin main:refs/remotes/origin/main
    LAST=$(git merge-base HEAD origin/main)
fi

echo "[DEBUG] Using last commit: $LAST"

# 2. Gather commits newer than LAST
# Exclude automation commits:
#  - commits modifying workflow files (.yml)
#  - anything containing [skip ci]
#  - commits tagged "internal"
#  - commits mentioning changelog automation
RAW_COMMITS=$(
    git log "${LAST}..HEAD" \
        --reverse \
        --no-merges \
        --pretty=format:"%H%x09%s%x09%b" |
        grep -v -Ei "(update changelog|\[skip ci\]|\.yml|internal)"
)

if [ -z "$RAW_COMMITS" ]; then
    echo "[INFO] No new commits to add"
    exit 0
fi

echo "[DEBUG] Found commits:"
echo "$RAW_COMMITS" | sed 's/^/  - /'

added=""
changed=""
deprecated=""
removed=""
fixed=""
security=""
misc=""

# 3. Categorize commits
while IFS=$'\t' read -r hash subject body; do
    ls=$(echo "$subject" | tr '[:upper:]' '[:lower:]')

    # remove semantic prefix e.g. "fix:" or "feature:"
    clean_subject=$(echo "$subject" | sed -E 's/^[a-z ]+:[ ]*//I')

    # include body if present
    formatted="- $clean_subject"
    if [ -n "$body" ]; then
        formatted="$formatted"$'\n'"  $(echo "$body" | sed 's/^/  /')"
    fi

    case "$ls" in
        feature:* )
            added="$added$formatted"$'\n'
            ;;
        patch:*|change:*|changed:* )
            changed="$changed$formatted"$'\n'
            ;;
        deprecated:* )
            deprecated="$deprecated$formatted"$'\n'
            ;;
        remove:*|removed:*|delete:*|deleted:* )
            removed="$removed$formatted"$'\n'
            ;;
        fix:*|fixed:* )
            fixed="$fixed$formatted"$'\n'
            ;;
        security:* )
            security="$security$formatted"$'\n'
            ;;
        * )
            misc="$misc$formatted"$'\n'
            ;;
    esac

    NEW_LAST=$hash
done <<< "$RAW_COMMITS"

# 4. Ensure header exists
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

# 5. Inject categorized items
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

# 6. Replace LAST_PROCESSED marker
sed -i '/LAST_PROCESSED/d' "$CHANGELOG"
echo "<!-- LAST_PROCESSED: $NEW_LAST -->" >> "$CHANGELOG"

echo "[INFO] Changelog updated through commit $NEW_LAST"

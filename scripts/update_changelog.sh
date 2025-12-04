#!/usr/bin/env bash
set -euo pipefail

OUTPUT_FILE="automated_changelog.md"
echo "[DEBUG] Starting automated changelog"

# 1. Determine last processed commit
#if grep -q "LAST_PROCESSED" "$OUTPUT_FILE" 2>/dev/null; then
#    LAST=$(grep -oP '(?<=LAST_PROCESSED: )[0-9a-f]+' "$OUTPUT_FILE" | tail -1)
#else
#    echo "[DEBUG] No LAST_PROCESSED found, using merge-base with main"
#    git fetch origin main:refs/remotes/origin/main
#    LAST=$(git merge-base HEAD origin/main)
#fi
#echo "[DEBUG] Using last commit: $LAST"

git fetch origin main:refs/remotes/origin/main
LAST=$(git merge-base HEAD origin/main)

echo "[DEBUG] Using starting commit (merge-base with main): $LAST"

# 2. Gather commits newer than LAST
COMMITS=$(git log "${LAST}..HEAD" --reverse --no-merges --pretty=format:"%H%x09%s%x09%b")
if [ -z "$COMMITS" ]; then
    echo "[INFO] No new commits to add"
    exit 0
fi

# 3. Initialize categories
added="" changed="" deprecated="" removed="" fixed="" security="" misc=""

NEW_LAST=""
# 4. Categorize commits
while IFS=$'\t' read -r hash subject body; do
    if [[ "$subject" =~ [Ii]nternal ]] || [[ "$subject" =~ \[skip\ ci\] ]]; then
        echo "[DEBUG] Skipping commit $hash: $subject"
        continue
    fi

    ls=$(echo "$subject" | tr '[:upper:]' '[:lower:]')
    clean_subject=$(echo "$subject" | sed -E 's/^[a-z ]+:[ ]*//I')

    entry="- $clean_subject"
    if [ -n "$body" ]; then
        entry="$entry"$'\n'"  $(echo "$body" | sed '/^\s*$/d; s/^/  /')"
    fi

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

if [ -z "$NEW_LAST" ]; then
    echo "[INFO] Only internal or automation commits found. Nothing to do."
    exit 0
fi

# 5. Ensure file exists with header
cat <<EOF > "$OUTPUT_FILE"
# Changelog (Automated per working version based off filtered commit messages)
This file contains automatically generated commit history.

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
### Misc

EOF
#    cat "$OUTPUT_FILE" >> "$OUTPUT_FILE.tmp" 2>/dev/null || true
#    mv "$OUTPUT_FILE.tmp" "$OUTPUT_FILE"
#fi

# 6. Insert categorized commits under headers
awk -v ADD="$added" -v CHG="$changed" -v DEP="$deprecated" -v REM="$removed" -v FIX="$fixed" -v SEC="$security" -v MSC="$misc" '
/### Added/      { print; if(ADD!="") print ADD; next }
/### Changed/    { print; if(CHG!="") print CHG; next }
/### Deprecated/ { print; if(DEP!="") print DEP; next }
/### Removed/    { print; if(REM!="") print REM; next }
/### Fixed/      { print; if(FIX!="") print FIX; next }
/### Security/   { print; if(SEC!="") print SEC; next }
/### Misc/       { print; if(MSC!="") print MSC; next }
{print}
' "$OUTPUT_FILE" > "$OUTPUT_FILE.new"

mv "$OUTPUT_FILE.new" "$OUTPUT_FILE"

# 7. Update LAST_PROCESSED marker
#sed -i '/LAST_PROCESSED/d' "$OUTPUT_FILE"
#echo "<!-- LAST_PROCESSED: $NEW_LAST -->" >> "$OUTPUT_FILE"

echo "[INFO] automated_changelog.md updated through commit $NEW_LAST"

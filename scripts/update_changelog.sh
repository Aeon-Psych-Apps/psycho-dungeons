#!/usr/bin/env bash
set -euo pipefail

CHANGELOG="CHANGELOG.md"

echo "[DEBUG] Starting changelog update"

# 1. Find last processed commit
if grep -q "LAST_PROCESSED" "$CHANGELOG"; then
  LAST=$(grep 'LAST_PROCESSED:' "$CHANGELOG" \
    | sed 's/.*LAST_PROCESSED: \([0-9a-f]*\).*/\1/' \
    | tail -1)
else
  echo "[DEBUG] No LAST_PROCESSED marker found. Using merge-base"
  git fetch origin main:refs/remotes/origin/main
  LAST=$(git merge-base HEAD origin/main)
fi

echo "[DEBUG] Using last commit: $LAST"

# Ensure LAST commit exists
if ! git cat-file -e "$LAST"^{commit} 2>/dev/null; then
  echo "[WARN] LAST commit missing locally. Fetching deeper history..."
  git fetch --unshallow || git fetch --all
fi

# 2. Extract commits newer than LAST including subject and body
# Use a unique delimiter so bodies are preserved safely
RAW_COMMITS=$(git log "${LAST}..HEAD" --reverse --no-merges \
    --pretty=format:"===COMMIT_START===%nHASH:%H%nSUBJECT:%s%nBODY:%b%n===COMMIT_END===" \
    || true)

if [ -z "$RAW_COMMITS" ]; then
  echo "[INFO] No commits found"
  exit 0
fi

# 3. Categorize + format
added=""
changed=""
deprecated=""
removed=""
fixed=""
security=""
misc=""
NEW_LAST="$LAST"

# Convert into individual commit blocks
echo "$RAW_COMMITS" | awk '
/===COMMIT_START===/ { capture=1; block=""; next }
capture==1          { block=block $0 ORS }
/===COMMIT_END===/  {
  print block;
  capture=0;
}
' | while read -r block; do

  hash=$(echo "$block" | grep "^HASH:" | sed 's/HASH://')
  subject=$(echo "$block" | grep "^SUBJECT:" | sed 's/SUBJECT://')
  body=$(echo "$block" | sed -n '/^BODY:/,$p' | sed 's/^BODY://')

  # skip automation and internal commits
  lsubject=$(echo "$subject" | tr '[:upper:]' '[:lower:]')
  if echo "$lsubject" | grep -Eq '(update changelog|\[skip ci\]|internal:)'; then
    continue
  fi

  # strip known prefixes for printed output
  clean_subject=$(echo "$subject" \
      | sed -E 's/^[a-z ]+:[ ]*//I')

  # multi-line bullet formatting
  entry="- $clean_subject"
  if [ -n "$body" ]; then
    entry="$entry"$'\n'"$(echo "$body" | sed 's/^/  /')"
  fi
  entry="$entry"$'\n'

  # categorize
  case "$lsubject" in
    feature:* )
      added="$added$entry"
      ;;
    changed:*|patch:* )
      changed="$changed$entry"
      ;;
    deprecated:* )
      deprecated="$deprecated$entry"
      ;;
    removed:*|delete:*|remove:* )
      removed="$removed$entry"
      ;;
    fix:*|fixed:* )
      fixed="$fixed$entry"
      ;;
    security:* )
      security="$security$entry"
      ;;
    * )
      misc="$misc$entry"
      ;;
  esac

  NEW_LAST="$hash"
done

# If nothing added anywhere
if [ -z "$added$changed$deprecated$removed$fixed$security$misc" ]; then
  echo "[INFO] No new changes for changelog"
  exit 0
fi

# 4. Ensure changelog has expected sections
if ! grep -q "## \[Unreleased\]" "$CHANGELOG"; then
cat <<EOF > "$CHANGELOG.tmp"
# Changelog

This project follows Keep a Changelog formatting.

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

# 5. Insert each category
awk \
  -v ADD="$added" \
  -v CHG="$changed" \
  -v DEP="$deprecated" \
  -v REM="$removed" \
  -v FIX="$fixed" \
  -v SEC="$security" \
  -v MSC="$misc" '
/### Added/      { print; if (ADD!="") print ADD; next }
/### Changed/    { print; if (CHG!="") print CHG; next }
/### Deprecated/ { print; if (DEP!="") print DEP; next }
/### Removed/    { print; if (REM!="") print REM; next }
/### Fixed/      { print; if (FIX!="") print FIX; next }
/### Security/   { print; if (SEC!="") print SEC; next }
/### Misc/       { print; if (MSC!="") print MSC; next }
{print}
' "$CHANGELOG" > "$CHANGELOG.new"

mv "$CHANGELOG.new" "$CHANGELOG"

# 6. Shift LAST_PROCESSED marker
sed -i '/LAST_PROCESSED/d' "$CHANGELOG"
echo "<!-- LAST_PROCESSED: $NEW_LAST -->" >> "$CHANGELOG"

echo "[INFO] Changelog updated through commit $NEW_LAST"

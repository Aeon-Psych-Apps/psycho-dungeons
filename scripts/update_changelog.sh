#!/usr/bin/env bash
set -euo pipefail

# Make sure main exists locally
git fetch origin main --depth=1 || true

# If main does not exist (first run), use the first commit as base
if git rev-parse origin/main >/dev/null 2>&1; then
    BASE=$(git merge-base HEAD origin/main)
else
    BASE=$(git rev-list --max-parents=0 HEAD)
fi

echo "Using base commit: $BASE"

# Extract commit history since base and categorize
git log ${BASE}..HEAD --no-merges --pretty=format:"%s%x09%b" | awk '
BEGIN { 
  FS="\t"
  added=""; changed=""; deprecated=""; removed=""; fixed=""; security=""; misc=""
}
{
  subject=$1
  body=""
  if (NF>1){
    for(i=2;i<=NF;i++){
      if($i!="") body=body"    - "$i"\n"
    }
  }
  lc=tolower(subject)

  # Ignore internal entries
  if(lc ~ /^internal:/ || lc ~ /\[skip ci\]/) next

  # Strip prefixes if present (handles FEATURE:test and FEATURE: test)
  sub(/^[a-z ]+:[ ]*/i, "", subject)

  # Categorize
  category=""
  if(lc ~ /^feature:/){category="added"}
  else if(lc ~ /^patch:/ || lc ~ /^changed:/){category="changed"}
  else if(lc ~ /^deprecated:/){category="deprecated"}
  else if(lc ~ /^(remove|removed|delete):/){category="removed"}
  else if(lc ~ /^fix:/ || lc ~ /^fixed:/){category="fixed"}
  else if(lc ~ /^security:/){category="security"}
  else {category="misc"}

  entry="- " subject "\n" body

  if(category=="added"){added=added entry "\n"}
  else if(category=="changed"){changed=changed entry "\n"}
  else if(category=="deprecated"){deprecated=deprecated entry "\n"}
  else if(category=="removed"){removed=removed entry "\n"}
  else if(category=="fixed"){fixed=fixed entry "\n"}
  else if(category=="security"){security=security entry "\n"}
  else {misc=misc entry "\n"}
}
END {
  print added > "/tmp/added.txt"
  print changed > "/tmp/changed.txt"
  print deprecated > "/tmp/deprecated.txt"
  print removed > "/tmp/removed.txt"
  print fixed > "/tmp/fixed.txt"
  print security > "/tmp/security.txt"
  print misc > "/tmp/misc.txt"
}'
 
# Ensure Unreleased header exists
if ! grep -q "## \\[Unreleased\\]" CHANGELOG.md; then
cat <<EOF > CHANGELOG.tmp
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
  cat CHANGELOG.md >> CHANGELOG.tmp
  mv CHANGELOG.tmp CHANGELOG.md
fi

# Insert new entries into headings
awk '
/## \[Unreleased\]/ {print; next}
/### Added/ {print; system("cat /tmp/added.txt"); next}
/### Changed/ {print; system("cat /tmp/changed.txt"); next}
/### Deprecated/ {print; system("cat /tmp/deprecated.txt"); next}
/### Removed/ {print; system("cat /tmp/removed.txt"); next}
/### Fixed/ {print; system("cat /tmp/fixed.txt"); next}
/### Security/ {print; system("cat /tmp/security.txt"); next}
/### Misc/ {print; system("cat /tmp/misc.txt"); next}
{print}
' CHANGELOG.md > CHANGELOG.new

mv CHANGELOG.new CHANGELOG.md
rm -f /tmp/*.txt

echo "Changelog updated"

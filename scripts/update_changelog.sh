#!/usr/bin/env bash
set -euo pipefail

# Ensure on test branch
if [ "$(git rev-parse --abbrev-ref HEAD)" != "test" ]; then
  echo "Not on test branch. Exiting."
  exit 0
fi

# Find base commit
BASE=$(git merge-base HEAD origin/main)

# Generate categorized changelog entries
LOG=$(git log ${BASE}..HEAD --no-merges --pretty=format:"%s%x09%b" | awk '
BEGIN { FS="\t"; OFS="\n"; added=""; changed=""; deprecated=""; removed=""; fixed=""; security=""; misc="" }
{
  subject=$1
  body=""
  if(NF>1){for(i=2;i<=NF;i++){if($i!="") body=body"    - "$i"\n"}}
  lc=tolower(subject)
  if(lc ~ /^internal:/) next
  if(lc ~ /\[skip ci\]/) next
  entry="- " subject "\n" body
  if(lc ~ /^feature:/){added=added entry "\n"}
  else if(lc ~ /^fix:/){fixed=fixed entry "\n"}
  else if(lc ~ /^patch:/){changed=changed entry "\n"}
  else if(lc ~ /^deprecated:/){deprecated=deprecated entry "\n"}
  else if(lc ~ /^(remove|removed|delete):/){removed=removed entry "\n"}
  else if(lc ~ /^security:/){security=security entry "\n"}
  else {misc=misc entry "\n"}
}
END {
  # Print each section’s entries separately
  print added > "/tmp/added.txt"
  print changed > "/tmp/changed.txt"
  print deprecated > "/tmp/deprecated.txt"
  print removed > "/tmp/removed.txt"
  print fixed > "/tmp/fixed.txt"
  print security > "/tmp/security.txt"
  print misc > "/tmp/misc.txt"
}')

# Create CHANGELOG template if missing
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

# Insert entries under each section
awk '
/## \[Unreleased\]/ {unrel=1; print; next}
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

# Cleanup
rm -f /tmp/*.txt

echo "Changelog updated successfully"

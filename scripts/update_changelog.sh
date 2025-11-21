#!/usr/bin/env bash
set -euo pipefail

# Ensure on test branch
if [ "$(git rev-parse --abbrev-ref HEAD)" != "test" ]; then
  echo "Not on test branch. Exiting."
  exit 0
fi

# Find base commit
BASE=$(git merge-base HEAD origin/main)

# Generate categorized changelog
LOG=$(git log ${BASE}..HEAD --no-merges --pretty=format:"%s%x09%b" | awk '
BEGIN {RS="\n"; FS="\t"; ORS=""; added=""; changed=""; deprecated=""; removed=""; fixed=""; security=""; misc=""}
{
  subject=$1
  body=""
  if(NF>1){for(i=2;i<=NF;i++){if($i!="") body=body"    - "$i"\n"}}
  lc=tolower(subject)
  if(lc ~ /^internal:/) next
  if(lc ~ /\[skip ci\]/) next
  entry="- " subject "\n" body
  if(lc ~ /^feature:/){sub(/^feature:[ ]*/i,"",entry); added=added entry "\n"}
  else if(lc ~ /^fix:/){sub(/^fix:[ ]*/i,"",entry); fixed=fixed entry "\n"}
  else if(lc ~ /^patch:/){sub(/^patch:[ ]*/i,"",entry); changed=changed entry "\n"}
  else if(lc ~ /^deprecated:/){sub(/^deprecated:[ ]*/i,"",entry); deprecated=deprecated entry "\n"}
  else if(lc ~ /^(remove|removed|delete):/){sub(/^(remove|removed|delete):[ ]*/i,"",entry); removed=removed entry "\n"}
  else if(lc ~ /^security:/){sub(/^security:[ ]*/i,"",entry); security=security entry "\n"}
  else {misc=misc entry "\n"}
}
END {
  print "### Added\n" added "\n"
  print "### Changed\n" changed "\n"
  print "### Deprecated\n" deprecated "\n"
  print "### Removed\n" removed "\n"
  print "### Fixed\n" fixed "\n"
  print "### Security\n" security "\n"
  print "### Misc\n" misc "\n"
}')

# Create CHANGELOG if not exists
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

# Insert log under Unreleased
awk -v new="$LOG" '
BEGIN {in_unrel=0}
/## \[Unreleased\]/ {print; in_unrel=1; next}
in_unrel && /^### / {print new; in_unrel=0}
{print}
' CHANGELOG.md > CHANGELOG.new

mv CHANGELOG.new CHANGELOG.md
echo "Changelog updated"

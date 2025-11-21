#!/usr/bin/env bash
set -euo pipefail

# Ensure we are on the test branch
if [ "$(git rev-parse --abbrev-ref HEAD)" != "test" ]; then
  echo "Not on test branch. Exiting."
  exit 0
fi

# Get the common base with main (make sure origin/main exists)
git fetch origin main --depth=1
BASE=$(git merge-base HEAD origin/main)

# Generate categorized changelog entries without headings
git log ${BASE}..HEAD --no-merges --pretty=format:"%s%x09%b" | awk '
BEGIN { FS="\t"; added=""; changed=""; deprecated=""; removed=""; fixed=""; security=""; misc="" }
{
  subject=$1; body=""
  if(NF>1){for(i=2;i<=NF;i++){if($i!="") body=body"    - "$i"\n"}}
  lc=tolower(subject)
  if(lc ~ /^internal:/ || lc ~ /\[skip ci\]/) next

  # Determine category and strip prefix
  entry_text = subject
  category=""
  if(lc ~ /^feature:/){category="added"; sub(/^feature:[ ]*/i,"",entry_text)}
  else if(lc ~ /^fix:/ || lc ~ /^fixed:/){category="fixed"; sub(/^(fix|fixed):[ ]*/i,"",entry_text)}
  else if(lc ~ /^patch:/ || lc ~ /^changed:/){category="changed"; sub(/^(patch|changed):[ ]*/i,"",entry_text)}
  else if(lc ~ /^deprecated:/){category="deprecated"; sub(/^deprecated:[ ]*/i,"",entry_text)}
  else if(lc ~ /^(remove|removed|delete):/){category="removed"; sub(/^(remove|removed|delete):[ ]*/i,"",entry_text)}
  else if(lc ~ /^security:/){category="security"; sub(/^security:[ ]*/i,"",entry_text)}
  else {category="misc"}

  # Format entry
  entry="- " entry_text "\n" body

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

# Insert entries under the correct sections
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

# Cleanup temporary files
rm -f /tmp/*.txt

echo "Changelog updated successfully"

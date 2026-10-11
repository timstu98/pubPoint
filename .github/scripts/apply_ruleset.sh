#!/bin/bash

set -euo pipefail

repository="${GH_REPOSITORY:-timstu98/pubPoint}"
ruleset_id="$(gh api "repos/${repository}/rulesets" --jq '.[] | select(.name == "Main") | .id' | head -n 1)"

if [[ -z "$ruleset_id" ]]; then
  printf 'Main ruleset not found for %s\n' "$repository" >&2
  exit 1
fi

gh api \
  --method PUT \
  "repos/${repository}/rulesets/${ruleset_id}" \
  --input .github/rulesets/main.json \
  --silent

#!/bin/bash

set -euo pipefail

repository="${GH_REPOSITORY:-timstu98/pubPoint}"

gh api \
  --method PATCH \
  "repos/${repository}" \
  --input .github/settings/repository.json \
  --silent

./bash_scripts/apply_main_ruleset.sh

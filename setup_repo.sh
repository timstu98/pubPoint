#!/usr/bin/env bash
set -e

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
git -C "$repo_root" config --local core.hooksPath .githooks

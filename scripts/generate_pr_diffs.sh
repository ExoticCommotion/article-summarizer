#!/bin/bash

# This script uses only POSIX tools — no jq required.

OUTDIR="outputs"
mkdir -p "$OUTDIR"

STAMP=$(date -u +"%Y%m%dT%H%M%SZ")

# Check for GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI 'gh' is not installed. Install from https://cli.github.com/"
    exit 1
fi

echo "📡 Fetching open pull requests from GitHub..."

# Get PRs as plain text: one per line like "123   devin/1747-title"
PR_LIST=$(gh pr list --state open --json number,headRefName \
  --template '{{range .}}{{.number}}{{"\t"}}{{.headRefName}}{{"\n"}}{{end}}')

if [ -z "$PR_LIST" ]; then
    echo "⚠️  No open PRs found."
    exit 0
fi

echo "🔍 Found open PRs:"
echo "$PR_LIST" | sed 's/^/   • /'

while IFS=$'\t' read -r PR_NUM HEAD_BRANCH; do
    SAFE_NAME=$(echo "$HEAD_BRANCH" | tr '/' '-')
    FILE="$OUTDIR/${SAFE_NAME}-${STAMP}.patch"

    echo "📦 Fetching and diffing $HEAD_BRANCH → $FILE"

    git fetch origin "$HEAD_BRANCH"

    BASE=$(git merge-base origin/main origin/"$HEAD_BRANCH")
    if [ -z "$BASE" ]; then
        echo "⚠️  Skipping $HEAD_BRANCH — no merge-base with origin/main"
        continue
    fi

    git diff "$BASE"...origin/"$HEAD_BRANCH" > "$FILE"
    echo "✅  Wrote diff to $FILE"

done <<< "$PR_LIST"

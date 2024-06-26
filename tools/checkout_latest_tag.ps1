git -C "$PSScriptRoot" checkout main
git -C "$PSScriptRoot" pull
$latest_tag = git -C "$PSScriptRoot" describe --tags --abbrev=0

git -C "$PSScriptRoot" checkout "$latest_tag"
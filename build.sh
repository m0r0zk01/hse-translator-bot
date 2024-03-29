#!/bin/bash

echo "[INFO] Starting build...\n"

docker compose build --build-arg YA_OAUTH_TOKEN="$YA_OAUTH_TOKEN" --build-arg FOLDER_ID="$FOLDER_ID" --build-arg TG_BOT_TOKEN="$TG_BOT_TOKEN"

echo "[INFO] Build done!\n"

if [[ "$1" = "run" ]]; then
    echo "[INFO] Starting...\n"
    docker compose up
fi

echo "[INFO] Exiting...\n"

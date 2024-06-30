#!/bin/bash

# Function to update pacman.conf
update_pacman_conf() {
    local repo_name=$1
    local server_url=$2

    echo -e "\n[${repo_name}]\nServer = ${server_url}" | sudo tee -a /etc/pacman.conf
}

# Function to handle GPG keys
handle_gpg_keys() {
    local key_id=$1

    sudo pacman-key --recv-keys "${key_id}"
    sudo pacman-key --lsign-key "${key_id}"
}

# Fetch the repository information using the Python script
REPOS=$(scrape_arch_repos.py)

# Loop through the fetched repositories and update pacman.conf and handle GPG keys
IFS=$'\n'
for repo in $REPOS; do
    IFS=',' read -r name server key <<< "$repo"
    update_pacman_conf "$name" "$server"
    handle_gpg_keys "$key"
done

echo "Repositories and keys have been updated successfully."

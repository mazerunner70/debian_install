#!/bin/bash

echo "Creating Moinmoin docker image and upload to repo"

# Confirm we can process command line options
# Taken from http://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash

getopt --test > /dev/null
if [[ $? -ne 4 ]]; then
    echo "I’m sorry, `getopt --test` failed in this environment."
    exit 1
fi

# Allowed params:
# -u | --username  docker username (id)
# -p | --password  docker login password
# -t | --tag       tag for docker image
# -r | --repo      destination repository

SHORT=u:p:t:v:r::
LONG=username:password:tag:version:repo::

# -temporarily store output to be able to check for errors
# -activate advanced mode getopt quoting e.g. via “--options”
# -pass arguments only via   -- "$@"   to separate them correctly
PARSED=$(getopt --options $SHORT --longoptions $LONG --name "$0" -- "$@")
if [[ $? -ne 0 ]]; then
    # e.g. $? == 1
    #  then getopt has complained about wrong arguments to stdout
    exit 2
fi

# use eval with "$PARSED" to properly handle the quoting
eval set -- "$PARSED"

while true; do
    case "$1" in
        -u|--username)
            username="$2"
            shift 2
            ;;
        -p|--password)
            password="$2"
            shift 2
            ;;
        -t|--tag)
            tag="$2"
            shift 2
            ;;
        -v|--version)
            version="$2"
            shift 2
            ;;
        -r|--repo)
            repo="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
done

echo "Building latest moinmoin to $username/$tag:$version"

echo 

echo "testing if image is in repo already"
# Using idea from -u 

function docker_tag_exists() {
    TOKEN=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username": "'${username}'", "password": "'${password}'"}' https://hub.docker.com/v2/users/login/ | ./TokenFilter.py)
    echo $TOKEN
    EXISTS=$(curl -s -H "Authorization: JWT ${TOKEN}" https://hub.docker.com/v2/repositories/${username}/tags/?page_size=10000)
    echo $EXISTS
    test $EXISTS = true
}

if docker_tag_exists; then
    echo exist
else 
    echo not exists
fi



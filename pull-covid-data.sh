#!/usr/bin/env bash

repo_url=https://github.com/pcm-dpc/COVID-19

if [ ! -d "COVID-19" ]; then
    git clone $repo_url
fi

cd COVID-19 && git pull --rebase origin master
res=$?
cd ..
if [ 0 -ne $res ]; then
   rm -rf COVID-19
   git clone $repo_url
fi
date -Is > update_timestamp.txt

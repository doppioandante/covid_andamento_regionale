#!/usr/bin/env bash

if [ ! -d "COVID-19" ]; then
    git clone https://github.com/pcm-dpc/COVID-19
fi

cd COVID-19 && git pull --rebase origin master
cd ..
date -Is > update_timestamp.txt

#!/usr/bin/bash

for segundo in $(seq 1 5); do
    for n in $(seq 1 10); do
        python3 client/client.py example.md 2>&1 | sed "s/^/[${segundo}, ${n}] /" &
    done
    sleep 1
done

wait

#!/bin/bash
export file_name=$1
export curr=$(dirname "$0")
python3 "$curr"/upload.py
#!/usr/bin/env bash

DIR="$(cd "$(dirname "$0")" && pwd)"

cd $DIR && . ../bin/activate && python run.py

#!/bin/bash

set -e

sleep 10

export DEBIAN_FRONTEND=noninteractive

sudo apt-get autoremove

sudo apt-get update

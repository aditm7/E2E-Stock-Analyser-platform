#!/bin/bash

if [ -f ./database/database.db ]; then
  rm ./database/database.db
fi

if [ -d ./database/migrations ]; then
  rm -r ./database/migrations
fi
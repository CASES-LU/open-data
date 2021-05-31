#! /usr/bin/env bash


git pull origin master --tags
npm install
poetry install
poetry run pybabel compile -d opendata/translations
poetry run flask db upgrade
sudo systemctl restart opendata.service

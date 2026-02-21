#!/bin/bash

celery -A celery_app worker -B --loglevel INFO

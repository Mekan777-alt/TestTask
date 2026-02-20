FROM ubuntu:latest
LABEL authors="mekanmededov"

ENTRYPOINT ["top", "-b"]
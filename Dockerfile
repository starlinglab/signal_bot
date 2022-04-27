FROM debian:latest

ARG HOST_UID=1337
ARG HOST_GID=1337

RUN apt -y update;\
    apt -y install python3 python3-pip ; \
    mkdir store
RUN pip3 install semaphore-bot requests
COPY proofmodebot.py /proofmodebot.py

ENTRYPOINT ["/usr/bin/python3","/proofmodebot.py"]

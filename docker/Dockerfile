FROM python:3.12-slim AS paper-toaster-base

WORKDIR /app
RUN apt-get update -y &&\
    apt-get install -y ghostscript

RUN adduser --disabled-password --gecos "Toastmaster" --uid 1000 toastmaster

WORKDIR /app
RUN mkdir /output &&\
    chown -R toastmaster:toastmaster /output
USER toastmaster

CMD ["bash"]

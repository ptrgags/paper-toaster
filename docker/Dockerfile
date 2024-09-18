# Python container for running the main script and generating postscript -------
FROM python:3.12-slim AS paper-toaster

WORKDIR /app
RUN apt-get update -y &&\
    apt-get install -y ghostscript

RUN adduser \
    --disabled-password \
    --gecos "The master of toast" \
    --uid 1000 toastmaster

WORKDIR /app
RUN mkdir /output &&\
    chown -R toastmaster:toastmaster /output
USER toastmaster

CMD ["bash"]

# Linux container with GhostScript for converting PostScript to PDF/PNG --------
FROM alpine:3.20 AS post-toast-ghost

WORKDIR /scripts
RUN adduser \
    --disabled-password \
    --gecos "A ghost in the machine" \
    --uid 1000 ghostmaster

RUN apk add --no-cache ghostscript

USER ghostmaster

COPY post-processing /scripts
ENTRYPOINT ["sh", "./convert_receipt.sh"]

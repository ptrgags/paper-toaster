# Python container for running the main script and generating postscript -------
FROM python:3.12.6-slim AS paper-toaster
WORKDIR /app
ENV WORK_DIR=/workdir

RUN adduser \
    --disabled-password \
    --gecos "The master of toast" \
    --uid 1000 toastmaster
USER toastmaster

ENTRYPOINT ["python", "-m", "papertoaster"]
COPY src /app

# Linux container with GhostScript for converting PostScript to PDF/PNG --------
FROM alpine:3.20.3 AS post-toast-ghost

WORKDIR /scripts

RUN adduser \
    --disabled-password \
    --gecos "A ghost in the machine" \
    --uid 1000 ghostmaster

RUN apk add --no-cache ghostscript
USER ghostmaster

ENTRYPOINT ["sh", "./convert_receipt.sh"]
COPY post-processing /scripts


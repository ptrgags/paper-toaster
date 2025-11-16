#!/bin/sh
# For use in the Docker container (post-toast-ghost)

# Get the filename minus extension and any leading path
ID=$(basename "$1" .ps)

if [ -z "$ID" ]
then
    echo "usage: ./convert_receipt.sh <filename>"
    exit 1
fi

INPUT_FILE=$WORK_DIR/$ID.ps

if [ ! -f "$INPUT_FILE" ]
then
    echo "Could not find input file $INPUT_FILE"
    exit 1
fi

# Generate a PDF file, this is what I print
PDF_FILE=$WORK_DIR/$ID.pdf
echo "Generating PDF file $PDF_FILE"
ps2pdf $INPUT_FILE $PDF_FILE

# Generate a 100 DPI image, I use this for thumbnails in the README as well
# as my website.
THUMBNAIL_FILE=$WORK_DIR/${ID}_thumbnail.png
echo "Generating thumbnail image $THUMBNAIL_FILE"
gs -o $THUMBNAIL_FILE -sDEVICE=png16m -r100 $INPUT_FILE

# Generate a 200 DPI image, I use these for featuring artworks on my website
WEB_FILE=$WORK_DIR/${ID}_web.png
echo "Generating image $WEB_FILE"
gs -o $WEB_FILE -sDEVICE=png16m -r200 $INPUT_FILE

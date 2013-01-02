#!/bin/bash

PDF_PATH="$HOME/Dropbox/git/data/pdf"
POST_PATH="$HOME/Dropbox/git/hrwgc.github.com/_posts"

ls -1 $POST_PATH | while read FILE; do
    UUID=$(cat "$POST_PATH/$FILE" | sed -nE 's/^uid: (.*)$/\1/p' | tr -d '\"');	
	PDF_SUBSTRING=$(cat "$POST_PATH/$FILE" | sed -nE 's/^local_pdf: \"([^\"]+)\"/\1/p' | sed -nE 's_^\.\./\.\./hrwgc-pdf/data/[^\-]+\-[^\-]+\-[^\-]+\-[^\-]+\-[^\-]+\-(.*)$_\1_p')
	PREV_FILE="${PDF_PATH}/*${PDF_SUBSTRING}"
	NEW_FILE="$PDF_PATH/$UUID-$PDF_SUBSTRING"
	if [ -n "$PDF_SUBSTRING" ]; then
		if [ -f `ls ${PDF_PATH}/*${PDF_SUBSTRING}` ]; then
			 mv ${PDF_PATH}/*${PDF_SUBSTRING} "$NEW_FILE"
             echo "$FILE ==> $PDF_SUBSTRING"
		fi
	fi
	echo "----------------"
done
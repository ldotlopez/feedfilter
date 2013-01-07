#!/bin/bash

FEEDFILTER="$HOME/local/feedfilter/feedfilter.py"
if [ ! -x "$FEEDFILTER" ]; then
	echo "feedfilter.py not found" >&2
	exit 1
fi

T="$(mktemp)"
wget -qq -O - http://www.meneame.net/rss2.php | "$FEEDFILTER" -o "$T"
if [ $? -eq 0 ]; then
	mv "$T" "$HOME/public_html/feeds/meneame.rss" && chmod 644 "$HOME/public_html/feeds/meneame.rss"
	exit 0
else
	rm "$T"
	exit 1
fi

# Document Event Extraction for Google Calendar Integration

Currently looking to get complete support for syllabuses first before I tackle other types of documents (work schedules, game schedules, etc.)

## Contributors
* Alberto Mejia '20

## Setup

To install the dependencies found in requirements.txt, run the following command in your terminal:

`pip3 install -r requirements.txt to install`

Now run the following commands:
<pre>
	python3 -m spacy download en_core_web_sm
</pre>

<pre>
	sudo pip3 install --upgrade google-api-python-client
</pre>

In order to get credentials for your Google Calendar, run the following
<pre>
	python3 google.py
</pre>

And now run python3 main.py to get the website running.
<pre>
	python3 main.py
</pre>

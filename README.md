## Vocabulary Learner

Python script which uses Google's text to speech to teach vocabulary incorporating audio

#### How to use
* Install requirements
  * `pip install -r requirements.txt`
  * `bower install`
* Run
  * `python app.py`
* Point your browser (works best on Chrome or Safari) to 0.0.0.0:5000

#### Details

When prompted choose a user name (this names the file where your work is stored in user_name.pdeck)

Upload a unicode csv with the words you want to learn in the first column and their meanings in the right column (no headers).
The easiest way to make this csv is using Google Sheets. You can upload a list of the words you want to learn.
Then use the GoogleTranslate command to get simple translations. Many of these will probably be a little off but you can 
fix them as you go along.

When you notice mistakes in the data you can edit the words in the program. This won't effect anything.

You can click on the progress tab to see how you are doing.

Words are selected for review using the pimsleur method. Whenever you get a word wrong it is reviewed imediately after looking at one other word.

You can edit the language that words are read in and how many new words can be introduced in an hour in the change settings tab.
Words are only added if you are upto date on reviewing words you already learned.

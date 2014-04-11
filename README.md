#TweetPyMax

##Max Patch which takes a list of hashtags and a bang, outputs total occurrences 
of each hashtag since last bang

##Use

- put tweetpymax.maxpat somewhere Max can find it
- make sure that you have the Python twitter library installed. If it's not, run:
`sudo pip install twitter`
- navigate to this directory on command line
- start Python script by typing ./run.py in the command line 
- insert tweetpymax patcher in Max set

- tweetpymax.inlet[0] takes a Message with a colon-delimited list of hashtags to 
track (max 4 right now)

- tweetpymax.inlet[1] takes a bang

- tweetpymax.outlet[0:3] outlet the count since last bang of corresponding hashtag



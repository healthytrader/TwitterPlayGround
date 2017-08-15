FROM python:2
ADD mytwitter.cfg /
ADD streamer.py /
RUN pip install tweepy
CMD ["python","./streamer.py"]

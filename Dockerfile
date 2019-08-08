FROM python:3

WORKDIR /python/biwenger-bot/
RUN pip install requests && \
	pip install numpy && \
	pip install matplotlib && \
	pip install sklearn

ADD . .
EXPOSE 8100
ENTRYPOINT python biwenger-bot


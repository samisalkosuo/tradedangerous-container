FROM docker.io/python:3.11-alpine

WORKDIR /tradedangerous

#install git, flask and Trade-Dangerous from sources
RUN apk add git && \
    git clone https://github.com/eyeonus/Trade-Dangerous && \
    cd Trade-Dangerous && \
    pip install -r requirements/publish.txt && \
    pip install flask && \
    python setup.py install && \
    cd /tradedangerous && \
    rm -rf Trade-Dangerous

#uncomment to skip build cache
#ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

#import data, takes ~10min or so
RUN trade import -P eddblink -O all,skipvend

#add web helper and other sources
COPY src ./src/

COPY trade.sh ./ 

#exec mode: cli, shell, web
ENV EXEC web

ENTRYPOINT [ "sh","./trade.sh" ]
#CMD ["/bin/sh"]

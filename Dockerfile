FROM debian:stable

RUN apt-get update && \
    apt-get install -y net-tools python3 python3-pip git tor curl unzip gnupg

WORKDIR /socialpwned
COPY . /socialpwned

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt && \
    pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint && \
    /usr/bin/python3 /socialpwned/lib/GHunt/docker/download_chromedriver.py && \
    chmod +x /socialpwned/start.sh
ENTRYPOINT ["/socialpwned/start.sh"]

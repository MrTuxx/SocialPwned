FROM debian:stable
RUN apt-get update
RUN apt-get install net-tools python3 python3-pip git tor -y
WORKDIR /socialpwned
COPY . /socialpwned
RUN pip install -r requirements.txt
RUN pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
RUN chmod +x /socialpwned/start.sh
ENTRYPOINT ["/socialpwned/start.sh"]

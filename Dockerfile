FROM python:3.8

RUN apt-get update && \
apt-get install -y --no-install-recommends \
locales \
apt-transport-https \
cron \
vim \
locales \
&& apt-get autoremove -y \
&& rm -r /var/cache/apt/archives/* \
&& rm -r /var/lib/apt/*

RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN mkdir /var/logs

WORKDIR /opt/project
COPY requirements.txt /opt/project/
RUN pip install -U pip && pip install -r requirements.txt

COPY . /opt/project/

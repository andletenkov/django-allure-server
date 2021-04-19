FROM python:3.9

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk8-installer;

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

ENV ALLURE_VERSION 2.13.8
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/${ALLURE_VERSION}/allure-commandline-${ALLURE_VERSION}.zip && \
    unzip allure-commandline-${ALLURE_VERSION}.zip -d /allure && \
    rm allure-commandline-${ALLURE_VERSION}.zip

ENV PATH="/allure/allure-${ALLURE_VERSION}/bin:${PATH}"

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

COPY ./ .

RUN mkdir db && \
    chmod +x run_worker.sh && \
    chmod +x run_app.sh

EXPOSE 8001
CMD ["/bin/sh", "-c", "./run_app.sh"]
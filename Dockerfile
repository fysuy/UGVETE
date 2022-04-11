FROM python:3.9.12
RUN apt-get update && apt-get -y update
RUN pip3 -q install pip --upgrade
RUN mkdir ugvete
WORKDIR ugvete/
COPY . .
RUN apt-get install swig -y
RUN pip3 install -r dependencies.txt
EXPOSE 80

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

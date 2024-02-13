FROM jupyter/datascience-notebook:lab-3.5.0

RUN pip install --upgrade pip
RUN pip install jupyterlab
RUN jupyter serverextension enable --py jupyterlab

WORKDIR $HOME
RUN mkdir config jupyternb output rightgbm
COPY lib.sh /home/jovyan
COPY writelib.sh /home/jovyan

EXPOSE 8888
VOLUME ["/home/jovyan/jupyternb"]

CMD ['/bin/bash']

FROM alejandrox1/ubuntu_miniconda

RUN apt-get update -y

RUN pip install sqlalchemy
RUN pip install psycopg2
RUN pip install kafka==1.3.3
RUN pip install ipython

COPY store_data_fancy.py /app/store_data_fancy.py
WORKDIR /app

# default entrypoint "/bin/bash -c"

FROM continuumio/miniconda3:4.10.3

COPY ./requirements/requirements.txt ./requirements.txt
COPY ./datazeit ./datazeit

RUN /opt/conda/bin/pip install -r requirements.txt
RUN /opt/conda/bin/pip install --no-deps -e /datazeit

WORKDIR /
CMD ["conda", "run", "--no-capture-output", "-n", "base", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]




FROM python:3.12-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN useradd -ms /bin/bash moh

# USER moh

COPY . /app

# COPY . .
# WORKDIR /home/moh


WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements3.txt

EXPOSE 8501

# RUN rm -rf .gitignore Procfile README.org README.md.bak reqirments_new.txt requirements.txt setup.sh __pycache__/

# ENTRYPOINT ["streamlit","run"]

CMD ["streamlit","run","app.py"]

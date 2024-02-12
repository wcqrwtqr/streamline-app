FROM python:3.12-slim-bullseye

# Create a non-root user
# RUN groupadd -r myapp && useradd -r -g myapp myapp

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy files to the container
COPY . /app

# Set ownership to the non-root user
# RUN chown -R myapp:myapp /app

# Switch to the non-root user
#USER myapp


# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements3.txt

# Expose port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]






# FROM python:3.12-slim-bullseye

# ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # RUN useradd -ms /bin/bash moh

# # USER moh

# COPY . /app

# # COPY . .
# # WORKDIR /home/moh


# WORKDIR /app
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements3.txt

# EXPOSE 8501

# # RUN rm -rf .gitignore Procfile README.org README.md.bak reqirments_new.txt requirements.txt setup.sh __pycache__/

# # ENTRYPOINT ["streamlit","run"]

# CMD ["streamlit","run","app.py"]

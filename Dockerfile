FROM python:3.12-slim

WORKDIR /app

RUN apt update && \
    apt install -y \
    build-essential \
    curl \
    # software-properties-common \
    git && \
    apt clean

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# RUN git clone git@github.com:FalconPoncho/murder-mystery-fbi.git

COPY requirements.txt .

# Create and activate virtual environment, and install dependencies
ENV VIRTUAL_ENV=venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin/:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
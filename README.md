# Gaia API
Gaia backend

## Features
- Text Translation
- Text to Speech
- Medical Queries
- Mental Health Queries

## Installation

1. - Clone the repo to your local system
   ```git
   git clone https://gitlab.niveussolutions.com/niv-hack/niv-hack-2023/t3-tribe/vertexai-api.git
   cd vertexai-api
   ```

2. Create a virtual environment and activate it
   ```bash:
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install the dependencies
    ```bash:
    pip3 install -r requirements.txt
    ```

4. Generate a Google Service Account config file and save it in a file named CREDENTIALS in env.

5. Then, run the development server:
    ```bash:
    python3 main.py
    ```

## Installation using Docker
1. Build the Docker image using the following command:
    ```bash:
    docker build -t gaia .
    ```

2. Run the Docker container using the following command:
    ```bash:
    docker run -p 8080:8080 -e .env gaia
    ```


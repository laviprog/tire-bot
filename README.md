# TIRE-BOT
This is a Telegram bot designed for motorcycle service appointment scheduling. Users can easily book maintenance or repair sessions via an intuitive chat interface.  

## Getting started
Follow the steps below to set up and run the TIRE-BOT using Docker.

### 📦 Install Dependencies

You can use either uv (recommended for speed) or pip.

#### Using `uv`:
```bash
uv sync
```

#### Using `pip`:
1. Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
2. Activate the virtual environment:
    ```bash
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate   # Windows
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
   
### ⚙️ Configure Environment Variables

Copy the example environment file and fill in the necessary values:

```bash
cp .env.example .env
```

Edit the `.env` file to set your environment variables. You can use the default values or customize them as needed.

### 🐳 Build and Run the Docker Container

Start the Docker container with the following command:

```bash
docker compose up --build -d
```

This command will build the Docker image and start the container.

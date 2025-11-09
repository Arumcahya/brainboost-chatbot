# Streamlit Brainboost Education Chatbot
![image text](https://github.com/Arumcahya/brainboost-chatbot/blob/2ab877e5af6ff937611126ac049e2241f31fda0b/ui-brainboost-chatbot.png)


## Getting Started

### Prerequisites

Ensure you have Python installed. It is recommended to use `miniconda` or `conda` for environment management.

### Installation

1.  **Install Miniconda (if not already installed)**

    Download and install Miniconda from the official website: <mcurl name="Miniconda Installer" url="https://docs.conda.io/en/latest/miniconda.html"></mcurl>

2.  **Create a Conda Environment**

    Open your terminal or Anaconda Prompt and create a new environment:

    ```bash
    conda create -n brainboost-env python=3.11
    conda activate brainboost-env
    ```

3.  **Install Requirements**

    Navigate to the project directory and install the necessary packages:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application**

    ```bash
    streamlit run brainboost_chatbot.py

    The application will open in your web browser.

### Running with Docker (Optional)

1.  **Build the Docker Image**

    Navigate to the project directory and build the Docker image:

    ```bash
    docker build -t brainboost_chatbot .
    ```

2.  **Run the Docker Container**

    Run the Docker container, mapping port 8501:

    ```bash
    docker run -p 8501:8501 brainboost_chatbot
    ```

    The application will be accessible in your web browser at `http://localhost:8501`.

## Code Structure

- brainboost_chatbot.py: The main Streamlit application file, containing the chatbot UI and logic.
- requirements.txt: Lists all Python dependencies required for the project.

# Data-Spider
Data Spider is a powerful web scraping tool built with Python and FastAPI. It allows you to effortlessly scrape product information from a catalogue website and store the scraped data in a structured JSON format. The scraper is designed to be run inside a Docker container, providing a seamless and hassle-free setup process.

FLOW:
This is based on event driven architecture once the request is been made server will immediately accept or reject the response if accepted will create a background task which will  take queue of tasks as input...every task in queue is single page of the website ...scraper will process this queue in FIFO form and keep adding the scraped results of that page in products.json file as well as in redis for caching purpose


1. **storage of products**
  <img width="1244" alt="product-data" src="https://github.com/user-attachments/assets/8cea4a3e-a9c2-4ff3-a7a8-3245e912f4c5">

  
2. **Notifications on scraping each page**

  <img width="765" alt="notifications" src="https://github.com/user-attachments/assets/856a97e6-e571-4eaa-8fe0-38bd9fca8b84">

  
3. **storing results in cache which will be only used to update the database if there any price changes**
     
  
   <img width="1435" alt="cachin in redis" src="https://github.com/user-attachments/assets/9a6b1d42-264a-4628-ad1d-8cd9c47f3190">


## Prerequisites

Before diving into the installation and setup process, ensure that you have the following prerequisites installed on your system:

- Docker: Data Spider relies on Docker to run the scraper in a containerized environment. Make sure you have Docker installed on your machine. You can download and install Docker from the official website: [Install Docker](https://docs.docker.com/get-docker/).

- Docker Compose: Docker Compose is a tool for defining and running multi-container Docker applications. It simplifies the process of managing and orchestrating multiple Docker containers. Docker Compose is typically installed along with Docker. You can find installation instructions for Docker Compose on the official Docker website: [Install Docker Compose](https://docs.docker.com/compose/install/).


## Installation and Setup

Follow these step-by-step instructions to set up and run the Data Spider scraper on your local machine:

1. **Clone the Repository**:
   Start by cloning the Data Spider repository to your local machine. Open a terminal and run the following command:

   ```bash
   git clone 
   cd Data-Spider
   
2.  **docker commands to initialise app**:
    Build the Docker Image:
    With the configuration in place, you're ready to build the Docker image for the Data Spider scraper. In the terminal, make sure you're still in the project directory and run the following command:
    ```bash
    docker-compose build
    //running the container default port 8000
    docker-compose up
    ```

3.  **import this curl in postman or use fastapi Swagger documentation to initialise the scraper**
    
    make sure to replace the auth token with right key provided
    ```bash
        curl --location --request POST 'localhost:8000/scrape?max_pages=10&proxy=' \
        --header 'AUTH-TOKEN: XXXX-YYYY-ZZZZ-AAAA'
    ```
    fast api doc link
    ```
    http://localhost:8000/docs

    ```
    <img width="1369" alt="API results" src="https://github.com/user-attachments/assets/43947d9e-bf0c-4c30-a4ce-818e4aae980e">

4. ***cached results can be checked by entering redis container using below commands***

   ```bash
    docker exec -it <container-id> sh
    redis-cli
   ```

   

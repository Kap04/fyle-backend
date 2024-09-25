# Fyle Backend Challenge

## Who is this for?

This challenge is meant for candidates who wish to intern at Fyle and work with our engineering team. You should be able to commit to at least 6 months of dedicated time for internship.

## Why work at Fyle?

Fyle is a fast-growing Expense Management SaaS product. We are ~40 strong engineering team at the moment. 

We are an extremely transparent organization. Check out our [careers page](https://careers.fylehq.com) that will give you a glimpse of what it is like to work at Fyle. Also, check out our Glassdoor reviews [here](https://www.glassdoor.co.in/Reviews/Fyle-Reviews-E1723235.htm). You can read stories from our teammates [here](https://stories.fylehq.com).


## Challenge outline

**You are allowed to use any online/AI tool such as ChatGPT, Gemini, etc. to complete the challenge. However, we expect you to fully understand the code and logic involved.**

This challenge involves writing a backend service for a classroom. The challenge is described in detail [here](./Application.md)


## What happens next?

You will hear back within 48 hours from us via email. 


## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```
### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```



### Docker Instructions

1. **Build the Docker image:**

   In the project directory, run the following command to build the Docker image:

   ```bash
   docker build -t fyle-backend-challenge .
   ```

2. **Start the Application with Docker Compose:**

   We recommend using Docker Compose to orchestrate the application easily.
   If you have a `docker-compose.yml` file already set up, you can start the services by running:

   ```bash
   docker-compose up --build
   ```

   This will:
   - Build the Docker image if necessary.
   - Start the containerized services.

   To run the containers in detached mode, use:

   ```bash
   docker-compose up -d
   ```

3. **Access the Application:**

   After starting the services, you can access the application by visiting the appropriate URL (e.g., `http://localhost:5000`), based on your `docker-compose.yml` configuration.

4. **Running Tests inside Docker:**

   You can run the tests inside the Docker container by executing:

   ```bash
   docker-compose exec app pytest -vvv -s tests/
   ```

   For test coverage:

   ```bash
   docker-compose exec app pytest --cov
   ```

5. **Shutting Down the Services:**

   When you're done, stop and remove the containers by running:

   ```bash
   docker-compose down
   ```




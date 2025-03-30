# Restaurant Chatbot Project

## 1. Project Overview
This chatbot automates the process of taking customer orders and tracking order status for a restaurant.  
It interacts with users via Dialogflow and processes and updates orders using a backend SQL database.  
The chatbot captures user intents, retrieves menu details, creates and manipulates orders, calculates order totals, and tracks order progress, enhancing efficiency and user experience.

## 2. Features
- **Natural Language Processing**  
  The chatbot understands customer queries, intents and processes orders using Google Cloud's Dialogflow.

- **Order Management**  
  Customers can place, modify, or cancel orders dynamically.

- **Order Tracking**  
  Users can check the status of their orders in real time.

- **Database Integration**  
  The chatbot connects to an SQL database to store order details and retrieve menu information.

- **Python Backend**  
  The chatbot’s logic is implemented using Python and FastAPI for handling requests.

## 3. Installation
To set up and run the chatbot:

1. Clone the repository and navigate to the project directory.
2. Ensure you have **MySQL Workbench CE** and an (IDE) used for programming in Python like **Pycharm Community Edition** is installed on your device.
3. Save project files in your desired directory.
  - Set the working directory in **Bash or Command Prompt:**  
     ```bash
     cd /path/to/your/project

4. Install dependencies using:  
  - **Command Prompt or Bash:**  
     ```bash
       pip install -r requirements.txt
     
5. Import the Dialogflow Agent
   - Open **Dialogflow Console** ([dialogflow.cloud.google.com](https://dialogflow.cloud.google.com/)).
   - Select your agent from the left panel.
   - Click on the **⚙️ Settings (gear icon)** in the left menu.
   - Click on the **Export and Import** tab.
   - Click **Import from ZIP** and upload the exported file.
   - Confirm the import and wait for Dialogflow to restore the agent.
     
   - Note: Make sure the **Webhook** button under the **Fulfilment** tab is Enabled. 
     
6. Install **ngrok** for secure and external access to the local server, **ngrok** for HTTPS can be utilized to establish an HTTPS tunnel, ensuring encrypted and reliable communication.
   - Download and Install **ngrok** from https://ngrok.com/downloads/windows and save it to your project's directory.
   
7. Set up a MySQL database and configure connection settings.
   - Open **MySQL Workbench CE**.
   - Create a connection and load the data using **Server > Data Import**.

## 4. Data Sources

### **1. MySQL Database (`pandeyji_eatery`)**
Contains the following tables:
- **`orders`** – Stores customer orders.
- **`menu`** – Holds menu items and prices.
- **`order_tracking`** – Tracks order statuses.

### **2. Python Scripts**
- **`main.py`** – Handles chatbot requests and processes user intents.
- **`db_helper.py`** – Interacts with the database to insert and retrieve order data.
- **`generic_helper.py`** – Provides utility functions for data formatting and session handling.

## 5. How to Use (Once all Installation Steps are completed)

1. Run the following FastAPI command using **Command Prompt or Bash:**:
   ```bash
    uvicorn main:app --reload

2. Run the following Ngrok command using **Command Prompt or Bash:**:
   ```bash
    ngrok http 8000
  Note: In FastAPI, the default port is 8000. How to check your running server’s port? Look at the terminal when you start FastAPI. It shows something like: 'Uvicorn running on http://127.0.0.1:8000'

3. Copy the https url (eg. https://7de1-82-2-105-194.ngrok-free.app) that appears and paste it in Dialogflow's **Fulfilment** tab URL text box and Save.

4. Once connection is established open Dialogflow's **Intigration** tab and choose the **web demo** icon and click **Enable**.

5. Open the URL to interact with the Chatbot:

### **Chatbot Interactions**
- **Place a new order**  
User: *"I’d like to make an order."*  
Bot: *"Starting new order. Specify food items and quantities. For example, you can say, "I would like to order two pizzas ..."*

- **Modify an order**  
User: *"Remove one pizza from my order."*  
Bot: *"Pizza removed. Here’s what’s left in your order: ..."*

- **Track an order**  
User: *"Where is my order?"*  
Bot: *"Your order is in progress."*


## 6. Technologies Used
- **Google Cloud Dialogflow**
- **Python (FastAPI)**
- **MySQL**
- **Uvicorn (for running the API server)**



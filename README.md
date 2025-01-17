Data Extraction from Financial Documents
This project is a data extraction pipeline designed to extract Profit & Loss (P&L) related information from financial documents (e.g., PDFs) and answer specific questions based on the extracted data. The application leverages various Python libraries and machine learning models to accurately parse, retrieve, and answer questions about financial data.

Features
Document Parsing: Extract relevant information such as revenue, expenses, and profit from P&L statements.
Question Answering: Answer specific queries about financial data based on the extracted content.
Streamlit Interface: Interactive web interface built with Streamlit for easy interaction.
Containerization: Dockerized application for easy deployment.
Requirements
Python 3.9+
Docker (for containerization)
Installation
1. Clone the repository:
bash
Copy
Edit
git clone https://github.com/aanchalbagotiya/QA-Bot.git
cd data-extraction
2. Install dependencies:
First, ensure that you have the requirements.txt file in the repository. It should contain all the necessary Python libraries.

bash
Copy
Edit
pip install -r requirements.txt
If you’re using Docker, the dependencies will be installed automatically when building the container (as part of the Dockerfile).

3. Running the Application Locally:
Without Docker:
Run the following command to start the Streamlit application:

bash
Copy
Edit
streamlit run streamlit-app.py
The application will be accessible at http://localhost:8501.

With Docker:
Build the Docker image:

bash
Copy
Edit
docker build -t streamlit-app .
Run the container:

bash
Copy
Edit
docker run -p 8501:8501 streamlit-app
The app will be accessible at http://localhost:8501.

Project Structure
Dockerfile: The Dockerfile used to containerize the application.
requirements.txt: List of Python dependencies required to run the project.
streamlit-app.py: Main Streamlit app for the user interface.
app/: Contains other necessary files such as scripts for data extraction and question answering.
How It Works
Data Extraction:

The application uses libraries like PyPDF2, pdfplumber, or camelot to extract text or tables from PDF files.
Relevant data (like revenue, expenses, and profit) is parsed from the financial documents.
Question Answering:

A question answering model is used to answer user queries based on the extracted data.
You can ask questions like "What is the total revenue?", "What is the net profit?", etc., and the model will extract the relevant information from the P&L statement.
Streamlit Interface:

Users can upload PDF documents via the Streamlit interface.
The user is presented with the option to ask specific questions about the document, and the application will display the answers.
Docker Instructions
Build Docker Image: Build the Docker image using the following command:

bash
Copy
Edit
docker build -t streamlit-app .
Run the Application: Run the containerized application:

bash
Copy
Edit
docker run -p 8501:8501 streamlit-app
Access the App: Open your browser and go to http://localhost:8501 to interact with the application.

Performance Considerations
Optimization: The pipeline is designed to handle large financial documents and multiple queries without latency issues.
Accuracy: Special care has been taken to ensure accurate parsing and retrieval of terms from the P&L statements for precise question answering.
Contributing
Fork the repository
Create a new branch (git checkout -b feature-name)
Make your changes and commit them (git commit -am 'Add new feature')
Push to your branch (git push origin feature-name)
Create a new Pull Request
License
This project is licensed under the MIT License - see the LICENSE file for details.

How to Use
Upload a Document: Once the app is running, click the "Browse Files" button and upload a financial document (such as a PDF).
Ask Questions: After uploading, you can ask specific questions about the document (e.g., "What is the total revenue?").
Get Answers: The app will extract relevant data from the document and return answers based on the queried information.

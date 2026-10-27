# AI-Powered Code Analyzer and Repair Platform

## Project Overview

The AI-Powered Code Analyzer and Repair Platform is a web-based application designed to help developers identify programming errors, understand their root causes, and improve code quality using Artificial Intelligence. The platform integrates Python, Flask, the Groq API, and a Llama large language model to provide intelligent code analysis, debugging assistance, and optimization suggestions through a user-friendly interface.

## Technology Stack

**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, Flask  
**AI Integration:** Groq API and Llama language model  
**Database:** SQLite  
**Development Tools:** Visual Studio Code, Git, GitHub

## Frontend Development

The frontend is developed using HTML, CSS, and JavaScript to provide an interactive interface for users. It allows developers to submit source code for analysis and view the results in a structured format. The interface presents error explanations, possible corrections, and optimization recommendations in an understandable manner, making the platform accessible to both beginners and experienced programmers.

## Backend Development

Python and Flask form the core of the backend architecture. Flask handles HTTP requests, application routing, form submissions, and communication between the frontend and AI service. When a user submits code, the backend receives the input, prepares the appropriate prompt, and sends the request to the Groq API. The application processes the returned response and displays the analysis results on the webpage.

Flask's rendering and session management capabilities support the application's web interface and user interactions. SQLite is used to store user-related information, providing lightweight database functionality without requiring a separate database server.

## AI Integration and Code Analysis

The platform integrates the Groq API with a Llama language model to perform intelligent code analysis. The submitted source code is combined with a prompt describing the required analysis, and the request is sent to the AI service. The model's response is then processed by the backend and presented to the user.

The platform focuses on three major capabilities:

1. **Error Detection and Explanation:** Identifies potential programming errors and explains their possible causes in simple language, helping developers understand and debug their code.
2. **Code Optimization:** Provides recommendations for improving code efficiency, readability, and performance, including suggestions related to time and space complexity.
3. **Smart Code Repair:** Generates corrected versions of submitted code while aiming to preserve its intended functionality and original logic.

These features help reduce manual debugging effort and support a more efficient development workflow. The AI-generated suggestions are intended to assist developers and should be reviewed and tested before being used in production applications.

## Database Management

SQLite is used for database operations and persistent storage of user-related information. The backend interacts with the database to manage relevant records, while password hashing is handled using Werkzeug utilities. Flask sessions support maintaining user state across requests.

## Project Objective and Learning Outcomes

The primary objective of this project is to demonstrate how AI services can be integrated into a web application to solve practical software development problems. It combines frontend development, backend programming, API integration, database management, and prompt engineering in a single application.

Developing this platform provided practical exposure to Flask routing, HTTP request handling, REST-style API communication, SQL database operations, session management, and integrating large language models into software applications. It also demonstrates how AI-assisted tools can support debugging, code understanding, and optimization while keeping developers involved in reviewing the generated results.

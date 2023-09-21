# Threat Watch Web Application

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Setting Up the Database](#setting-up-the-database)
- [Running the Application](#running-the-application)

## Overview
The Threat Watch web application is a powerful security intelligence platform built using Flask, Microsoft SQL Server, and Python. It provides real-time insights into emerging cyber threats and vulnerabilities, empowering organizations to proactively defend their digital infrastructure.

## Prerequisites
Before running the application, make sure you have the following installed:
- Python (3.6 or higher)
- Virtual Environment
- Microsoft SQL Server

## Getting Started
Clone the repository:
git clone https://github.com/yourusername/threat-watch.git

Navigate to the project directory:
cd ThreatWatch

Create a virtual environment (optional but recommended):
python -m venv venv

Activate the virtual environment:
On Windows:
.\venv\Scripts\activate.bat

On macOS and Linux:
source venv/bin/activate

Setting Up the Database
Create a new database in Microsoft SQL Server.

Update the SQLALCHEMY_DATABASE_URI in the config.py file with the connection string for your database.

Running the Application
Install the required dependencies
Run the application:
flask run

Open your web browser and go to http://localhost:5000 to access Threat Watch.

# Parcel Locker Project  
An automated parcel locker system that allows users to send and receive parcels via a smart locker. It includes email notifications for package updates and integrates voice control for easy program management.

## Project Description  
The Parcel Locker project is designed to streamline the process of sending and receiving parcels through an automated locker system. The application notifies users of parcel statuses via email and offers a voice-controlled interface for easier interaction.

Key Features:
- Sending and receiving parcels through an automated locker.
- Email notifications to users for package updates.
- Voice control interface for managing parcel tasks.

Technology Stack:
- Python 3.13
- Libraries: `email-validator`, `geopy`, `python-dotenv`, `speechrecognition`, `pyaudio`, `elevenlabs`, `openai`, `pipwin`
- Testing and Development: `pytest`, `pytest-cov`, `mypy`, `pyright`

## System Requirements  
- Python version: 3.13  
- Required packages and dependencies: pipenv

## Installation  
To set up the environment and run the project, follow these steps:

```bash
# Clone the repository
git clone https://github.com/your-account/your-project.git
cd your-project

# Install dependencies with Pipenv
pipenv install

# Activate the virtual environment
pipenv shell

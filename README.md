# Birthday Reminder Application

This repository contains a Python application that reads a list of birthdays from a CSV file and sends out birthday wishes via email.

## Features

- Reads birthdays and email addresses from a CSV file.
- Calculates the number of days until the next birthday for each person.
- Generate a birthday image (OpenAI Dall-e 3 prompt)
- Genarete a birthday wish (OpenAI / langachain chat prompt)
- Upload birthday image and card to AWS S3 bucket (AWS S3 service)
- Sends an email with a birthday wish on the day of the person's birthday (AWS SES service)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- OpenAI key
- AWS S3 credentials
- AWS SES credentials
- Python 3
- AWS SDK 
- OpenAI
- langchain
- pandas
- Other Python packages

### Installation

1. Clone this repository.
2. Install the required Python packages.

### Usage

1. Update the `birthdays.csv` file with the names, birthdays, and email addresses of the people you want to send birthday wishes to.
2. Run the `birthday.py` script.

## Code Overview

The main script is `birthday.py`. It reads the `birthdays.csv` file, calculates the number of days until the next birthday for each person, and calls the `handle_birthday` function on the day of the person's birthday.

The `handle_birthday` function generates a birthday message, creates a birthday card and an HTML page, uploads them to a server, and sends an email with the birthday card attached and a link to the birthday page.
# SmartMoving CRM Automation System

This is a Selenium-based automation system designed to extract and process data from the SmartMoving CRM Application.  

The following instructions will guide you to set up, configure, and run the system on your local computer.


## Prerequisites

1. **Python**  
   - Download the latest Python version: https://www.python.org/downloads/  
   - During installation, check the box “Add Python to PATH”  
   - Verify installation in terminal/command prompt:  
     python --version  
     pip --version

2. **IDE: VS Code**  
   - Download and install: https://code.visualstudio.com/  

3. **Git (Version Control)**  
   - Download and install Git for Windows: https://git-scm.com/download/win  
   - Verify installation:  
     git --version

---

## Setup Instructions

### 1. Open Project in VS Code
- Launch VS Code and create a new project folder  
- Open Git Bash in the terminal (`Ctrl+` ` `)  

### 2. Clone the Repository
git clone <repo_url>  
cd <project_folder>  
- Replace <repo_url> with your repository link  

### 3. Initialize Git (if not already)
git init  
git remote add origin <repo_url>  
git branch -M main  

### 4. Create and Activate Virtual Environment
python -m venv venv  
# On Windows (Git Bash):  
source venv/Scripts/activate  
# On macOS/Linux:  
source venv/bin/activate  
- Verify: (venv) should appear before the terminal prompt  

### 5. Install Project Dependencies
pip install -r requirements.txt

---

## Google API Setup

1. **Enable Google Sheets API**  
   - Follow instructions: https://docs.gspread.org/en/v6.1.4/oauth2.html#enable-api-access-for-a-project

2. **Create a Service Account for Bot**  
   - Follow instructions: https://docs.gspread.org/en/v6.1.4/oauth2.html#for-bots-using-service-account  
   - Download the JSON credentials file  

3. **Move JSON to Project Directory**  
   - Place the downloaded JSON file in the root folder of your project  
   - Rename the file to:  
     service_account.json

---

## Environment Variables

1. Create a file named `.env` in the root project folder  
2. Add the following lines (replace with your credentials):  
SMARTMOVING_USERNAME=your_username  
SMARTMOVING_PASSWORD=your_password  

NINETYIO_USERNAME=your_username  
NINETYIO_PASSWORD=your_password  

- Ensure there are no trailing spaces  

---

## Google Sheets Setup

1. Create a Google Spreadsheet for bot access  
2. Add sheets according to storage needs (e.g., Office Calendar, Sales)  
3. Share the spreadsheet with the bot:  
   - Open service_account.json  
   - Copy the client_email value  
   - Share the spreadsheet with this email as an Editor  

---

## Running the System

1. Activate the virtual environment:  
# Windows  
source venv/Scripts/activate  
# macOS/Linux  
source venv/bin/activate  

2. Run your main script (example):  
python main.py



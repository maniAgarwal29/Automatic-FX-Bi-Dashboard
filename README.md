Automated Currency Exchange Rate Dashboard
🔴 Live Dashboard

This project showcases a fully automated, 8-page interactive Power BI dashboard that tracks the daily exchange rate of the US Dollar (USD) against seven major global currencies.

Main Page (Overview & Navigation Center)
![Image](https://github.com/user-attachments/assets/f190956f-e69f-41b3-98f1-7d8baad2f474)


Detail Page (Comprehensive Analysis per Currency)


![Image](https://github.com/user-attachments/assets/e6661877-3ed2-45c4-a99d-b985a93a3cde)


![Image](https://github.com/user-attachments/assets/fa47d2b9-369a-45a3-9a98-4b42efb0b7d1)

![Image](https://github.com/user-attachments/assets/8c24add3-efd7-496d-baaf-9d862e5942d5)


🎯 Project Goal
The primary aim of this initiative was to create a professional-grade, end-to-end business intelligence solution. The pipeline automatically collects both daily and historical currency exchange rates, processes and stores the data in a cloud-based repository, and visualizes the results through an interactive dashboard built in Power BI. The entire process operates without any manual input.

🧰 Technology Stack & System Architecture
A modern, serverless design powers this robust and scalable data pipeline.

Technology	Role
Python	Core tool for automation, data retrieval, and processing.
Pandas Library	Handles data cleansing, transformation, and structuring from the API.
Requests Library	Facilitates HTTP requests to the currency exchange rate API.
Google Cloud Platform	Enables cloud connectivity through essential APIs.
Google Sheets & Drive APIs	Allow automated updates to the cloud-based spreadsheet.
Google Sheets	Serves as a lightweight, serverless cloud database.
Power BI	Used for data modeling, analysis, and interactive visualizations.
DAX	Drives complex metrics such as Moving Averages, Volatility, and Summaries within Power BI.
Git & GitHub	Manages version control and public project portfolio.

🔄 Automation Process
The workflow is divided into two fully automated stages:

Backend (Python): A Python script (update_sheets.py) runs daily via Windows Task Scheduler. It retrieves the latest data from the Frankfurter API and updates the corresponding Google Sheet.

Frontend (Power BI): The Power BI dashboard uses a Scheduled Refresh setup in the Power BI Service to automatically fetch the latest data from Google Sheets every day, ensuring the visuals stay current.

✨ Notable Features
Fully Automated Workflow: The system updates both data and visualizations daily without any manual effort.

Interactive Design: The Main Page acts as a centralized dashboard. Selecting any currency card leads to its respective analysis page via Power BI bookmarks.

Comprehensive Visual Insights: Each detail page includes diverse visuals, such as:

KPI Cards showing current rate, historical highs/lows, and daily percentage change.

Historical Trend Line featuring 7-day and 30-day moving averages to reveal patterns.

Volatility Chart summarizing the past 60 days of daily performance.

Narrative Analysis: Each currency’s page features a dynamically generated natural-language summary using DAX, offering context about recent performance and historical positioning.

Serverless Architecture: Utilizes Google Cloud tools and Google Sheets as a storage solution, highlighting a modern, lightweight approach to data engineering.

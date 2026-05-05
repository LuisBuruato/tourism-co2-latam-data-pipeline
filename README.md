🌍 Tourism vs CO₂ Emissions in LATAM
End-to-End Data Engineering Pipeline on AWS
🌐 Live Dashboard

👉 https://tourism-co2-latam-data-pipeline-wrpgpj54yuhwc66tdgqmqn.streamlit.app/

🚀 TL;DR

End-to-end data pipeline on AWS analyzing tourism vs CO₂ emissions in LATAM, using Medallion Architecture (Bronze → Silver → Gold), orchestrated with Airflow and visualized in Streamlit.

📌 Overview

This project is an end-to-end data pipeline that analyzes the relationship between tourism activity and CO₂ emissions across Latin America.

It integrates multiple datasets, processes them through a layered architecture (Bronze → Silver → Gold), orchestrates workflows using Apache Airflow, and presents insights through an interactive Streamlit dashboard.

🎯 Objectives
Analyze correlations between tourism growth and environmental impact
Build a scalable and modular data pipeline
Apply Medallion Architecture (Bronze → Silver → Gold)
Enable data-driven insights through visualization
🏗️ Architecture

The pipeline follows a layered architecture:

Bronze Layer → Raw data ingestion from external sources
Silver Layer → Data cleaning, validation, and transformation
Gold Layer → Aggregated and analytics-ready datasets

Orchestrated using Apache Airflow and stored in AWS (S3 + processing layer).

🧠 Architecture Diagram

🔄 Data Flow
Extract
Tourism data
CO₂ emissions (OWID)
Bronze Layer
Raw partitioned data by country and year
Silver Layer
Cleaned and integrated datasets
Gold Layer
Aggregated KPIs ready for analytics
Visualization
Interactive dashboard (Streamlit) 

⚙️ Tech Stack
🐍 Python
📊 Pandas
🔄 Apache Airflow
🐳 Docker
🌐 Streamlit
📁 Parquet (data storage)
☁️ AWS S3
📊 Dashboard Features
🌱 KPIs Overview
Total CO₂ emissions
Total tourism arrivals
Decoupling index
## 📊 Dashboard Features

### 🌱 KPIs Overview
- Total CO₂ emissions  
- Total tourism arrivals  
- Decoupling index  

---

### 📈 CO₂ Emissions Over Time
![CO2](https://raw.githubusercontent.com/LuisBuruato/tourism-co2-latam-data-pipeline/main/assets/TourismvsCO2.PNG)

---

### ✈️ Tourism Trends
![Tourism](https://raw.githubusercontent.com/LuisBuruato/tourism-co2-latam-data-pipeline/main/assets/TourismArrivals.PNG)

---

### 🔗 Correlation Analysis
![Correlation](https://raw.githubusercontent.com/LuisBuruato/tourism-co2-latam-data-pipeline/main/assets/TourismCorrelation.PNG)

---

### 🏆 Sustainability Ranking
![Sustainable](https://raw.githubusercontent.com/LuisBuruato/tourism-co2-latam-data-pipeline/main/assets/SustainableCountries.PNG)

📈 Results
Consolidated datasets across multiple LATAM sources
Identified trends between tourism and CO₂ emissions
Delivered interactive insights via dashboard
📌 Key Insights
Tourism growth does not always correlate linearly with CO₂ emissions
Some countries show signs of decoupling, indicating sustainable growth
COVID-19 created visible disruptions in both tourism and emissions.


🗂️ Project Structure
├── dags/                # Airflow DAGs
├── scripts/             # ETL scripts
├── dashboard/           # Streamlit app
├── data/
│   ├── gold/            # Final curated dataset
├── assets/              # Images for documentation
├── docker-compose.yml   # Airflow setup
├── requirements.txt

⚙️ How to Run Locally
1. Clone the repository
git clone https://github.com/LuisBuruato/tourism-co2-latam-data-pipeline.git
cd tourism-co2-latam-data-pipeline
2. Start services with Docker
docker-compose up --build
3. Access Airflow
http://localhost:8080
4. Run the DAG
Enable DAG: tourism_co2_pipeline
Trigger execution
5. Run the dashboard
streamlit run dashboard/app.py


💼 Why This Project Matters

This project demonstrates:

End-to-end data engineering skills
Workflow orchestration with Airflow
Data modeling (Bronze / Silver / Gold)
Data visualization & storytelling
Production-ready pipeline design


🧠 Note

This is an independent implementation created for portfolio purposes, using a custom architecture and design approach.


🚀 Future Improvements
Real-time data ingestion (streaming)
Advanced analytics / forecasting models
Data quality monitoring (Great Expectations)
CI/CD pipeline for automated deployments
👨‍💻 Author

Luis Ramón Buruato

📧 luisburuato@gmail.com

🔗 https://github.com/LuisBuruato

🔗 https://www.linkedin.com/in/luis-ramon-buruato-1a949741/

⭐ If you like this project

Give it a star ⭐ on GitHub!

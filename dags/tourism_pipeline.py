from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# =========================
# CONFIG
# =========================

default_args = {
    "owner": "luis",
    "retries": 1
}

# =========================
# DAG
# =========================

with DAG(
    dag_id="tourism_co2_pipeline",
    default_args=default_args,
    description="ETL pipeline tourism + CO2 LATAM",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    # =========================
    # TASK 1 - EXTRACT
    # =========================

    extract = BashOperator(
        task_id="extract_data",
        bash_command="python /opt/airflow/scripts/extract.py"
    )

    # =========================
    # TASK 2 - BRONZE (CO2)
    # =========================

    bronze_co2 = BashOperator(
        task_id="bronze_co2",
        bash_command="python /opt/airflow/scripts/bronze_owid_partition.py"
    )

    # =========================
    # TASK 3 - SILVER
    # =========================

    silver = BashOperator(
        task_id="silver_integration",
        bash_command="python /opt/airflow/scripts/silver_integrated.py"
    )

    # =========================
    # TASK 4 - GOLD
    # =========================

    gold = BashOperator(
        task_id="gold_kpis",
        bash_command="python /opt/airflow/scripts/gold_kpis.py"
    )

    # =========================
    # FLOW
    # =========================

    extract >> bronze_co2 >> silver >> gold
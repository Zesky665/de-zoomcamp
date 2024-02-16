import requests
import sys

def get_quarter(quarter: int):
    if quarter == 1:
        return ["01", "02", "03"]
    elif quarter == 2:
        return ["04", "05", "06"]
    elif quarter == 3:
        return ["07", "08", "09"]
    elif quarter == 4:
        return ["10", "11", "12"]
    else:
        raise ValueError("Invalid quarter")

def ingest_month(year: str, month: str):
    url = "http://localhost:6789/api/pipeline_schedules/5/pipeline_runs/72ebbf5d21964c72b4fb48ff63f87e2e"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "pipeline_run": {
            "variables": {
                "year": year,
                "month": month
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

if __name__ == "__main__":
    year = sys.argv[1]
    quarter = int(sys.argv[2])

    months = get_quarter(quarter)
    for month in months:
        print(f"Ingesting data for month {month}")
        ingest_month(year, month)
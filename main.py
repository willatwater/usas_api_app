# main.py

from grants import search_grants
from hhs_acf_grants import update_hhs_acf_grants

# Adjustable variables
start_date = "2021-01-20"
end_date = "2024-11-17"

if __name__ == "__main__":
    # Call the search_grants function with start and end dates and the output path
    update_hhs_acf_grants(start_date, end_date)
    
# grants.py

import requests
import pandas as pd

def search_grants(start_date, end_date, program_numbers=None, tas_codes=None, output_path="output/usa_spending_api_grants.csv"):
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "filters": {
            "award_type_codes": ["02", "03", "04", "05"],  # Grant codes
            "time_period": [
                {
                    "start_date": start_date,
                    "end_date": end_date,
                    "date_type": "new_awards_only"
                }
            ]
        },
        "fields": [
            "Award ID", 
            "generated_internal_id",
            "Recipient Name", 
            "Recipient DUNS Number",
            "Awarding Agency",
            "Funding Agency",
            "Awarding Sub Agency",
            "Funding Sub Agency",
            "Description",
            "Award Amount",
            "Total Outlays",
            "Start Date",
            "End Date",
            "Place of Performance Country Code",
            "Place of Performance State Code",
            "Place of Performance City Code",
            "Base Obligation Date",
            "CFDA Number"
        ],
        "page": 1,
        "limit": 100
    }

    if program_numbers:
        data["filters"]["program_numbers"] = program_numbers
    if tas_codes:
        data["filters"]["tas_codes"] = {"require": tas_codes}

    award_data = []

    while True:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            results = response.json()
            awards_data = results.get('results', [])
            
            if not awards_data:
                break
            
            for award in awards_data:
                award_id = award.get("Award ID")
                generated_internal_id = award.get("generated_internal_id")
                recipient_name = award.get("Recipient Name")
                awarding_agency = award.get("Awarding Agency")
                description = award.get("Description")
                amount = award.get("Award Amount")
                total_outlays = award.get("Total Outlays")
                place_of_performance_country = award.get("Place of Performance Country Code")
                place_of_performance_state = award.get("Place of Performance State Code")
                place_of_performance_city = award.get("Place of Performance City Code")
                base_obligation_date = award.get("Base Obligation Date")
                cfda_number = award.get("CFDA Number")

                base_obligation_year = base_obligation_date[:4] if base_obligation_date else None
                award_url = f"https://www.usaspending.gov/award/{generated_internal_id}" if award_id else None
                
                if award_id:
                    award_data.append({
                        "Award ID": award_id,
                        "Awarding Agency": awarding_agency,
                        "Recipient Name": recipient_name,
                        "Description": description,
                        "Obligated Amount": amount,
                        "Total Outlays": total_outlays,
                        "Place of Performance Country Code": place_of_performance_country,
                        "Place of Performance State Code": place_of_performance_state,
                        "Place of Performance City Code": place_of_performance_city,
                        "Base Obligation Date": base_obligation_year,
                        "CFDA Number": cfda_number,
                        "Award URL": award_url
                    })

            data["page"] += 1
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

    if award_data:
        award_data_df = pd.DataFrame(award_data)
        award_data_df.to_csv(output_path, index=False)
        print(f"Award data has been saved to {output_path}")
    else:
        print("No award data retrieved to save to CSV.")

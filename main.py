# main.py

from grants import search_grants

# Adjustable variables
start_date = "2021-01-20"
end_date = "2024-11-01"

# Optional filters (user can specify either or both)
program_numbers = ["97.141"]  # Example CFDA program number
tas_codes = [["019", "019-1143"]]  # Uncomment to use TAS codes instead

if __name__ == "__main__":
    # Conditionally pass program_numbers and tas_codes based on which are defined
    if 'program_numbers' in locals() and program_numbers and 'tas_codes' in locals() and tas_codes:
        search_grants(start_date, end_date, program_numbers=program_numbers, tas_codes=tas_codes)
    elif 'program_numbers' in locals() and program_numbers:
        search_grants(start_date, end_date, program_numbers=program_numbers)
    elif 'tas_codes' in locals() and tas_codes:
        search_grants(start_date, end_date, tas_codes=tas_codes)
    else:
        print("Please specify at least one filter: either program_numbers or tas_codes.")




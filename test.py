from modules.initialize_data.catch_economic_data import (
    get_cpi_data,
    get_policy_rate_data,
    get_api_key
)

api_key = get_api_key()

policy_rate_df = get_policy_rate_data('2010-01-01', '2023-12-31', api_key)
print(policy_rate_df.head())

cpi_df = get_cpi_data('2010-01-01', '2023-12-31', api_key)
print(cpi_df.head())

# To make this code sample work in your Oracle Cloud tenancy,
# please replace the values for any parameters whose current values do not fit
# your use case (such as resource IDs, strings containing ‘EXAMPLE’ or ‘unique_id’, and
# boolean, number, and enum parameters with values not fitting your use case).

import oci
import requests
import csv

# Define constants that match your tenancy and the subscription you want to compare before running
OCI_CONFIG_FILE = '~/.oci/config'
SUBSCRIPTION_OCID = '' 
COMPARTMENT_OCID = ''


# Create a default config using DEFAULT profile in default location
# Refer to
# https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm#SDK_and_CLI_Configuration_File
# for more info
config = oci.config.from_file(OCI_CONFIG_FILE)

# Initialize service client with default config file
onesubscription_client = oci.onesubscription.RatecardClient(config)

# Send the request to service, some parameters are not required, see API
# doc for more info
list_rate_cards_response = onesubscription_client.list_rate_cards(
    subscription_id = SUBSCRIPTION_OCID,
    compartment_id = COMPARTMENT_OCID,
)

rate_card = list_rate_cards_response.data

# Write raw rate card to json file
with open('rate_card.json', 'w') as f:
    f.write(str(rate_card))

# Get List Prices in the same currency as the rate card and structure as a map for fast querying
api_url = 'https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?'
currency_code = rate_card[0].currency.iso_code
list_prices = requests.get(api_url + "&currencyCode=" + currency_code)
list_prices.raise_for_status()
list_prices = {o['partNumber']: o for o in list_prices.json()['items']}

# Compare each SKU in the rate card to the public rate and log in csv
fields = ['Product Name', 'SKU', 'Public Price', 'Discount', 'Net Price']
csv_output = []

# Write to CSV
with open('rate_with_discounts.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    
    for item in rate_card:
        product_name = item.product.name
        product_sku = item.product.part_number
        currency_code = item.currency.iso_code
        net_price = float(item.net_unit_price)
        precision = int(item.currency.std_precision)
        public_price = None
        discount = None

        # Verify the public prices contain the same sku that is in our rate card and calculate the discount
        if product_sku in list_prices:
            public_sku = list_prices[product_sku] 
            
            for c in public_sku['currencyCodeLocalizations']:
                if c['currencyCode'] == currency_code:
                    for p in c['prices']:
                        if p['model'] == 'PAY_AS_YOU_GO':
                            public_price = p['value']

            if public_price is None:
                discount = 'NaN'
                public_price = 'NaN'
            elif public_price == 0:
                discount = 'NaN'
                public_price = float(public_price)
            else:
                discount = round((public_price - net_price) / public_price, 4)
                public_price = round(public_price, precision)

        # Write the line for the current sku to csv file
        csv_output = {
            'Product Name': product_name,
            'SKU': product_sku,
            'Public Price': public_price,
            'Discount': discount,
            'Net Price': round(net_price, precision),
        }

        writer.writerow(csv_output)



## SHOWRATECARD - Oracle Cloud Infrastructure RateCard Reporting Tool

SHOWRATECARD is a ratecard reporting tool which uses the Python SDK to extract the ratecard from a subscription in your tenancy. 
Authentication by User.
Output is to CSV File.

**DISCLAIMER – This is not an official Oracle application,  It does not supported by Oracle Support, It should NOT be used for ratecard calculation, reporting, tracking or any other official capacity.

**Developed by Pablo Ruiz, 2024**

## Modules Included: 
- oci.onesubscription.RateCardClient

## Installation of Python 3 incase you don't have Python3 installed:
Please follow [Python Documentation](https://docs.python.org/3/using/index.html)

## Install OCI SDK Packages:
Please follow [Oracle Python SDK Documentation](https://github.com/oracle/oci-python-sdk)

## Setup connectivity using User

```  
1. Login to your OCI Cloud console

2. Create new group : ShowRateCardGroup  

3. Create new Policy: ShowRateCardGroupPolicy
 with Statements:
   Allow group ShowRateCardGroup to read subscription, billing-schedules, subscribed-services, rate-cards in tenancy 

4. Create new User  : showratecard.user -> Add to ShowRateCardGroup group  

5. Config OCI config file - ~/.oci/config
   Please follow SDK config documentation - https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm 
```

## Copy the Software
Download the show_ratecard.py from this project

## Input unique identifiers
Open the script and input the OCID of the root compartment as well as the id of the subscription you would like to download the rate card for.

Execute  
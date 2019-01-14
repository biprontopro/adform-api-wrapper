Adform API wrapper 📦
=====================

* Adform is a digital advertising platform.
* There's no Python API wrapper that I could find to communicate with Adform's API.
* This is an attempt to create an API wrapper I can use at work.


Installation
------------

```
pipenv install adform_api_wrapper
```

Getting Started
---------------

```python
import os

from adform_api_wrapper import AdformApi

ADFORM_CLIENT_ID = os.getenv('ADFORM_CLIENT_ID')
ADFORM_CLIENT_SECRET = os.getenv('ADFORM_CLIENT_SECRET')

adform_api = AdformApi(ADFORM_CLIENT_ID, ADFORM_CLIENT_SECRET)
# https://api.adform.com/v1/help/buyer/campaigns#!/Campaigns/get_v1_buyer_campaigns
all_campaigns = adform_api.get('/buyer/campaigns')
print(all_campaigns)
```

Features
--------

* Automatic fetching of authentication token
* Automatic refereshing of authentication token when it expires
* Re-using of internal session object between API calls

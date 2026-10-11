# voting_sdk.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**home_get**](DefaultApi.md#home_get) | **GET** / | Health Check


# **home_get**
> object home_get()

Health Check

### Example


```python
import voting_sdk
from voting_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = voting_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with voting_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = voting_sdk.DefaultApi(api_client)

    try:
        # Health Check
        api_response = api_instance.home_get()
        print("The response of DefaultApi->home_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->home_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


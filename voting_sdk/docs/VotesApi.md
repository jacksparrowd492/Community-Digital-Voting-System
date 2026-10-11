# voting_sdk.VotesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**revoke_vote_votes_vote_id_delete**](VotesApi.md#revoke_vote_votes_vote_id_delete) | **DELETE** /votes/{vote_id} | Revoke a vote


# **revoke_vote_votes_vote_id_delete**
> MessageResponse revoke_vote_votes_vote_id_delete(vote_id)

Revoke a vote

Revoke a previously cast vote, permitted only while the proposal remains active.

### Example


```python
import voting_sdk
from voting_sdk.models.message_response import MessageResponse
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
    api_instance = voting_sdk.VotesApi(api_client)
    vote_id = 56 # int | 

    try:
        # Revoke a vote
        api_response = api_instance.revoke_vote_votes_vote_id_delete(vote_id)
        print("The response of VotesApi->revoke_vote_votes_vote_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VotesApi->revoke_vote_votes_vote_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **vote_id** | **int**|  | 

### Return type

[**MessageResponse**](MessageResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


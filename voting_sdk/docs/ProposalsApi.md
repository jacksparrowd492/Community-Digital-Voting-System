# openapi_client.ProposalsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**close_proposal_proposals_proposal_id_close_patch**](ProposalsApi.md#close_proposal_proposals_proposal_id_close_patch) | **PATCH** /proposals/{proposal_id}/close | Manually close a proposal (Admin)
[**create_proposal_proposals_post**](ProposalsApi.md#create_proposal_proposals_post) | **POST** /proposals/ | Create a new proposal
[**get_proposal_proposals_proposal_id_get**](ProposalsApi.md#get_proposal_proposals_proposal_id_get) | **GET** /proposals/{proposal_id} | View a specific proposal with current vote counts
[**list_proposals_proposals_get**](ProposalsApi.md#list_proposals_proposals_get) | **GET** /proposals/ | Retrieve all proposals
[**vote_on_proposal_proposals_proposal_id_vote_post**](ProposalsApi.md#vote_on_proposal_proposals_proposal_id_vote_post) | **POST** /proposals/{proposal_id}/vote | Submit a vote for a proposal


# **close_proposal_proposals_proposal_id_close_patch**
> ProposalResponse close_proposal_proposals_proposal_id_close_patch(proposal_id, x_admin_token=x_admin_token)

Manually close a proposal (Admin)

Manually close an active proposal.

### Example


```python
import openapi_client
from openapi_client.models.proposal_response import ProposalResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ProposalsApi(api_client)
    proposal_id = 56 # int | 
    x_admin_token = 'x_admin_token_example' # str |  (optional)

    try:
        # Manually close a proposal (Admin)
        api_response = api_instance.close_proposal_proposals_proposal_id_close_patch(proposal_id, x_admin_token=x_admin_token)
        print("The response of ProposalsApi->close_proposal_proposals_proposal_id_close_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->close_proposal_proposals_proposal_id_close_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proposal_id** | **int**|  | 
 **x_admin_token** | **str**|  | [optional] 

### Return type

[**ProposalResponse**](ProposalResponse.md)

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

# **create_proposal_proposals_post**
> ProposalResponse create_proposal_proposals_post(proposal_create)

Create a new proposal

Create a new proposal for voting.

### Example


```python
import openapi_client
from openapi_client.models.proposal_create import ProposalCreate
from openapi_client.models.proposal_response import ProposalResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ProposalsApi(api_client)
    proposal_create = openapi_client.ProposalCreate() # ProposalCreate | 

    try:
        # Create a new proposal
        api_response = api_instance.create_proposal_proposals_post(proposal_create)
        print("The response of ProposalsApi->create_proposal_proposals_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->create_proposal_proposals_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proposal_create** | [**ProposalCreate**](ProposalCreate.md)|  | 

### Return type

[**ProposalResponse**](ProposalResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_proposal_proposals_proposal_id_get**
> ProposalDetailResponse get_proposal_proposals_proposal_id_get(proposal_id)

View a specific proposal with current vote counts

View details of a specific proposal along with current vote counts.

### Example


```python
import openapi_client
from openapi_client.models.proposal_detail_response import ProposalDetailResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ProposalsApi(api_client)
    proposal_id = 56 # int | 

    try:
        # View a specific proposal with current vote counts
        api_response = api_instance.get_proposal_proposals_proposal_id_get(proposal_id)
        print("The response of ProposalsApi->get_proposal_proposals_proposal_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->get_proposal_proposals_proposal_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proposal_id** | **int**|  | 

### Return type

[**ProposalDetailResponse**](ProposalDetailResponse.md)

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

# **list_proposals_proposals_get**
> List[ProposalResponse] list_proposals_proposals_get(status=status)

Retrieve all proposals

Retrieve all proposals, optionally filtered by status ('active', 'closed', 'expired').

### Example


```python
import openapi_client
from openapi_client.models.proposal_response import ProposalResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ProposalsApi(api_client)
    status = 'status_example' # str |  (optional)

    try:
        # Retrieve all proposals
        api_response = api_instance.list_proposals_proposals_get(status=status)
        print("The response of ProposalsApi->list_proposals_proposals_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->list_proposals_proposals_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **str**|  | [optional] 

### Return type

[**List[ProposalResponse]**](ProposalResponse.md)

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

# **vote_on_proposal_proposals_proposal_id_vote_post**
> VoteResponse vote_on_proposal_proposals_proposal_id_vote_post(proposal_id, vote_create)

Submit a vote for a proposal

Submit a vote ('yes', 'no', or 'abstain') on an active proposal.

### Example


```python
import openapi_client
from openapi_client.models.vote_create import VoteCreate
from openapi_client.models.vote_response import VoteResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ProposalsApi(api_client)
    proposal_id = 56 # int | 
    vote_create = openapi_client.VoteCreate() # VoteCreate | 

    try:
        # Submit a vote for a proposal
        api_response = api_instance.vote_on_proposal_proposals_proposal_id_vote_post(proposal_id, vote_create)
        print("The response of ProposalsApi->vote_on_proposal_proposals_proposal_id_vote_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProposalsApi->vote_on_proposal_proposals_proposal_id_vote_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **proposal_id** | **int**|  | 
 **vote_create** | [**VoteCreate**](VoteCreate.md)|  | 

### Return type

[**VoteResponse**](VoteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


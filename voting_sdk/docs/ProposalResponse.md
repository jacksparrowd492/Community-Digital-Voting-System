# ProposalResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Title of the proposal | 
**description** | **str** | Detailed proposal description | 
**id** | **int** |  | 
**created_at** | **datetime** |  | 
**deadline** | **datetime** |  | 
**status** | **str** |  | 

## Example

```python
from voting_sdk.models.proposal_response import ProposalResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProposalResponse from a JSON string
proposal_response_instance = ProposalResponse.from_json(json)
# print the JSON string representation of the object
print(ProposalResponse.to_json())

# convert the object into a dict
proposal_response_dict = proposal_response_instance.to_dict()
# create an instance of ProposalResponse from a dict
proposal_response_from_dict = ProposalResponse.from_dict(proposal_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



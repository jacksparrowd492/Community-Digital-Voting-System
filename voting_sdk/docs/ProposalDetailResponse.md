# ProposalDetailResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Title of the proposal | 
**description** | **str** | Detailed proposal description | 
**id** | **int** |  | 
**created_at** | **datetime** |  | 
**deadline** | **datetime** |  | 
**status** | **str** |  | 
**vote_counts** | [**VoteCounts**](VoteCounts.md) |  | 

## Example

```python
from voting_sdk.models.proposal_detail_response import ProposalDetailResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProposalDetailResponse from a JSON string
proposal_detail_response_instance = ProposalDetailResponse.from_json(json)
# print the JSON string representation of the object
print(ProposalDetailResponse.to_json())

# convert the object into a dict
proposal_detail_response_dict = proposal_detail_response_instance.to_dict()
# create an instance of ProposalDetailResponse from a dict
proposal_detail_response_from_dict = ProposalDetailResponse.from_dict(proposal_detail_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



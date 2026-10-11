# VoteCounts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**yes** | **int** |  | [optional] [default to 0]
**no** | **int** |  | [optional] [default to 0]
**abstain** | **int** |  | [optional] [default to 0]
**total** | **int** |  | [optional] [default to 0]

## Example

```python
from voting_sdk.models.vote_counts import VoteCounts

# TODO update the JSON string below
json = "{}"
# create an instance of VoteCounts from a JSON string
vote_counts_instance = VoteCounts.from_json(json)
# print the JSON string representation of the object
print(VoteCounts.to_json())

# convert the object into a dict
vote_counts_dict = vote_counts_instance.to_dict()
# create an instance of VoteCounts from a dict
vote_counts_from_dict = VoteCounts.from_dict(vote_counts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



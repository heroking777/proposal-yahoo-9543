import json

def validate_and_map_auction_data(data):
    # Define the expected structure of the data
    expected_structure = {
        "user_id": str,
        "auction_id": str,
        "bid_amount": float,
        "timestamp": str,
        "status": str
    }

    # Validate and map the data
    mapped_data = {}
    for key, value in data.items():
        if key in expected_structure:
            expected_type = expected_structure[key]
            if isinstance(value, expected_type):
                mapped_data[key] = value
            else:
                raise ValueError(f"Invalid type for {key}. Expected {expected_type}, got {type(value)}")
        else:
            raise KeyError(f"Unexpected key: {key}")

    return mapped_data

# Example usage
auction_data = {
    "user_id": "12345",
    "auction_id": "67890",
    "bid_amount": 100.5,
    "timestamp": "2023-04-01T12:00:00Z",
    "status": "completed"
}

try:
    validated_data = validate_and_map_auction_data(auction_data)
    print(json.dumps(validated_data, indent=4))
except (ValueError, KeyError) as e:
    print(e)
```

This Python function `validate_and_map_auction_data` takes a dictionary representing auction data and validates it against an expected structure. If the data is valid, it maps the data to a new dictionary with the same keys but ensures they are of the correct type. If there are any issues with the data (e.g., unexpected keys or incorrect types), it raises appropriate exceptions. The example usage demonstrates how to use this function and handle potential errors.
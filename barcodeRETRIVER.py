import base64

# The Base64-encoded data
base64_data = 'MDAzNjM4MzgzMTUxMQ=='

# Decode the Base64-encoded data
decoded_data = base64.b64decode(base64_data)

# Print the decoded binary data
print(decoded_data)
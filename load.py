from lambda_function import lambda_handler

print(lambda_handler({"manual": True, "count": False}, False))
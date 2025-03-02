import unittest
from unittest.mock import patch, MagicMock
from lambda_function import parse_launch_data, save_launch_to_dynamodb

class TestSpaceXLambda(unittest.TestCase):

    def test_parse_launch_data(self):
        sample_launch = {
            "fairings": {},
            "links": {},
            "static_fire_date_utc": "2006-03-17T00:00:00.000Z",
            "static_fire_date_unix": 1142553600,
            "net": False,
            "window": 0,
            "rocket": "5e9d0d95eda69955f709d1eb",
            "success": False,
            "failures": [
                {
                    "time": 33,
                    "reason": "merlin engine failure"
                }
            ],
            "details": "Engine failure at 33 seconds and loss of vehicle",
            "crew": [],
            "ships": [],
            "capsules": [],
            "payloads": [],
            "launchpad": "5e9e4502f5090995de566f86",
            "flight_number": 1,
            "name": "FalconSat",
            "date_utc": "2006-03-24T22:30:00.000Z",
            "date_unix": 1143239400,
            "date_local": "2006-03-25T10:30:00+12:00",
            "date_precision": "hour",
            "upcoming": False,
            "cores": [],
            "auto_update": True,
            "tbd": False,
            "id": "5eb87cd9ffd86e000604b32a"
        }
        parsed = parse_launch_data(sample_launch)
        self.assertEqual(parsed["launch_id"], "5eb87cd9ffd86e000604b32a")
        self.assertEqual(parsed["order_id"], "5eb87cd9ffd86e000604b32a_")
        self.assertEqual(parsed["mission_name"], "FalconSat")
        self.assertEqual(parsed["rocket_id"], "5e9d0d95eda69955f709d1eb")
        self.assertEqual(parsed["launch_date"], "2006-03-24T22:30:00.000Z")
        self.assertEqual(parsed["status"], "FAILED")
        self.assertEqual(parsed["launchpad"], "5e9e4502f5090995de566f86")

    @patch("boto3.resource")
    def test_save_launch_to_dynamodb(self, mock_dynamo_resource):
        mock_table = mock_dynamo_resource.return_value.Table.return_value
        sample_data = {
            "launch_id": "5eb87cd9ffd86e000604b32a",
            "order_id": "5eb87cd9ffd86e000604b32a_",
            "mission_name": "FalconSat",
            "rocket_id": "5e9d0d95eda69955f709d1eb",
            "launch_date": "2006-03-24T22:30:00.000Z",
            "status": "FAILED",
            "launchpad": "5e9e4502f5090995de566f86"
        }
        save_launch_to_dynamodb(sample_data, mock_table)
        mock_table.put_item.assert_called_once_with(Item=sample_data)

if __name__ == "__main__":
    unittest.main()
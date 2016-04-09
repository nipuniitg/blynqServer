
class TestDataClass:
    data = {
        'message': 'Hi, this is from test File'
    }

    def getScreenTestData(self):
        screens = [
            {
                "screenName": "Screen1",
                "description": "This is the first screen"
            },
            {
                "screenName": "Screen2",
                "description": "This is the second screen"
            }
        ]
        return screens

    def getGroupsTestData(self):
        groups = [
             {"groupId": 1, "groupName": "Shopping Mall", "Description": "This is for the group Description"},
             {"groupId": 2, "groupName": "supermarket",   "Description": "This is for the group Description"},
             {"groupId": 3, "groupName": "cinimax",       "Description": "This is for the group Description"},
             {"groupId": 4, "groupName": "sports corner", "Description": "This is for the group Description"},
             {"groupId": 5, "groupName": "top floor",     "Description": "This is for the group Description"},
             {"groupId": 6, "groupName": "Entrance",      "Description":"This is for the group Description"},
             {"groupId": 7, "groupName": "sports center", "Description": "This is for the group Description"},
             {"groupId": 0, "groupName": "topfloor",      "Description": "This is for the group Description"}
        ];
        return groups
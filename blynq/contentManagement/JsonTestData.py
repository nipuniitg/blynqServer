
class TestDataClass:
    def getContentTestData(self):
        content={
            'folders': [
                {'folderName': 'Folder 1', 'folderId': '1', 'parentFolderId': -1},
                {'folderName': 'Folder 2', 'folderId': '2', 'parentFolderId': -1},
            ],
            'items': [
                {'itemId': 1, 'itemName': 'image 1', 'url':'/static/images/nba.jpg', 'contentType': 'image', 'resolution':'42*34'},
                {'itemId': 2, 'ItemName': 'image 2', 'url':'/static/images/nba.jpg', 'contentType': 'video', 'resolution':'32*56'},
            ]
        }
        return content
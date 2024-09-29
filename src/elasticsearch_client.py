import json
import requests
from config.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_INDEX

class ElasticsearchClient:
    def __init__(self):
        self.url = f"{ELASTICSEARCH_HOST}/{ELASTICSEARCH_INDEX}/_bulk"

    def bulk_insert(self, documents):
        bulk_data = ""
        for doc in documents:
            bulk_data += json.dumps({"index": {"_index": ELASTICSEARCH_INDEX}}) + "\n"
            bulk_data += json.dumps(doc) + "\n"
        
        headers = {'Content-Type': 'application/x-ndjson'}
        response = requests.post(self.url, data=bulk_data, headers=headers)
        return response.status_code, response.text

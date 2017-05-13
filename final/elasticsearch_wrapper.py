import json, requests

from six.moves import configparser

class ElasticsearchWrapper:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.end_point = config.get('Elasticsearch', 'end_point')
        self.index = config.get('Elasticsearch', 'index')
        self.mapping_type = config.get('Elasticsearch', 'mapping_type')        
        self.address = 'http://%s/%s/%s' % (self.end_point, self.index, self.mapping_type)

    def create_index(self):
        data = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            },
            "mappings": {
                self.mapping_type: {
                    "properties": {
                        "name": { "type" : "text" },
                        "time": { "type": "date", "format": "yyyy/MM/dd HH:mm:ss"},
                        "location": { "type": "geo_point"},
                        "text": { "type": "text"},
                        "profile_image_url": { "type": "text" },
                        "sentiment": { "type": "text" }
                    }
                }
            }
        }
        print (data)
        response = requests.put(self.address, data=json.dumps(data))
        return response.text

    def upload(self, data):
        print ('uploading to databse...')
        upload_address = '%s/_bulk' % (self.address)
        response = requests.put(upload_address, data=data)
        print ('upload success')
        # return response

   

es = ElasticsearchWrapper()
res = es.create_index()
print res
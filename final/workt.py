#in charge of sending josn to es
#!/usr/bin/env python
import json, requests

from six.moves import configparser

end_point = 'search-jacketsu-4pm2nv7dseksmqm2v4edzc2xxe.us-east-1.es.amazonaws.com'
index = 'twitter'
mapping_type = 'tweet'  
address = 'http://%s/%s/%s' % (end_point, index, mapping_type)


class ElasticsearchWrapper:
    
    def create_index(self):
        data = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            },
            "mappings": {
                mapping_type: {
                    "properties": {
                        "Index": { "type" : "text" },
                        "LastTradeWithCurrency": { "type": "long"},
                        "LastTradeDateTime": { "type": "date"},
                        "LastTradePrice": { "type": "double"},
                        "LastTradeTime": { "type": "date"},
                        "StockSymbol": { "type": "text" },
                        "ID": { "type": "text" }
                    }
                }
            }
        }
        #print (data)
        response = requests.post(address, data=json.dumps(data))
        return response.text

    def upload(data1):
        print ('uploading to databse...')
        #upload_address = '%s/_bulk' % (self.address)
        #response = requests.put(upload_address, data=data)
        response = requests.post(address, data1)
        print ('upload success')
        # return response

    def search(self,keyword):
         data = {
             "size": 2000,
             "query": {
                 "query_string": { "query": keyword }
             }
         }
         search_address = '%s/_search' % (address)
         response = requests.post(search_address, data=json.dumps(data))

         return response.json()

    def printa(self,searchkey):
        resultjson=self.search(searchkey)
        output= json.dumps(resultjson)
    # print output
        modefied_json=resultjson['hits']['hits']
        print json.dumps(modefied_json)

        with open('%s_tweet.json'%searchkey, 'w') as f:
            json.dump(modefied_json, f)

















if __name__ == '__main__':

    es = ElasticsearchWrapper()
    #res = es.create_index()
    #print res
    
    es.printa('AAPL')
    es.printa('GOOGL')
    es.printa('FB')
    es.printa('AMZN')
    es.printa('LNKD')
    es.printa('MSFT')
    es.printa('TSLA')

import json, requests

from six.moves import configparser

end_point = ''
index = 'stock'
mapping_type = 'price'  
address = 'http://%s/%s/%s' % (end_point, index, mapping_type)

class ElasticsearchStock:
    
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

        response = requests.post(address, data=json.dumps(data))
        return response.text

    def upload(data1):
        print ('uploading to databse...')
        response = requests.post(address, data1)
        print ('upload success')

    def search_stock(self, keyword):
         data = {
             "size": 2000,

             "query": {
                 "query_string": { "query": keyword }
             },
             "sort": { "LastTradeDateTime": { "order": "desc" }}
             
    
         }
         search_address = '%s/_search' % (address)
         response = requests.post(search_address, data=json.dumps(data))

         return response.json()

    def printa(self,searchkey):
        resultjson=self.search(searchkey)
        output= json.dumps(resultjson)
        print (output)
        modefied_json=resultjson['hits']['hits']

        with open('%s.json'%searchkey, 'w') as f:
            json.dump(modefied_json, f)


if __name__ == '__main__':

    es = ElasticsearchStock()
    
    es.printa('AAPL')
    es.printa('GOOGL')
    es.printa('FB')
    es.printa('AMZN')
    es.printa('LNKD')
    es.printa('MSFT')
    es.printa('TSLA')

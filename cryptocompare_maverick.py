import urllib.request
import urllib.parse
import gzip
import json
import datetime as dt
import time

PRODUCTION_URL = 'https://www.cryptocompare.com/api/data%s'
PRODUCTION_URL_MIN = 'https://min-api.cryptocompare.com/data%s'

class HTTPClient:
    def __init__(self, endpoint, headers = dict(), params = dict()):
        self.url = endpoint
        self.params = params
        self.headers = headers

    def perform(self):
        resource = self.url

        if self.params:
            query_string = urllib.parse.urlencode(self.params)
            resource = '%s&%s' % (self.url, query_string)

        request = urllib.request.Request(resource, headers=self.headers)
        handler = urllib.request.urlopen(request)
        raw_response = handler.read()

        if 'Accept-Encoding' in self.headers:
            if self.headers['Accept-Encoding'] == 'deflat, gzip':
                raw_response = gzip.decompress(raw_response)

        encoding = handler.info().get_content_charset('utf-8')
        response = json.loads(raw_response.decode(encoding))
        return response


# meta data and fundamentals
class MetadataListCoinsRequest:
    def endpoint(self):
        return PRODUCTION_URL % '/coinlist/'

class CoinSnapshotRequest:
    def __init__(self,
                 from_symbol,
                 to_symbol = 'USD',
                 query_parameters = dict()):
        self.fsym = from_symbol
        self.tsym = to_symbol
    
    def endpoint(self):
        return PRODUCTION_URL %'/coinsnapshot/?fsym=%s&tsym=%s' % (
            self.fsym,
            self.tsym)

# current price
class SpecificRateRequest:
    def __init__(self,
                 from_symbol,
                 to_symbols = 'USD,ETH,BTC',
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        self.fsym = from_symbol
        self.tsyms = to_symbols
        self.e = exchanges
        self.query_parameters = query_parameters

    def endpoint(self):
        return PRODUCTION_URL_MIN %'/price?fsym=%s&tsyms=%s&e=%s' % (
            self.fsym,
            self.tsyms,
            self.e)

class MultiRateRequest:
    def __init__(self, 
                 from_symbols,
                 to_symbols = 'USD,ETH,BTC',
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        self.fsyms = from_symbols
        self.tsyms = to_symbols
        self.e = exchanges
        self.query_parameters = query_parameters

    def endpoint(self):
        return PRODUCTION_URL_MIN %'/pricemulti?fsyms=%s&tsyms=%s&e=%s' % (
            self.fsyms,
            self.tsyms,
            self.e)

class DayAveRequest:
    def __init__(self,
                 from_symbol,
                 to_symbol = 'USD',
                 exchanges = 'CCCAGG',
                 ave_type = 'HourVWAP',
                 hour_diff_utc = 0 ,
                 query_parameters = dict()):
        self.fsym = from_symbol
        self.tsym = to_symbol
        self.e = exchanges
        self.avgType = ave_type
        self.UTCHourDiff = hour_diff_utc
        self.query_parameters = query_parameters

    def endpoint(self):
        return PRODUCTION_URL_MIN %'/dayAvg?fsym=%s&tsym=%s&UTCHourDiff=%d&avgType=%s&e=%s' % (
            self.fsym,
            self.tsym,
            self.UTCHourDiff,
            self.avgType,
            self.e)


# historical prices
class HistoMntRequest:
    def __init__(self,
                 from_symbol,
                 to_symbol = 'USD',
                 limit = 300 ,
                 end_time = dt.datetime.now(),
                 agg = 5,
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        self.fsym = from_symbol
        self.tsym = to_symbol
        self.limit = limit               
        self.toTs = int(time.mktime(end_time.timetuple()))
        self.e = exchanges
        self.aggregate = agg
        self.query_parameters = query_parameters

    def endpoint(self):
        return PRODUCTION_URL_MIN %'/histominute?fsym=%s&tsym=%s&limit=%d&toTs=%d&aggregate=%d&e=%s' % (
            self.fsym,
            self.tsym,
            self.limit,
            self.toTs,
            self.aggregate,
            self.e)
        
class HistoHourRequest:
    def __init__(self,
                 from_symbol,
                 to_symbol = 'USD',
                 start_time = dt.datetime.today() + dt.timedelta(hours = -48),
                 end_time = dt.datetime.today(),
                 agg = 1,
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        self.fsym = from_symbol
        self.tsym = to_symbol
        self.limit = int((end_time - start_time).days * 24)               
        self.toTs = int(time.mktime(end_time.timetuple()))
        self.e = exchanges
        self.aggregate = agg
        self.query_parameters = query_parameters

    def endpoint(self):
        return PRODUCTION_URL_MIN %'/histohour?fsym=%s&tsym=%s&limit=%d&toTs=%d&aggregate=%d&e=%s' % (
            self.fsym,
            self.tsym,
            self.limit,
            self.toTs,
            self.aggregate,
            self.e)

class HistoDayRequest:
    def __init__(self,
                 from_symbol,
                 to_symbol = 'USD',
                 start_time = dt.datetime.today() + dt.timedelta(hours = -48),
                 end_time = dt.datetime.today(),
                 agg = 1,
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        self.fsym = from_symbol
        self.tsym = to_symbol
        self.limit = int((end_time - start_time).days )               
        self.toTs = int(time.mktime(end_time.timetuple()))
        self.e = exchanges
        self.aggregate = agg
        self.query_parameters = query_parameters

    def endpoint(self):
        return PRODUCTION_URL_MIN %'/histoday?fsym=%s&tsym=%s&limit=%d&toTs=%d&aggregate=%d&e=%s' % (
            self.fsym,
            self.tsym,
            self.limit,
            self.toTs,
            self.aggregate,
            self.e)        

class HistoDayFullRequest:
    def __init__(self,
                 from_symbol,
                 to_symbol = 'USD',
                 agg = 1,
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        self.fsym = from_symbol
        self.tsym = to_symbol
        self.e = exchanges
        self.aggregate = agg
        self.query_parameters = query_parameters

    def endpoint(self):
        return PRODUCTION_URL_MIN %'/histoday?fsym=%s&tsym=%s&allData=true&aggregate=%d&e=%s' % (
            self.fsym,
            self.tsym,
            self.aggregate,
            self.e)        
        
class CryptocompareMaverick:
    DEFAULT_HEADERS = {
        'Accept': 'application/json'
    }
    def __init__(self, client_class=HTTPClient):
#        self.api_key = api_key
#        header_apikey = {'cryptocompare-API-Key': self.api_key}
#        self.headers = {**self.DEFAULT_HEADERS, **headers, **header_apikey}
        self.client_class = client_class

#    def with_header(self, header, value):
#        old_headers = self.headers
#        new_header = {header: value}
#        return CoinAPIv1(self.api_key, {**old_headers, **new_header})

    def getMetadataListCoins(self):
        request = MetadataListCoinsRequest()
        client = self.client_class(request.endpoint())
        response = client.perform()
        message ={ (key): (value if key != 'Data' else len(value) ) for key, value in response.items() }
        data = response['Data']
        return message, data


    def getCoinSnapshot(self, 
                        from_symbol,
                        to_symbol = 'USD', 
                        query_parameters = dict()):
        
        request = CoinSnapshotRequest(from_symbol, 
                                      to_symbol = to_symbol, 
                                       query_parameters = query_parameters)

        client = self.client_class(request.endpoint())
        response = client.perform()
        message ={ (key): (value if key != 'Data' else len(value) ) for key, value in response.items() }
        data = response['Data']
        return message, data

    def getSpecificRate(self,
                 from_symbol,
                 to_symbols = 'USD,ETH,BTC',
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        request = SpecificRateRequest(from_symbol, 
                                       to_symbols = to_symbols,
                                       exchanges = exchanges,
                                       query_parameters = query_parameters)
        client = self.client_class(request.endpoint())
        response = client.perform()
        return response

    def getMultiRate(self,
                 from_symbols,
                 to_symbols = 'USD,ETH,BTC',
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        request = MultiRateRequest(from_symbols, 
                                       to_symbols = to_symbols,
                                       exchanges = exchanges,
                                       query_parameters = query_parameters)
        client = self.client_class(request.endpoint())
        data = client.perform()
        return data

    def getDayAve(self,
                 from_symbol,
                 to_symbol = 'ETH',
                 exchanges = 'CCCAGG',
                 ave_type = 'HourVWAP',
                 hour_diff_utc = 0,
                 query_parameters = dict()):
        request = DayAveRequest(from_symbol, 
                               to_symbol = to_symbol,
                               exchanges = exchanges,
                               ave_type = ave_type ,
                               hour_diff_utc = hour_diff_utc ,
                               query_parameters = query_parameters)
        client = self.client_class(request.endpoint())
        data = client.perform()
        return data

    def getHistoMnt(self,
                 from_symbol,
                 to_symbol = 'ETH',
                 limit = 300 , 
                 end_time = dt.datetime.now() ,
                 agg = 5 ,
                 exchanges = 'CCCAGG' ,
                 query_parameters = dict()):
        request = HistoMntRequest(from_symbol, 
                               to_symbol = to_symbol,
                               limit = limit ,
                               end_time = end_time ,
                               agg = agg ,
                               exchanges = exchanges,
                               query_parameters = query_parameters)
        client = self.client_class(request.endpoint())
        response = client.perform()
        message = { (key): (value if key != 'Data' else len(value) ) for key, value in response.items() }
        data = response['Data']
        return message, data
    
    def getHistoHour(self,
                 from_symbol,
                 to_symbol = 'ETH',
                 end_time = dt.datetime.today() ,
                 agg = 1,
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        request = HistoHourRequest(from_symbol, 
                               to_symbol = to_symbol,
                               start_time = start_time ,
                               end_time = end_time ,
                               agg = agg ,
                               exchanges = exchanges,
                               query_parameters = query_parameters)
        client = self.client_class(request.endpoint())
        response = client.perform()
        message = { (key): (value if key != 'Data' else len(value) ) for key, value in response.items() }
        data = response['Data']
        return message, data
    
    def getHistoDay(self,
                 from_symbol,
                 to_symbol = 'ETH',
                 start_time = dt.datetime.today() + dt.timedelta(hours = -48) ,
                 end_time = dt.datetime.today() ,
                 agg = 1,
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        
        request = HistoDayRequest(from_symbol, 
                               to_symbol = to_symbol,
                               start_time = start_time ,
                               end_time = end_time ,
                               agg = agg ,
                               exchanges = exchanges,
                               query_parameters = query_parameters)
        
        client = self.client_class(request.endpoint())
        response = client.perform()
        message = { (key): (value if key != 'Data' else len(value) ) for key, value in response.items() }
        data = response['Data']
        return message, data

    def getHistoDayFull(self,
                 from_symbol,
                 to_symbol = 'ETH',
                 agg = 1,
                 exchanges = 'CCCAGG',
                 query_parameters = dict()):
        
        request = HistoDayFullRequest(from_symbol, 
                               to_symbol = to_symbol,
                               agg = agg ,
                               exchanges = exchanges,
                               query_parameters = query_parameters)
        
        client = self.client_class(request.endpoint())
        response = client.perform()
        message = { (key): (value if key != 'Data' else len(value) ) for key, value in response.items() }
        data = response['Data']
        return message, data










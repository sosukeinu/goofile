import http.client
import logging
import re
import sys

import requests


class TailCaller(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        ret = self.f(*args, **kwargs)
        while type(ret) is TailCall:
            ret = ret.handle()
        return ret

class TailCall(object):
    def __init__(self, call, *args, **kwargs):
        self.call = call
        self.args = args
        self.kwargs = kwargs

    def handle(self):
        if type(self.call) is TailCaller:
            return self.call.f(*self.args, **self.kwargs)
        else:
            return self.call(*self.args, **self.kwargs)

class GooSearch:
    def __init__(self, domain=None, filetype=None, key=None, engine=None, limit=100, query='', log='INFO'):
        self.domain = domain
        self.filetype = filetype
        self.key = key
        self.engine = engine
        self.limit = limit
        self.query = query
        self.results = []
        self.temp_results = []
        self.log = log
        self.init_logging()

    def init_logging(self):
        """Set logging handlers, and create the logs/ directory and file if it doesn't exist.

        :param name: log file name (without the trailing .log).
        :return: None.
        """
        logging.getLogger().handlers = []
        logger = logging.getLogger()
        shandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        shandler.setFormatter(formatter)
        shandler.setLevel(getattr(logging, self.log))
        logger.addHandler(shandler)
        logger.setLevel(getattr(logging, self.log))

    def build_query_string(self, **kwargs):
        s = "https://www.googleapis.com/customsearch/v1?"
        if getattr(self, 'domain', None):
            if s.endswith('?'):
                s = '{0}siteSearch={1}'.format(s, self.domain)
            else:
                s = '{0}&siteSearch={1}'.format(s, self.domain)
        if getattr(self, 'filetype', None):
            if s.endswith('?'):
                s = '{0}fileType={1}'.format(s, self.filetype)
            else:
                s = '{0}&fileType={1}'.format(s, self.filetype)
        if getattr(self, 'key', None):
            if s.endswith('?'):
                s = '{0}key={1}'.format(s, self.key)
            else:
                s = '{0}&key={1}'.format(s, self.key)
        if getattr(self, 'engine', None):
            if s.endswith('?'):
                s = '{0}cx={1}'.format(s, self.engine)
            else:
                s = '{0}&cx={1}'.format(s, self.engine)
        if getattr(self, 'query', None):
            if s.endswith('?'):
                s = '{0}q={1}'.format(s, self.query)
            else:
                s = '{0}&q={1}'.format(s, self.query)
        else:
            if s.endswith('?'):
                s = '{0}q='''.format(s)
            else:
                s = '{0}&q='''.format(s)
        if kwargs.get('start', None):
            if s.endswith('?'):
                s = '{0}start={1}'.format(s, kwargs.get('start', 1))
            else:
                s = '{0}&start={1}'.format(s, kwargs.get('start', 1))
        return s

    def run_basic(self):
        h = http.client.HTTPSConnection('www.google.com')
        headers = {'Host': 'www.google.com', 'User-agent': 'Internet Explorer 6.0 ', 'Referrer': 'www.g13net.com'}
        h.request('GET', "/search?num=500&q=site:" + getattr(self, 'domain', None) + "+filetype:" + getattr(self, 'filetype', None), headers=headers)
        response = h.getresponse()
        status = response.status
        reason = response.reason
        if status == 200:
            data = response.read()
            try:
                data = data.decode('utf-8')
            except UnicodeDecodeError:
                data = data.decode('latin-1')
            data = re.sub('<b>', '', data)
            for e in ('>', '=', '<', '\\', '(', ')', '"', 'http', ':', '//'):
                data = data.replace(e, ' ')
            r1 = re.compile('[-_.a-zA-Z0-9.-_]*' + '\.' + getattr(self, 'filetype', None))
            res = r1.findall(data)
        elif status == 302:
            print('Your request returned a {0} status. Reason: {1}'.format(status, reason))
            print('This usually happens because Google flagged your network for suspicious activity.')
            sys.exit()
        else:
            print('Your request returned a {0} status. Reason: {1}'.format(status, reason))
            sys.exit()
        return res

    @TailCaller
    def run_api(self, **kwargs):
        start_index = kwargs.get('start', 1)
        logging.debug('start_index: {0}'.format(start_index))
        start = None
        search_string = self.build_query_string(start=start_index)
        logging.debug('search string: {0}'.format(search_string))
        r = requests.get(search_string)
        if r.status_code == 200:
            parsed_json = r.json()
            items = parsed_json.get('items', None)
            queries = parsed_json.get('queries', None)
            next = queries.get('nextPage', None)
            if next:
                start = next[0]['startIndex']
            logging.debug('start: {0}'.format(start))
            request = queries.get('request', None)
            count = request[0]['count']
            res = getattr(self, 'temp_results', [])
            logging.debug('temp_results: {0}'.format(res))
            logging.debug('count: {0}'.format(count))
            if items:
                for x in items:
                    logging.debug('item link: {0}'.format(x['link']))
                    if res:
                        res.append(x['link'])
                    else:
                        res = [x['link']]
            if count < 10:
                setattr(self, 'results', res)
                return self.results
            else:
                start_index = start
                setattr(self, 'temp_results', res)
                return TailCall(self.run_api, self, start=start_index)
        else:
            setattr(self, 'results', getattr(self, 'temp_results', []))
            print('The last request resulted in an error code {0}'.format(r.status_code))
            return self.results

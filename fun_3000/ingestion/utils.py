import urllib2


def get_unicode_response(url):
    '''
    Do an HTTP GET, figure out the charset and convert to unicode
    :param url: Web URL where HTTP GET will be submitted
    :return: Unicode string
    '''
    try:
        query_response = urllib2.urlopen(url)
        query_response_content = query_response.read()
        encoding = query_response.headers['content-type'].split('charset=')[-1]
        unicode_response = unicode(query_response_content, encoding)
    except:
        #bad status line error ... can't fix it
        unicode_response = ''

    return unicode_response
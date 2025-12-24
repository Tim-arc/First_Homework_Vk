def application(environ, start_response):
    status = '200 OK'
    
    response_headers = [
        ('Content-type', 'text/plain; charset=utf-8'),
    ]
    
    query_string = environ.get('QUERY_STRING', '')
    
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
        
    request_body = environ['wsgi.input'].read(request_body_size)
    
    output = [
        f"Hello World!\n".encode('utf-8'),
        f"GET parameters: {query_string}\n".encode('utf-8'),
        f"POST parameters: {request_body.decode('utf-8')}\n".encode('utf-8')
    ]
    
    start_response(status, response_headers)
    return output
import ssl

def create_server_context():
    # Retourne un objet SSLContext 
    server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    server_context.minimum_version = ssl.TLSVersion.TLSv1_3
    server_context.maximum_version = ssl.TLSVersion.TLSv1_3
    server_context.verify_mode = ssl.CERT_NONE
    
    server_context.load_cert_chain('certificates/server/server.crt', 'certificates/server/server.key')
    return server_context

def create_client_context():
    # Retourne un objet SSLContext 
    client_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    
    client_context.minimum_version = ssl.TLSVersion.TLSv1_3
    client_context.maximum_version = ssl.TLSVersion.TLSv1_3
    client_context.check_hostname = True
    
    client_context.load_verify_locations('certificates/ca/ca.crt')
    return client_context

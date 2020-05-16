# How to push data real time and update charts

1. Websocket
2. Plotly

### Generate .pem file for SSL

But the following one cannot be used on localhost:

    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.pem -out localhost.pem

### Generate self-certified Certificate
    
Rreate domains.ext

    authorityKeyIdentifier=keyid,issuer
    basicConstraints=CA:FALSE
    keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
    subjectAltName = @alt_names
    [alt_names]
    DNS.1 = localhost

Run the following commands:

    openssl req -x509 -nodes -new -sha256 -days 1024 -newkey rsa:2048 -keyout RootCA.key -out RootCA.pem -subj "/C=US/CN=Example-Root-CA"
    openssl x509 -outform pem -in RootCA.pem -out RootCA.crt

    openssl req -new -nodes -newkey rsa:2048 -keyout localhost.key -out localhost.csr -subj "/C=US/ST=TX/L=Frisco/O=Example-Certificates/CN=localhost.local"
    openssl x509 -req -sha256 -days 1024 -in localhost.csr -CA RootCA.pem -CAkey RootCA.key -CAcreateserial -extfile domains.ext -out localhost.crt

    localhost.crt is the certificate
    
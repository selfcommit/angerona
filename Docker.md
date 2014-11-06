Docker instructions for Angerona
--------------------------------

- CID=$(docker run -dP petergrace/angerona)
- docker port $CID 443
- open browser to port shown by docker port command

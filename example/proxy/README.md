### Running this example:
install traefik

run:
```sh
traefik --configFile=traefik.toml
```

or with Dokcer
```sh
docker run -d -p 8080:8080 -p 80:80 \
    -v $PWD/traefik.yml:/etc/traefik/traefik.yml traefik:v2.9
```

then in another shell run:
```sh
uvicorn app:app
```

alternatively, delete `root_path="/api"` from `app.py` and run:
```sh
uvicorn app:app --root-path /api
```

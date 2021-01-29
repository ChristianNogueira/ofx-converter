## OFX Converter

Creates OFX required by [Contabilizei](https://www.contabilizei.com.br/) to upload account balance.

Currently, converts xlsx provided by [Neon Pejota](https://neon.com.br/pejota)

You can run from [Docker Hub](https://hub.docker.com/repository/docker/chris3669/ofx-converter/general) as temporary container as:
```bash
docker container run --rm --name ofx -p 8080:8080 chris3669/ofx-converter:1.0.0
```
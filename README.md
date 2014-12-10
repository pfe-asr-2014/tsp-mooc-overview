

Run container:

```sh
# With boot2docker
docker run -it --env HOST_IP=$(ip route|awk '/192/ { print $9 }') debian bash

# Without b2d
docker run -it debian bash
```


config_test containers based on [rockymeza/django-docker-example](https://github.com/rockymeza/django-docker-example)

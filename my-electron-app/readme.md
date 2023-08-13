Docker for electron setup
`https://trigodev.com/blog/develop-electron-in-docker#how`

# Build
``sh
docker build -it electron-app .
``
# Run application
``sh
 docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -v $(pwd):/reference -w /reference electron-app bash
```
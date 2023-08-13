From --platform=arm64 node:18.16.0

RUN apt update && \
 apt install \
 git libx11-xcb1 libxcb-dri3-0 libxtst6 libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm-dev dbus \
    -yq --no-install-suggests --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .
RUN useradd -d /app electron
RUN chown -R electron /app

USER electron

RUN npm install
RUN npx electron-rebuild

USER root
RUN chown root /app/node_modules/electron/dist/chrome-sandbox
RUN chmod 4755 /app/node_modules/electron/dist/chrome-sandbox

USER electron

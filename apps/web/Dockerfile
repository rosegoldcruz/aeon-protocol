FROM node:20-alpine
WORKDIR /app

# Install deps
COPY apps/web/package.json /app/apps/web/package.json
RUN cd /app/apps/web && npm install --legacy-peer-deps

# Copy source
COPY apps/web /app/apps/web

EXPOSE 3000
CMD ["npm", "run", "dev", "--prefix", "/app/apps/web"]


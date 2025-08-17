# apps/web/Dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml* package-lock.json* yarn.lock* ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
RUN npm run build --workspace apps/web

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
COPY --from=builder /app/apps/web/.next /app/apps/web/.next
COPY --from=builder /app/apps/web/public /app/apps/web/public
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/apps/web/package.json /app/apps/web/package.json
EXPOSE 3000
CMD ["npm","run","start","--prefix","/app/apps/web"]

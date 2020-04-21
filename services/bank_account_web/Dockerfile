FROM node:latest as builder

WORKDIR /app

COPY . .
RUN npm install
RUN npm run build --prod

FROM node:alpine

RUN mkdir -p /app

WORKDIR /app

COPY --from=builder /app/dist/bank-account-web /app

RUN npm install -g serve

CMD ["serve", "-s", "/app"]

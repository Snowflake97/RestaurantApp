FROM node:16.13.1-alpine

WORKDIR /frontend

COPY package.json  package-lock.json ./

RUN npm i --silent
RUN npm i react-scripts@4.0.3 -g

COPY src/ ./src/
COPY public/ ./public/

EXPOSE 3000


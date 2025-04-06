FROM node:18 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine

# On copie notre config nginx custom
COPY nginx.conf /etc/nginx/nginx.conf

# On copie le build React
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

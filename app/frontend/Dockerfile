FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install
# RUN npx update-browserslist-db@latest || true

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
FROM node:20-bullseye-slim

WORKDIR /frontend

COPY . .

RUN npm install

RUN npm install file-saver --save

RUN npm install classnames

EXPOSE 3000

CMD ["npm", "start"]
from node:17

WORKDIR /agent
COPY package.json main.js ./
RUN npm install

EXPOSE 3000
CMD ["node", "main.js"]
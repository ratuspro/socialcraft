from node:17-alpine
LABEL socialcraft_agent=''

WORKDIR /agent
COPY package.json socialcraft.js ./
RUN npm install

EXPOSE 3000
CMD ["node", "main.js"]
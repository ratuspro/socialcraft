from nikolaik/python-nodejs:python3.10-nodejs16-alpine
LABEL socialcraft_agent=''

# Add Mineflayer modules
WORKDIR /agent
RUN npm install mineflayer mineflayer-pathfinder mineflayer-statemachine minecraft-data vec3 dotenv

COPY socialcraft_handler.js/ ./socialcraft_handler.js

# Run Agent
EXPOSE 3000
CMD ["node", "main.js"]
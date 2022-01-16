from nikolaik/python-nodejs:python3.10-nodejs16-slim
LABEL socialcraft_agent=''

# Add Mineflayer modules
WORKDIR /agent
COPY package.json ./
RUN npm install

# Add javascript module to python
RUN pip install javascript

# Run Agent
EXPOSE 3000
CMD ["python", "main.py"]
FROM apify/actor-node:22
COPY package*.json ./
RUN npm ci --omit=dev --ignore-scripts
COPY src ./src
COPY catalog/memefx.json ./catalog/memefx.json
CMD ["npm", "start"]

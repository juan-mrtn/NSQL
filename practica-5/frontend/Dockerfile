FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Expose port for dev server
EXPOSE 5173

# Run vite dev server
CMD ["npm", "run", "dev", "--", "--host"]

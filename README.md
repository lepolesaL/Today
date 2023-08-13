# TODAY - Task Management Application

## Prerequisites

- Docker and Docker Compose installed on your system
- Node.js and npm (for local development)

## Deployment with Docker Compose

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a `.env` file in the root directory and add necessary environment variables:
   ```
   MONGODB_URL=mongodb://admin:admin@mongodb:27017
   ```

3. Build and start the containers:
   ```sh
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

5. To stop the application:
   ```sh
   docker-compose down
   ```

## Local Development

### Frontend

1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Start the development server:
   ```sh
   export NODE_OPTIONS=--openssl-legacy-provider
   npm start
   ```

4. Open http://localhost:3000 in your browser.

### Backend

1. Navigate to the backend directory:
   ```sh
   cd backend
   ```

2. Install dependencies (preferably in a virtual environment):
   ```sh
   pip install -r requirements.txt
   ```

3. Start the development server:
   ```sh
   uvicorn main:app --reload --host=0.0.0.0
   ```

## Electron App Development

To develop the Electron app using Docker:

1. Build the Docker image:
   ```sh
   docker build -t electron-app .
   ```

2. Run the application:
   ```sh
   docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -v $(pwd):/reference -w /reference electron-app bash
   ```

## Infrastructure as Code (Pulumi)

To deploy the infrastructure using Pulumi:

1. Set up your AWS credentials in `~/.aws/credentials`.

2. Export your Pulumi access token:
   ```sh
   export PULUMI_ACCESS_TOKEN=<your-pulumi-access-token>
   ```

3. Run the Pulumi command:
   ```sh
   docker run -it -v ~/.aws:/root/.aws:ro -e AWS_PROFILE=lp -e PULUMI_ACCESS_TOKEN=${PULUMI_ACCESS_TOKEN} -v $(pwd):/pulumi -w /pulumi/iac pulumi/pulumi up --stack dev
   ```

## Additional Information

For more details on React and Create React App, refer to the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).
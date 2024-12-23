
# **DevOps Machine Learning Project**

This project demonstrates a DevOps workflow to deploy a Flask application using Docker, GitLab CI/CD, and GitLab's Container Registry. The application leverages a pre-trained machine learning model to identify flowers.

-----

## **Getting Started**

### **1. Clone the Repository**
Clone the repository and navigate to the project directory:
```bash
git clone https://gitlab.com/hamzamejri/devops-machineL-project.git
cd devops-machineL-project
```

### **2. Setup the Project Locally**

#### **Install Docker and Docker Compose**
- Install Docker on your machine.
- Verify the installation:
  ```bash
  docker --version
  docker-compose --version
  ```
- Start Docker.

#### **Run the Application Locally**
- Build and start the application:
  ```bash
  docker-compose up --build
  ```
- Access the application at [http://localhost:5000](http://localhost:5000).

---

## **Configure GitLab CI/CD Pipeline**

### **1. Enable the GitLab Container Registry**
- Go to your project in GitLab.
- Navigate to **Settings > General > Visibility, project features, permissions**.
- Enable the **Container Registry** feature.

### **2. Set Up CI/CD Variables**
Add the following variables in **Settings > CI/CD > Variables**:

| Variable Name          | Value                  | Description                                       |
|------------------------|------------------------|---------------------------------------------------|
| `CI_REGISTRY_USER`     | `<Your GitLab Username>` | Your GitLab username, e.g., `alaajaghmoun`.        |
| `CI_REGISTRY_PASSWORD` | `<Personal Access Token>`| A token with `read_registry` and `write_registry` scopes. |
| `CI_REGISTRY`          | `registry.gitlab.com`   | The URL of GitLab’s Container Registry.          |

### **3. Generate a Personal Access Token**
- Go to **GitLab Personal Access Tokens**.
- Create a new token with:
  - **Name**: Container Registry Token
  - **Scopes**: Select `read_registry` and `write_registry`
- Copy the token and set it as the value of `CI_REGISTRY_PASSWORD` in your CI/CD variables.

---

## **Handling Docker Authentication Conflicts**
If the pipeline fails due to a conflict in the Docker credentials configuration:
1. Open your Docker `config.json` file (e.g., `~/.docker/config.json` or `C:\Users\<username>\.docker\config.json`).
2. Remove or comment out the `"credsStore": "desktop"` line.
3. Reauthenticate with Docker:
   ```bash
   docker login
   ```
4. This will regenerate the `auth` token in the `config.json` file, resolving credential conflicts.

---

## **CI/CD Pipeline Configuration**

The `.gitlab-ci.yml` file defines the pipeline with the following stages:

| Stage     | Description                                                   |
|-----------|---------------------------------------------------------------|
| **Build** | Builds the Docker image and pushes it to the GitLab Container Registry. |
| **Test**  | Pulls the Docker image and tests the application.             |
| **Deploy**| Pulls the Docker image and runs the application.              |

## **Runner Configuration**
1. make sure you are using this configuration for your runner so it can work perfectly with your enviroment
```bash
concurrent = 1
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "My-Local-Runner"
  url = "https://gitlab.com"
  token = "Your Token"
   executor = "docker"
  [runners.docker]
    tls_verify = false
    image = "docker:latest"
    privileged = true
    volumes = ["/var/run/docker.sock:/var/run/docker.sock","/c/Users/your_username/.docker/config.json:/root/.docker/config.json"]
    shm_size = 0
```
2. On the deployment script, make sure to add the local tag in theh script and inside gitlab under Settings -> CI/CD -> Runners
3. Head to C:/Gitlab-Runner and open cmd and type ```bash
   gitlab-runner.exe run
   ```

### **CI/CD Workflow**
1. On every commit, the pipeline is triggered automatically.
2. The pipeline builds, tests, and deploys the Dockerized application.
3. Deployment exposes the application on [http://localhost:5000](http://localhost:5000).

---

## **Manual Deployment Steps**

If you prefer to deploy the application manually:

1. **Build the Docker Image**:
   ```bash
   docker build -t devops-ml-app .
   ```
2. **Run the Application**:
   ```bash
   docker run -d -p 5000:5000 --name devops-ml-app devops-ml-app
   ```
3. Access the application at [http://localhost:5000](http://localhost:5000).

---

## **Troubleshooting**

### **1. Unauthorized Access to GitLab Container Registry**
- Verify that `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD`, and `CI_REGISTRY` are set correctly in CI/CD variables.
- Ensure `CI_REGISTRY_PASSWORD` is a valid Personal Access Token with `read_registry` and `write_registry` scopes.

### **2. Pipeline Fails During Docker Login**
- If the pipeline fails during `docker login`, reauthenticate locally:
  ```bash
  docker login
  ```
- Remove stale credentials from the Docker configuration (`~/.docker/config.json`) as described earlier.

### **3. Application Fails to Start**
- Check the Docker container logs:
  ```bash
  docker logs devops-ml-app
  ```
---

## **Technologies Used**

- **Flask**: Python-based web framework.
- **Docker**: Containerization tool for building and deploying the application.
- **GitLab CI/CD**: Automates the build, test, and deployment process.
- **GitLab Container Registry**: Stores and manages Docker images.

---

## **Next Steps**

1. Optimize the pipeline for faster builds.
2. Add additional tests to validate application behavior.
3. Implement a monitoring solution for the deployed application.

---

## **License**

This project is licensed under the Tekup License.

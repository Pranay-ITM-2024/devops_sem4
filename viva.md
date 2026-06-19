# 🎓 DevOps Viva Preparation Guide

This guide contains the most frequently asked questions during a DevOps practical viva or interview. The answers are tailored specifically to the **SOC Automation Platform** you just built.

---

## 🏗️ 1. General Architecture & DevOps

**Q: What is DevOps, and how does your project demonstrate it?**
> **Answer:** DevOps is a culture and set of practices that combines software development (Dev) and IT operations (Ops) to shorten the development lifecycle and provide continuous delivery. My project demonstrates this by completely automating the build, test, infrastructure provisioning, and deployment of a Python-based SOC dashboard using tools like Jenkins, Terraform, and Kubernetes.

**Q: What is the difference between monolithic and microservices architecture? Which one is your app?**
> **Answer:** A monolith bundles everything (UI, logic, database) into one large program. Microservices split the app into small, independent pieces that communicate over APIs. My app uses a **Microservices** approach: the UI (Flask) and the Backend API (FastAPI) are separate services, running in different containers, communicating over HTTP.

---
 
## ☁️ 2. AWS Cloud Architecture

**Q: If you deployed this to AWS, what services would you use and what would the architecture look like?**
> **Answer:** In a production AWS environment, the architecture maps like this:
> 1. **Compute (Kubernetes):** I would use **Amazon EKS (Elastic Kubernetes Service)** to host the Flask and FastAPI containers, managed by auto-scaling node groups.
> 2. **Database:** Instead of running PostgreSQL in a container, I would use **Amazon RDS for PostgreSQL**. It provides automated backups, Multi-AZ high availability, and easier scaling.
> 3. **Container Registry:** I would push my Docker images to **Amazon ECR (Elastic Container Registry)** instead of DockerHub.
> 4. **Networking:** The cluster would sit inside a custom **VPC**, with public subnets for an **Application Load Balancer (ALB)** and private subnets for the EKS worker nodes and RDS database.
> 5. **CI/CD:** Jenkins can run on an EC2 instance, pulling code from GitHub, building images, and pushing them to ECR before updating EKS.

**Q: How did you configure the cloud infrastructure?**
> **Answer:** I used **Terraform** as Infrastructure-as-Code (IaC). Instead of clicking manually in the AWS Console, I wrote `.tf` files defining the VPC, subnets, and EKS clusters. Running `terraform apply` talks to the AWS API to provision exactly what is in the code.

---

## 🐳 3. Containerization (Docker)

**Q: Why did you use Docker? What problem does it solve?**
> **Answer:** Docker eliminates the "it works on my machine" problem. By packaging the Python code, the dependencies (`requirements.txt`), and the runtime environment into a container, I ensured that the application runs identically on my laptop, the testing server, and the production Kubernetes cluster.

**Q: Explain your Dockerfile. What is a multi-stage build?**
> **Answer:** My Dockerfile uses a multi-stage build. In the first stage (builder), it installs all the Python dependencies. In the second stage, it only copies the installed dependencies and the application code. This makes the final Docker image much smaller and more secure because it leaves behind cache files and build tools that attackers could exploit.

---

## ☸️ 4. Orchestration (Kubernetes)

**Q: Why do you need Kubernetes if you already have Docker?**
> **Answer:** Docker only runs containers on a single machine. Kubernetes is an orchestrator that manages thousands of containers across many machines. It handles load balancing, auto-scaling, auto-healing (restarting crashed containers), and rolling updates without downtime.

**Q: How does your application handle traffic spikes?**
> **Answer:** I implemented a **Horizontal Pod Autoscaler (HPA)**. It monitors the CPU usage of the FastAPI backend. If the CPU hits 70%, the HPA automatically scales the deployment from 2 pods up to 5 pods to handle the load, and scales back down when traffic drops.

---

## 🔄 5. CI/CD (Jenkins)

**Q: Walk me through your Jenkins Pipeline.**
> **Answer:** My Jenkinsfile defines several stages:
> 1. **Clone:** Fetches code from GitHub.
> 2. **Test:** Runs unit/E2E tests using `pytest` and `jest`.
> 3. **Security Scan:** Runs `bandit` to check the Python code for vulnerabilities.
> 4. **Build:** Creates the Docker images.
> 5. **Deploy:** Uses `kubectl set image` to update the Kubernetes cluster with the new Docker image without causing downtime.

---

## 📈 6. Monitoring & Logging (Prometheus & ELK)

**Q: How do you monitor the health of this application?**
> **Answer:** I use **Prometheus** to scrape metrics from my servers and Kubernetes pods (like CPU usage, memory, HTTP request rates). I use **Grafana** to connect to Prometheus and display those metrics in visual, real-time dashboards so analysts can see the system's health at a glance.

**Q: Why do you need Elasticsearch and Kibana (ELK) if you have Prometheus?**
> **Answer:** Prometheus is for **metrics** (numbers, like "CPU is at 80%"). ELK is for **logs** (text, like "User 'admin' failed to login at 2:00 PM"). Elasticsearch stores massive amounts of text logs from all my microservices in one central place, and Kibana is the search engine UI to dig through them when debugging an error.

---

## 💻 7. Core Commands Cheat Sheet (What they actually do)

During the viva, if they ask "What command do you use to do X?", use this reference:

### Docker Commands
* `docker compose up -d --build`  
  * **What it does:** Reads the `docker-compose.yml` file, builds the images from your Dockerfiles (`--build`), starts all the containers (Flask, FastAPI, DB), and runs them in the background detached (`-d`).
* `docker compose ps`  
  * **What it does:** Lists all currently running containers in your project so you can verify they are online.
* `docker compose down`  
  * **What it does:** Stops all containers and deletes them cleanly, freeing up your computer's memory.

### Kubernetes Commands
* `kubectl apply -f folder_name/`  
  * **What it does:** Reads all the `.yaml` files in the folder and tells Kubernetes to create those resources (Deployments, Services, Secrets) in the cluster exactly as written.
* `kubectl get pods -n soc-app`  
  * **What it does:** Lists all the running containers (Pods) inside the specific "soc-app" namespace to see if they are running or crashing.
* `kubectl rollout undo deployment/fastapi-backend -n soc-app`  
  * **What it does:** If a bad update was deployed, this instantly rolls the application back to the previous working version with zero downtime.

### Terraform Commands
* `terraform init`  
  * **What it does:** Downloads the necessary plugins (like the AWS or Docker provider) so Terraform knows how to talk to the cloud.
* `terraform plan`  
  * **What it does:** Shows a "dry run" of exactly what infrastructure Terraform is *going* to create or delete, before it actually does it.
* `terraform apply`  
  * **What it does:** Actually executes the plan and provisions the servers, databases, or networks in the cloud.

### Jenkins Commands (Inside Jenkinsfile)
* `kubectl set image deployment/fastapi-backend fastapi=yourimage:v2`
  * **What it does:** This is the CD (Continuous Deployment) command. It tells Kubernetes to swap out the old version of your code with the newly built Docker image tag, triggering a rolling update.

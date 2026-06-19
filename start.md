# 🚀 How to Start and Use Your SOC App

This guide is written in simple, plain English to help you start your app on your computer, test it out, and show it off for your exam!

---

## 🟢 Part 1: How to Start the App (The DevOps Way)

The most impressive way to start the whole platform (the dashboard, the API, the simulator, and the database) for your exam is to use **Terraform**. This shows you know Infrastructure-as-Code (IaC)!

### Step 1: Open your Terminal
Open the Terminal app on your Mac and go to the project's terraform folder:
```bash
cd ~/Desktop/DEVOPS/terraform
```

### Step 2: Start everything with Terraform
Run these commands to provision your local infrastructure:
```bash
terraform init
terraform apply -auto-approve
```
* **What this does:** Terraform reads your modular configuration (network and compute modules), provisions a custom Docker network, and securely deploys your database, backend, dashboard, and simulator as containers.
* **Wait a minute:** It might take a few seconds to start up. If it's your first time, it might download the Postgres image.

*(Note: If you just want a quick start without Terraform, you can still run `docker-compose up -d --build` from the `~/Desktop/DEVOPS` folder instead!)*

### Step 3: Check if it's running
Run this command to see your containers:
```bash
docker compose ps
```
You should see `soc_api`, `soc_dashboard`, `soc_db`, and `soc_simulator` running.

---

## 👀 Part 2: How to Use the App

Now that it's running, let's open it in your web browser!

### 1. View the Analyst Dashboard (Flask)
* **Open your browser and go to:** [http://localhost:5001](http://localhost:5001)
* **What you'll see:** A dark-themed web page showing statistics (Total Alerts, Open, Closed) and a table of security alerts.
* **Why this is cool:** The "Alert Simulator" we built is secretly running in the background. Every 30 seconds, it pretends to be a hacker and sends a fake alert (like "Brute Force" or "Malware") to your dashboard. Refresh the page after a minute to watch the list grow!

### 2. Triage an Alert
* On the dashboard, click the blue **title** of any alert to open its Details page.
* On the right side, you'll see **Triage Actions**. 
* Click the **Acknowledge** button (yellow). It updates the status to "In Progress".
* Click the **Close** button (green) when you are done.

### 3. Run a Security Playbook
* On that same details page, look at the bottom right for **Run Playbook**.
* Click **Block IP** or **Isolate Host**.
* A green success message will pop up! You just "automated" a security response.
* Go to the top menu and click **Playbook Logs** to see a history of all the buttons you clicked.

### 4. View the Backend API (FastAPI)
* **Open your browser and go to:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **What you'll see:** The Swagger UI. This is an interactive page where developers can test your API.
* **Why this is cool:** It proves to your exam grader that you built a proper, modern REST API. You can click on the `GET /api/alerts` box, click "Try it out", and click "Execute" to see the raw data.

---

## 🛑 Part 3: How to Stop the App

When you are finished testing and want to close the app so it stops using your computer's memory:

1. Go back to your Terminal.
2. Make sure you are in the `~/Desktop/DEVOPS/terraform` folder.
3. Run this command:
```bash
terraform destroy -auto-approve
```
* **What this does:** Terraform will look at the current state and cleanly destroy the network and containers it created.

*(If you used Docker Compose earlier, run `docker compose down` from the `~/Desktop/DEVOPS` folder instead.)*

---

## ☸️ Part 4: How to start it with Kubernetes (For the Exam Demo)

When you are ready to demonstrate the advanced DevOps stuff (Kubernetes), make sure Docker is stopped first (`docker compose down`).

Then, use Minikube:

```bash
# 1. Turn on Minikube
minikube start --cpus=4 --memory=8192
# 2. Tell Kubernetes to start our app
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/app/secrets.yaml
kubectl apply -f k8s/app/configmap.yaml
kubectl apply -f k8s/database/
kubectl apply -f k8s/app/
kubectl apply -f k8s/simulator/

# 3. Wait a minute for the pods to wake up, then check on them:
kubectl get pods -n soc-app

# 4. Ask Minikube to open the dashboard in your browser!
minikube service flask-service -n soc-app
```

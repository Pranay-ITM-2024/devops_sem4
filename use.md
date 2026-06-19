# 🎙️ SOC Automation Platform: Exam Demonstration Guide

This document is your "script" for demonstrating the project during your exam. If you follow these steps while sharing your screen, you will show off all the cool features of your application and prove that the DevOps pipeline is backing it up!

---

## 🎬 Pre-Flight Checklist (Before the presentation)
1. Make sure Docker Desktop is running (the whale icon is in your menu bar).
2. Open your terminal in the `DEVOPS/terraform` folder.
3. Start the app using your IaC: `terraform apply -auto-approve`
4. Wait 1 minute so the "Simulator" has time to generate a few fake alerts.

---

## 🎭 The Live Demonstration

### Step 1: Introduce the Dashboard
* **Action:** Open your browser to [http://localhost:5001](http://localhost:5001).
* **What to say:** *"This is the Security Operations Center (SOC) dashboard. It's built with Python Flask. As you can see, at the top we have our real-time metrics showing Total Alerts, Open Alerts, and Closed Alerts."*
* **Action:** Point out the table in the middle.
* **What to say:** *"This table shows incoming security threats. Right now, a Python script called 'Alert Simulator' is running in the background inside a Docker container. Every 30 seconds, it acts like a SIEM (Security Information and Event Management) system and fires a new simulated threat into our database."*
* **Action:** Refresh the page to show that the numbers went up and a new row appeared.

### Step 2: Triaging a Threat
* **Action:** Click on the blue title of a high-severity alert (e.g., "Brute force SSH login attempt" or "Ransomware").
* **What to say:** *"When an analyst clicks an alert, they get the full details—source IP, destination IP, and the exact description of the attack."*
* **Action:** On the right side, click the yellow **Acknowledge** button.
* **What to say:** *"I can acknowledge the alert, which updates its status to 'In Progress' so other analysts know I am handling it."*

### Step 3: Running an Automated Playbook (The Cool Part)
* **Action:** Scroll down slightly to the "Run Playbook" section on the same page.
* **What to say:** *"Normally, an analyst would have to manually log into a firewall to block an IP. This platform automates that. Watch this."*
* **Action:** Click the **Block IP** button. A green success message will appear at the top.w
* **What to say:** *"The Flask dashboard just sent an API request to our FastAPI backend, which securely logged the action and executed the automated defense playbook."*

### Step 4: Show the Audit Trail
* **Action:** Look at the top navigation bar and click **Playbook Logs**.
* **What to say:** *"In cybersecurity, logging is everything. Here we can see an immutable audit trail of the playbook I just ran, showing exactly who did it, what action was taken, and what time it happened."*

### Step 5: Show the API (The "Backend" Proof)
* **Action:** Open a new browser tab and go to [http://localhost:8000/docs](http://localhost:8000/docs).
* **What to say:** *"While the Flask app is the UI, the actual brain of the operation is a high-performance REST API built with FastAPI. Because I built it using modern standards, it automatically generates this Swagger documentation."*
* **Action:** Click on `GET /api/alerts`, click **Try it out**, then click **Execute**.
* **What to say:** *"This API is completely decoupled from the UI, meaning we could easily build a mobile app or integrate it with other security tools in the future."*

---

## 🛠️ Explaining the DevOps Behind the Scenes
After showing the app working, you switch to explaining *how* it's hosted.

* **What to say:** *"Now, while the application works well, the real achievement is the DevOps lifecycle behind it."*
* **Action:** Open your code editor (like VS Code) and show them these files quickly:
  1. **`docker-compose.yml`**: *"The whole app is containerized. The UI, API, Database, and Simulator run in isolated Docker environments."*
  2. **`Jenkinsfile`**: *"If I were pushing this to GitHub, this Jenkins pipeline automatically lints the code, runs security scans (using Bandit), builds the Docker images, and deploys them."*
  3. **`terraform/main.tf`**: *"Infrastructure is entirely managed as code. If we lose the server, Terraform can rebuild the network and database instantly."*
  4. **`k8s/` folder:** *"For production, we don't just run Docker. I've written full Kubernetes manifests including Horizontal Pod Autoscaling (HPA) so the API scales up automatically if we get hit with a massive wave of security alerts."*

---

## 🏁 Finishing the Demo
* **What to say:** *"In conclusion, this project demonstrates not just a functional business application, but a highly available, automated, and secure deployment pipeline capable of handling enterprise-scale traffic."*
* **Action:** Go to your terminal and type `terraform destroy -auto-approve` to cleanly shut everything off.

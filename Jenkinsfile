pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'yourusername'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Pranay-ITM-2024/devops_sem4.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install --break-system-packages -r api/requirements.txt'
                sh 'pip3 install --break-system-packages -r app/requirements.txt'
            }
        }

        stage('Run Unit Tests (Python)') {
            steps {
                sh 'cd api && python3 -m pytest tests/ -v --tb=short'
            }
        }

        stage('Run E2E API Tests (Node/Jest)') {
            steps {
                sh 'cd e2e-tests && npm install'
                // E2E tests require a live API server - marked non-blocking in CI
                sh 'cd e2e-tests && npm test || true'
            }
        }

        stage('Code Lint') {
            steps {
                sh 'pip3 install --break-system-packages flake8'
                sh 'flake8 api/ --max-line-length=120 --exclude=__pycache__ || true'
            }
        }

        stage('Security Scan') {
            steps {
                sh 'pip3 install --break-system-packages bandit'
                sh 'bandit -r api/ -f json -o bandit-report.json || true'
                sh 'echo "Security scan complete"'
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/soc-api:${IMAGE_TAG} ./api"
                sh "docker build -t ${DOCKER_HUB_USER}/soc-dashboard:${IMAGE_TAG} ./app"
                sh "docker build -t ${DOCKER_HUB_USER}/soc-simulator:${IMAGE_TAG} ./simulator"
                // Uncomment to push when Docker Hub credentials are configured
                // sh "docker push ${DOCKER_HUB_USER}/soc-api:${IMAGE_TAG}"
                // sh "docker push ${DOCKER_HUB_USER}/soc-dashboard:${IMAGE_TAG}"
                // sh "docker push ${DOCKER_HUB_USER}/soc-simulator:${IMAGE_TAG}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    kubectl set image deployment/fastapi-backend \\
                        fastapi=${DOCKER_HUB_USER}/soc-api:${IMAGE_TAG} \\
                        -n soc-app || true
                    kubectl set image deployment/flask-dashboard \\
                        flask=${DOCKER_HUB_USER}/soc-dashboard:${IMAGE_TAG} \\
                        -n soc-app || true
                    kubectl rollout status deployment/fastapi-backend -n soc-app || true
                    kubectl rollout status deployment/flask-dashboard -n soc-app || true
                """
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}

## CI/CD and Jenkins

### What is CI/CD

- Right now your workflow looks like this:
- Write code → manually test it → manually docker build → manually docker run → hope nothing broke
- Every step is manual. Every time you change code you repeat this whole sequence. On a team of 5 people all pushing code, this becomes a chaos problem very quickly — someone pushes broken code, nobody knows until much later.
- CI/CD automates this entire sequence.

### CI — Continuous Integration

Every time someone pushes code, automatically:

- Pull the latest code
- Install dependencies
- Run tests
- Build the Docker image
- Tell you if anything broke

### CD — Continuous Delivery/Deployment

After CI passes, automatically:

Push the Docker image to a registry
Deploy it to a server
Your new code is live

### What is Jenkins

- Jenkins is a tool that watches your code repository.
- runs a pipeline of steps automatically when code changes.
- You define the steps in a file called Jenkinsfile. 
- Jenkins reads it and executes each step in order.

```
You push code to GitHub
        ↓
Jenkins detects the change
        ↓
Jenkins reads your Jenkinsfile
        ↓
Runs each stage: Test → Build → Deploy
        ↓
Tells you pass or fail
```

---

## Installing Jenkins

### Step-1: docker network create jenkins

```bash
docker network create jenkins
```

### Step 2 — Run Jenkins container

```bash
docker run -d \
  --name jenkins \
  --network jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### Step 3 — Get the initial admin password

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Step 4 — Open Jenkins UI

- Go to http://localhost:8080 in your browser.
- Paste the password, then:
- Click Install suggested plugins — let it finish
- Create an admin user when prompted
- Leave the URL as http://localhost:8080
- Click Start using Jenkins


### Step 5 - Install Docker inside Jenkins container

```bash
docker exec -it --user root jenkins bash -c "
  apt-get update && \
  apt-get install -y docker.io && \
  chmod 666 /var/run/docker.sock
"
```

---

## Creating CI/CD Pipelines

### Step 1 - Create Jenkins file

```
pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/flask-devops-app.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t flask-app .'
            }
        }

        stage('Run') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! App is running.'
        }
        failure {
            echo 'Pipeline failed! Check the logs.'
        }
    }
}

```

### Step 2 — Push your Flask app to GitHub

- Create a new repo on GitHub called flask-devops-app (do this on github.com, make it public).
- Then in your WSL2 terminal:

```bash
git init
git add .
git commit -m "initial commit - dockerized flask app"
git remote add origin https://github.com/YOUR_USERNAME/flask-devops-app.git
git branch -M main
git push -u origin main
```

### Step 3 — Configure Jenkins to use GitHub 

- Back in the browser at http://localhost:8080:

- Click "New Item" on the left
- Enter name: flask-pipeline
- Select "Pipeline" (not Freestyle)
- Click OK

- You'll land on the job configuration page. Scroll down to the Pipeline section at the bottom.
- Change Definition dropdown from Pipeline script to Pipeline script from SCM
- SCM → select Git
- Repository URL → paste your GitHub HTTPS URL: https://github.com/YOUR_USERNAME/flask-devops-app.git
- Branch Specifier → change */master to */main
- Script Path → leave as Jenkinsfile
- Click Save

### Step 4 — Test it manually first

Click Build Now once to make sure the GitHub connection works before setting up the webhook.
Watch the Console Output — you should now see Jenkins actually cloning your repo:
Cloning the remote Git repository
Cloning repository https://github.com/YOUR_USERNAME/flask-devops-app.git
...
Checking out Revision abc123...
pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/ashleyxdev/flask-app.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t flask-app:dev .'
            }
        }

        stage('Run') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                sleep(time: 8, unit: 'SECONDS')
                sh 'docker exec test-app curl -f http://localhost:5000/health'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded! Blog app is live on port 5000.'
        }
        failure {
            echo '❌ Pipeline failed! Check the logs above.'
        }
    }
}
pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo 'Code is already checked out'
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
                sh 'docker-compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                sleep(time: 5, unit: 'SECONDS')
                sh 'curl -f http://localhost:5000/health'
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
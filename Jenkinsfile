pipeline {
    agent any

    stages {
        stage('Test Docker Access') {
            steps {
                sh 'docker ps'
            }
        }

        stage('Build backend image') {
            steps {
                sh 'docker-compose build backend'
            }
        }

        stage('Run backend tests') {
            steps {
                sh 'docker-compose run --rm backend pytest'
            }
        }

        stage('Build frontend image') {
            steps {
                sh 'docker-compose build frontend'
            }
        }

        stage('Deploy full stack with Docker Compose') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            sh 'docker-compose down'
        }
    }
}

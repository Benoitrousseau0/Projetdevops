pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "projetdevops"
    }

    stages {
        stage('Checkout code') {
            steps {
                git 'https://github.com/Benoitrousseau0/Projetdevops.git'
            }
        }

        stage('Build backend image') {
            steps {
                dir('backend') {
                    sh 'docker build -t backend-image .'
                }
            }
        }

        stage('Run backend tests') {
            steps {
                sh 'docker run --rm backend-image pytest'
            }
        }

        stage('Build frontend image') {
            steps {
                dir('frontend') {
                    sh 'docker build -t frontend-image .'
                }
            }
        }

        stage('Deploy full stack with Docker Compose') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
    }
}

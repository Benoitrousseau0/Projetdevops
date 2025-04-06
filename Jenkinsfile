pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "projetdevops"
    }

    options {
        checkoutToSubdirectory('projet')
    }

    stages {
        stage('Checkout code') {
            steps {
                dir('projet') {
                    git branch: 'main', url: 'https://github.com/Benoitrousseau0/Projetdevops.git'
                }
            }
        }

        stage('Setup environment') {
            steps {
                dir('projet/backend') {
                    echo '📁 Création du fichier .env à partir de .env.example.'
                    bat 'copy .env.example .env'
                }
            }
        }

        stage('Build & Start Backend + DB') {
            steps {
                dir('projet') {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'docker-hub-credentials',
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {
                        bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                    }
                    bat 'docker-compose up -d --build db backend'
                }
            }
        }

        stage('Run backend tests') {
            steps {
                dir('projet') {
                    // Attend quelques secondes pour que backend soit prêt (attente du wait-for-it.sh dans le Dockerfile)
                    bat 'docker-compose exec backend pytest'
                }
            }
        }

        stage('Build frontend') {
            steps {
                dir('projet') {
                    bat 'docker-compose build frontend'
                }
            }
        }

        stage('Full stack deployment') {
            steps {
                dir('projet') {
                    bat 'docker-compose down'
                    bat 'docker-compose up -d --build'
                }
            }
        }
    }
}

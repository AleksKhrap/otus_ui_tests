pipeline {
    agent any

    parameters {
        string(
            name: 'EXECUTOR',
            defaultValue: 'selenoid',
            description: 'Адрес Selenoid'
        )
        string(
            name: 'APP_URL',
            defaultValue: 'http://prestashop:80',
            description: 'Адрес приложения PrestaShop'
        )
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Браузер'
        )
        string(
            name: 'BROWSER_VERSION',
            defaultValue: 'default',
            description: 'Версия браузера'
        )
        string(
            name: 'THREADS',
            defaultValue: '1',
            description: 'Количество потоков'
        )
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare workspace') {
            steps {
                sh '''
                    rm -rf allure-results || true
                    mkdir -p allure-results
                    chmod -R 777 allure-results
                    ls -la allure-results/
                '''
            }
        }

        stage('Build test image') {
            steps {
                sh """
                    docker build -t prestashop-tests:latest .
                """
            }
        }

        stage('Run tests') {
            steps {
                script {
                    def containerName = "test-${BUILD_NUMBER}-${env.BUILD_ID}"
                    def exitCode = 0

                    try {
                        sh """
                            docker run --name ${containerName} \\
                                --network selenoid \\
                                ${imageName} \\
                                --browser=${params.BROWSER} \\
                                --headless=true \\
                                --url=${params.APP_URL} \\
                                --executor=${params.EXECUTOR} \\
                                --browser_version=${params.BROWSER_VERSION} \\
                                -n ${params.THREADS}
                        """
                    } catch (Exception e) {
                        exitCode = 1
                    } finally {
                        sh """
                            docker cp ${containerName}:/app/allure-results/. ./allure-results/ 2>/dev/null || true
                            docker rm -f ${containerName} 2>/dev/null || true
                            ls -la ./allure-results || true
                        """
                    }

                    if (exitCode != 0) {
                        error("Tests failed")
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                allure includeProperties: false,
                       report: 'allure-report',
                       results: [[path: 'allure-results']]
            }
        }
    }
}
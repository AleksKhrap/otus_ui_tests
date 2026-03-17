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
                sh """
                    docker run --name ${containerName} \\
                        --network selenoid \\
                        prestashop-tests:latest \\
                        --browser=${params.BROWSER} \\
                        --headless=true \\
                        --url=${params.APP_URL} \\
                        --executor=${params.EXECUTOR} \\
                        --browser_version=${params.BROWSER_VERSION} \\
                        -n ${params.THREADS} || true

                    docker cp ${containerName}:/app/allure-results/. ./allure-results/ 2>&1 || true
                    docker rm -f ${containerName} || true
                """
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
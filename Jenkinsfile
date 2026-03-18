pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_SCOPE',
            choices: ['all', 'ui', 'api'],
            description: 'Вид тестов'
        )
        string(
            name: 'API_URL',
            defaultValue: 'https://restful-booker.herokuapp.com',
            description: 'Адрес API Restful-booker'
        )
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
                script {
                    imageName = "prestashop-tests:latest"
                    sh "docker build -t ${imageName} ."
                }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    def exitCode = 0

                    if (params.TEST_SCOPE in ['api', 'all']) {
                        def apiContainer = "api-test-${BUILD_NUMBER}-${env.BUILD_ID}"
                        try {
                            sh """
                                docker run --name ${apiContainer} \\
                                    --network selenoid \\
                                    -e TEST_SCOPE=${params.TEST_SCOPE}
                                    ${imageName} \\
                                    --api-url=${params.API_URL} \\
                                    -n ${params.THREADS}
                            """
                        } catch (Exception e) {
                            exitCode = 1
                        } finally {
                            sh """
                                docker cp ${apiContainer}:/app/allure-results/. ./allure-results/ 2>/dev/null || true
                                docker rm -f ${apiContainer} 2>/dev/null || true
                            """
                        }
                    }

                    if (params.TEST_SCOPE in ['ui', 'all']) {
                        def uiContainer = "ui-test-${BUILD_NUMBER}-${env.BUILD_ID}"
                        try {
                            sh """
                                docker run --name ${uiContainer} \\
                                    --network selenoid \\
                                    -e TEST_SCOPE=${params.TEST_SCOPE}
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
                                docker cp ${uiContainer}:/app/allure-results/. ./allure-results/ 2>/dev/null || true
                                docker rm -f ${uiContainer} 2>/dev/null || true

                                ls -la ./allure-results || true
                            """
                        }
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
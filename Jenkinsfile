pipeline {
    agent any
    
    parameters {
        choice(name: 'BROWSER', choices: ['both', 'chrome', 'firefox'], description: 'Browser to run tests on')
        choice(name: 'MARKER', choices: ['full', 'smoke', 'regression'], description: 'Test marker to run')
        string(name: 'WORKERS', defaultValue: 'auto', description: 'Number of parallel workers')
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    
    environment {
        ALLURE_SERVER_URL = 'http://allure:5050'
        SHORT_TIMEOUT = '3'
        LONG_TIMEOUT = '10'
        VIDEO_RECORDING = 'True'
        PYTHONUNBUFFERED = '1'
    }
    
    stages {
        stage('Run Tests') {
            steps {
                script {
                    def browsers = params.BROWSER == 'both' ? ['chrome', 'firefox'] : [params.BROWSER]
                    
                    parallel browsers.collectEntries { browser -> 
                        [(browser): {
                            sh """
                                export BROWSER=${browser}
                                
                                # Clean previous results directory
                                rm -rf allure-results-${browser}
                                mkdir -p allure-results-${browser}
                                
                                . /opt/venv/bin/activate
                                xvfb-run -a -s "-screen 0 1920x1080x24" \
                                    pytest \
                                    -n ${params.WORKERS} --dist=loadfile \
                                    --alluredir=allure-results-${browser} \
                                    --html=report-${browser}.html \
                                    --self-contained-html \
                                    -m ${params.MARKER} || true
                            """
                        }]
                    }
                }
            }
        }
        
        stage('Upload Reports') {
            steps {
                script {
                    def browsers = params.BROWSER == 'both' ? ['chrome', 'firefox'] : [params.BROWSER]
                    
                    browsers.each { browser ->
                        uploadToAllure(browser)
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo "✓ Tests passed and report uploaded to Allure Docker Service!"
            echo "View reports: http://localhost:8080/"
        }
        failure {
            echo "✗ Tests failed. Check reports for details."
        }
    }
}

def uploadToAllure(browser) {
    def projectId = "selenium-tests-${browser}"
    def projectName = browser == 'chrome' ? 'Selenium Tests - Chrome' : 'Selenium Tests - Firefox'
    def allureUrl = env.ALLURE_SERVER_URL
    def resultsDir = "allure-results-${browser}"
    
    sh """#!/bin/bash
        set -e
        
        # Check if results directory exists and has JSON files
        if [ ! -d "${resultsDir}" ] || [ -z "\$(find ${resultsDir} -type f -name '*.json' | head -1)" ]; then
            echo "No Allure result files found in ${resultsDir}. Skipping upload."
            exit 0
        fi
        
        # Create or verify project exists
        echo "Creating/verifying project: ${projectName}..."
        curl -X POST "${allureUrl}/allure-docker-service/projects" \
            -H "Content-Type: application/json" \
            -d '{"id":"${projectId}","name":"${projectName}"}' \
            -s || echo "Project may already exist, continuing..."
        
        # Rename result.json only if filename UUID != JSON UUID
        RESULT_FILE=\$(find ${resultsDir} -name "*-result.json" | head -1)
        if [ -n "\$RESULT_FILE" ]; then
            UUID=\$(grep '"uuid"' "\$RESULT_FILE" | sed 's/.*"uuid": "\\([^"]*\\)".*/\\1/')
            FILENAME_UUID=\$(basename "\$RESULT_FILE" | sed 's/-result.json//')
            if [ -n "\$UUID" ] && [ "\$FILENAME_UUID" != "\$UUID" ]; then
                mv "\$RESULT_FILE" "${resultsDir}/\$UUID-result.json"
            fi
        fi
        
        # Send results files - separate find commands
        FILES_TO_SEND=\$(
            find "${resultsDir}" -type f -name '*.json';
            find "${resultsDir}" -type f -name '*.png';
            find "${resultsDir}" -type f -name '*.txt';
            find "${resultsDir}" -type f -name '*.properties'
        )
         FILES_TO_SEND=\$(echo "\$FILES_TO_SEND" | tr '\\n' ' ')
        
        if [ -z "\$FILES_TO_SEND" ]; then
            echo "No files to send. Skipping upload."
            exit 0
        fi

        FILES=''
        for FILE in \$FILES_TO_SEND; do
            FILES="\$FILES -F files[]=@\$FILE"
        done

        echo "Uploading ${browser} results to Allure Docker Service..."
        RESPONSE=\$(curl -X POST \
            -H 'Content-Type: multipart/form-data' \
            \$FILES \
            -L \
            -w "\\nHTTP Status: %{http_code}\\n" \
            -s \
            "${allureUrl}/allure-docker-service/send-results?project_id=${projectId}")
        
        # echo "\$RESPONSE"
        HTTP_CODE=\$(echo "\$RESPONSE" | tail -n 1 | grep -oP '\\d+')
        if [ "\$HTTP_CODE" = "200" ]; then
            echo "✓ ${browser} report uploaded successfully!"
            echo "View report at: http://localhost:5050/allure-docker-service/projects/${projectId}/reports/latest/index.html"
        else
            echo "✗ Upload failed with status: \$HTTP_CODE"
            echo "Full response: \$RESPONSE"
            exit 1
        fi
    """
}
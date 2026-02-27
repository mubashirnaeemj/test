pipeline {
    agent any

    triggers {
        githubPush() // triggers build on GitHub push
    }

    stages {
        stage('Clone / Update Repo') {
            steps {
                deleteDir()
                git branch: 'main',
                    url: 'https://github.com/mubashirnaeemj/test.git'
            }
        }

        stage('Generate Diff') {
            steps {
                script {
                    def prevCommit = sh(script: "git rev-parse HEAD~1", returnStdout: true).trim()
                    echo "Previous commit: ${prevCommit}"

                    sh "git --no-pager diff ${prevCommit} HEAD > changes.diff"
                    sh "cat changes.diff"
                }
            }
        }

        stage('Archive Diff') {
            steps {
                archiveArtifacts artifacts: 'changes.diff', allowEmptyArchive: true
            }
        }

        stage('Send Diff to FastAPI') {
            steps {
                script {
                    def commitId = sh(script: "git rev-parse HEAD", returnStdout: true).trim()
                    def diffContent = sh(script: "cat changes.diff | sed 's/\"/\\\\\"/g' | sed ':a;N;\$!ba;s/\\n/\\\\n/g'", returnStdout: true).trim()

                    // Send diff JSON to FastAPI backend
                    sh """
                    curl -X POST http://127.0.0.1:8000/jenkins/diff \\
                         -H 'Content-Type: application/json' \\
                         -d '{ "commit_id": "${commitId}", "diff": "${diffContent}" }'
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}

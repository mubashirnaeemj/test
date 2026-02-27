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
                    // Get previous commit
                    def prevCommit = sh(script: "git rev-parse HEAD~1", returnStdout: true).trim()
                    echo "Previous commit: ${prevCommit}"

                    // Generate diff file
                    sh "git --no-pager diff ${prevCommit} HEAD > changes.diff"

                    // Print diff in Jenkins console
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
                    def diffContent = sh(script: "cat changes.diff | sed 's/\"/\\\\\"/g'", returnStdout: true).trim()

                    sh """
                    curl -X POST http://127.0.0.1:8000/commits/ \\
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

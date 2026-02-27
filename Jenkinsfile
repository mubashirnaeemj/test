pipeline {
    agent any

    triggers {
        // Automatically run when changes are pushed to GitHub
        githubPush()
    }

    stages {
        stage('Clone / Update Repo') {
            steps {
                // Clean workspace and clone repo
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

                    // Save the diff to a file
                    sh "git --no-pager diff ${prevCommit} HEAD > changes.diff"

                    echo "Changes since last commit:"
                    sh "cat changes.diff"
                }
            }
        }

        stage('Archive Diff') {
            steps {
                archiveArtifacts artifacts: 'changes.diff', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}

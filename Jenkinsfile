pipeline {
    agent any

    triggers {
        githubPush()
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
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}

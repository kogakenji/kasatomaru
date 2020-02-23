pipeline {
	agent any
	stages {
		stage('Checkout') {
			steps {
				echo 'Checkout...'
				sh 'env'
				checkout scm
				￿￿//stash 'sources'
			}
		}
		stage('Build') {
			steps {
				echo 'Build...'

				//unstash 'sources'
				sh 'python hello.py'
				stash 'sources'
				sh 'export BUILD_STATUS=success'
			}
		}
	}
	post {
		//always, changed, fixed, regression, aborted, success, unsuccessful, unstable, failure, notBuilt, cleanup
        always {
            echo 'I will always say Hello again!'
        }
    }
}

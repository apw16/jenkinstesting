pipeline {
    agent { docker { image 'maven:3.3.3' } }

  //check every minute for changes
  triggers {
    pollSCM('*/1 * * * *')
  }
  
    stages {
        stage('build') {
            steps {
                sh 'mvn --version'
            }
        }
		
        stage('test') {
            steps {
                sh 'mvn --version'
            }
        }
		
        stage('deploy') {
            steps {
                sh 'mvn --version'
            }
        }
    }
}
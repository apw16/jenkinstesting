pipeline {
  agent none

  //check every minute for changes
  triggers {
    pollSCM('*/1 * * * *')
  }

  stages {
    //Build goes here
stage('Build') {
  agent {
    kubernetes {
      label 'jenkinsrun'
      defaultContainer 'builder'
      yaml """
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: builder
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
      - name: docker-config
        mountPath: /kaniko/.docker
  volumes:
    - name: docker-config
      configMap:
        name: docker-config
"""
    }
  }

  steps {
      script {
        //write the version number to a file which gets copied into the container
        sh 'echo $BUILD_ID > VERSION.txt'
        sh "/kaniko/executor --dockerfile `pwd`/Dockerfile --context `pwd` --destination=853908049944.dkr.ecr.eu-west-1.amazonaws.com/adrian-whittle/app:${env.BUILD_ID}"
    } //container
  } //steps
} //stage(build)

    //Test goes here
    //Test goes here
stage('Test') {
  parallel {

    stage('Static Analysis') {
      //Run this code within our container for this build
      agent {
        kubernetes {
          label 'jenkins-lint'
          defaultContainer 'appy'
          // aws registry
          containerTemplate(name: 'appy', image: "853908049944.dkr.ecr.eu-west-1.amazonaws.com/adrian-whittle/app:${env.BUILD_ID}", ttyEnabled: true, command: 'cat')

          // nexus local registry
          //containerTemplate(name: 'appy', image: "docker.docap.com/app:${env.BUILD_ID}", ttyEnabled: true, command: 'cat', imagePullSecrets: ["docker-docap-key"], alwaysPullImage: false)
        }
      }

      //Run pylint on app.py
      steps {
        sh 'pylint app.py'
      }
    } //stage(static analysis)

    //Functional testing goes here
    stage('Functional Tests') {
  //Run this code within our container for this build
  agent {
    kubernetes {
      label 'jenkins-test'
      defaultContainer 'appy'
      // aws registry
      containerTemplate(name: 'appy', image: "853908049944.dkr.ecr.eu-west-1.amazonaws.com/firstname-lastname/app:${env.BUILD_ID}", ttyEnabled: true, command: 'cat')

      // nexus local registry
      //containerTemplate(name: 'appy', image: "docker.docap.com/app:${env.BUILD_ID}", ttyEnabled: true, command: 'cat', imagePullSecrets: ["docker-docap-key"], alwaysPullImage: false)
    }
  }

  steps {
    sh 'py.test --junitxml results.xml tests.py'
  }

  //Tell Jenkins about the test report
  post {
    always {
      junit '*.xml'
    }
  }
} //stage(functional tests)

    //BDD testing goes here

  } //parallel
} //stage(test)

    //SonarQube goes here

    //Documentation generation goes here

    //Deploy goes here
stage('Deploy') {
  input {
    message "Should we deploy?"
    ok "Yes, please, that'd be really good"
  }
  agent {
    kubernetes {
      label 'jenkins-deploy'
      defaultContainer 'kubectl'
      containerTemplate(name: 'kubectl', image: "lachlanevenson/k8s-kubectl:v1.13.0", ttyEnabled: true, command: 'cat')
    }
  }

  //replace __version__ with the build number and then apply to our cluster
  steps {
    sh "sed s/__VERSION__/${env.BUILD_ID}/g app-deploy.yml | kubectl apply -f -"
  }
}

    //Performance testing goes here
  } //stages
}
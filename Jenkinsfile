pipeline {
    agent { label 'monarch-agent-large' }
        environment {
        HOME = "${env.WORKSPACE}"
        RELEASE = sh(script: "echo `date +%Y-%m-%d`", returnStdout: true).trim()
        PATH = "/opt/poetry/bin:${env.PATH}"
    }
    stages {
        stage('setup') {
            steps {
                sh '''
                    echo "Current directory: $(pwd)"
                    # export PATH=$PATH:$HOME/.local/bin
                    echo "Path: $PATH"
                    
                    # echo $SHELL
                    python3 --version
                    pip --version
                    poetry --version
                  

                    # poetry config experimental.new-installer false
                    poetry install
                    poetry run which ingest
                '''
            }
        }
        stage('download') {
            steps {
                sh '''
                    mkdir data || true
                    gsutil -q -m cp -r gs://monarch-ingest-data-cache/* data/
                    ls -lasdf
                    ls -la data
                '''
            }
        }
        stage('transform') {
            steps {
                sh 'poetry run ingest transform --all --log --rdf'
            }
        }
        stage('merge') {
            steps {
                sh 'poetry run ingest merge'
            }
        }
        stage('kgx-graph-summary') {
            steps {
                sh 'poetry run kgx graph-summary -i tsv -c "tar.gz" --node-facet-properties provided_by --edge-facet-properties provided_by output/monarch-kg.tar.gz -o output/merged_graph_stats.yaml'
            }
        }
        stage('neo4j-v4-transform'){
            steps {
                sh '''
                    docker rm -f neo || True
                    mkdir neo4j-v4-data
                    docker run -d --name neo -p7474:7474 -p7687:7687 -v neo4j-v4-data:/data --env NEO4J_AUTH=neo4j/admin neo4j:4.4
                    poetry run kgx transform --stream --transform-config neo4j-transform.yaml > kgx-transform.log
                    docker stop neo
                    docker run -v $(pwd)/output:/backup -v neo4j-v4-data:/data --entrypoint neo4j-admin neo4j:4.4 dump --to /backup/monarch-kg.neo4j.dump
                '''
            }
        }
        stage('denormalize') {
            steps {
                sh 'poetry run ingest closure'
            }
        }
        stage('solr') {
            steps {
                sh 'poetry run ingest solr'
            }
        }
        stage('sqlite') {
            steps {
                sh 'poetry run ingest sqlite'
            }
        }
        stage('upload files') {
            steps {
                sh 'poetry run ingest release'
            }
        }
        stage('index') {
            steps {
                sh '''
                    echo "Current directory: $(pwd)"
                    python3 --version
                    pip --version
                    export PATH=$HOME/.local/bin:$PATH
                    echo "Path: $PATH"

                    cd $HOME
                    mkdir data-public
                    gcsfuse --implicit-dirs data-public-monarchinitiative data-public

                    git clone https://github.com/monarch-initiative/monarch-file-server.git
                    pip install -r monarch-file-server/scripts/requirements.txt
                    python3 monarch-file-server/scripts/directory_indexer.py --inject monarch-file-server/scripts/directory-index-template.html --directory data-public --prefix https://data.monarchinitiative.org -x
                '''
            }
        }
    }
    post {
        always {
            sh 'docker rm -f neo || true'
        //    sh 'docker rm my_solr || true'
        }
    }
}

desc 'Clean project'
task :clean do
    sh 'find . -print0 -name "__pycache__" -exec rm -rf {} \; > /dev/null'
    sh 'find . -print0 -name "*.pyc" -exec rm -f {} \; >/dev/null'
end

namespace :test do
    desc 'Type checker'
    task :type do
        sh 'mypy --ignore-missing-imports src/descriptor.py'
        sh 'mypy --ignore-missing-imports src/schema.py'
        sh 'mypy --ignore-missing-imports src/error.py'
    end

    desc 'Unit tests'
    task :unit do
        sh 'coverage run --source src test/test_schema_processing.py --verbose'
        sh 'coverage run --source src test/test_validation.py --verbose'
    end

    desc 'Test coverage'
    task :coverage => :unit do
        sh 'coverage report -m'
    end

    desc 'Python linter'
    task:lint do
        sh 'pylint --disable=too-many-public-methods,missing-docstring src/descriptor.py'
        sh 'pylint --disable=too-many-public-methods,missing-docstring src/schema.py'
        sh 'pylint --disable=too-many-public-methods,missing-docstring src/error.py'
        sh 'pylint --disable=too-many-public-methods,missing-docstring test/test_schema_processing.py'
        sh 'pylint --disable=too-many-public-methods,missing-docstring test/test_validation.py'
    end

    desc 'All tests'
    task :all => [:type, :unit, :coverage, :lint]
end

namespace :docker do
    desc 'Build Docker image'
    task :build do
        sh 'docker build -t csizsek/jysp:latest .'
    end

    desc 'Push image to registry'
    task :push do
        sh 'docker push csizsek/jysp:latest'
    end

    desc 'Docker build and push'
    task :all => [:build, :push]
end

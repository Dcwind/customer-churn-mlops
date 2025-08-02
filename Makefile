# Install ALL dependencies for a DEVELOPMENT environment
install:
	pip install --upgrade pip &&\
		pip install -r requirements-dev.txt

# Install ONLY production dependencies (for Docker, CI/CD)
install-prod:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# Format code with black
format:
	black src/

# Run tests 
test:
	# Add test 

# Run all tasks
all: install lint test
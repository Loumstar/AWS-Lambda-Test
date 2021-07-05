# Base image is Python 3.8 provided by AWS Lambda in Docker Hub
FROM public.ecr.aws/lambda/python:3.8

# Copy and install jsonschema package
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the script
COPY assert_similar.py ${LAMBDA_TASK_ROOT}

# Run the handler function
CMD ["assert_similar.handler"]
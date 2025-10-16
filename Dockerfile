# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy everything from your project into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 3000 (Render uses this)
EXPOSE 3000

# Command to run your bot
CMD ["python", "app.py"]

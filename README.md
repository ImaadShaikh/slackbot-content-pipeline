# slackbot-content-pipeline
A slackbot that helps content team streamline keyword based contents. This allows the users to type the keywords, which will automatically clean and group them, followed by generating ideas and finally exporting it in the form of PDF; All done within slack


Features
1. Input & Cleaning - Accepts CSV or keywords, removing duplicates
2. Clustering - Groups keywords using Kmeans and TFDF Vector
3. Content Generation - Extracts info from google results using Serper API
4. Idea Generation - Uses Ollama llm and rule based fall back.
5. Results - Displays result inside SLACK in the form of PDF

Architecture
Input -> Keyword Cleaning -> Clustering -> Websearch -> Post idea Generator -> Slack Output -> PDF Generation

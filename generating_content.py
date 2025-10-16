import requests
import random

# Rule-based fallback templates
templates = [
    "Share 3 quick tips about {}",
    "Write a LinkedIn post explaining why {} matters in 2025",
    "Summarize key trends in {}",
    "Post a short data insight thread on {}",
]

def rule_based_idea(cluster_name, keywords):
    topic = random.choice(keywords) if keywords else cluster_name
    return random.choice(templates).format(topic)


def idea_generator(cluster_name, keywords, outline=None):
    topic = ", ".join(keywords[:5]) or cluster_name

    outline_text = outline or "No outline context provided."
    prompt = f"""
You are an experienced content strategist and creative copywriter.

Here is the keyword cluster: {topic}

Here is some background context or outline (from web research):
{outline_text}

Now:
1. Identify what key insight, theme, or audience interest connects these keywords.
2. Propose a catchy, original *post idea* (for a blog, LinkedIn, or marketing campaign).
3. Write a short example post — use a fun, insightful, or professional tone depending on topic.
4. Add 1-2 lines explaining *why this idea works* and who it would appeal to.

Your output must follow this structure:
---
**Cluster:** {cluster_name}
**Post Idea:** [Give a short, catchy title]
**Concept:** [Describe the idea in 1-2 sentences]
**Example Post:** [Give a creative example paragraph]
**Why It Works:** [Explain briefly]
---

Keep the tone relevant to the keywords.
If it's a technical topic → be insightful.
If it's lifestyle/food → be playful or engaging.
If it's business → be sharp and trend-focused.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=90
        )
        data = response.json()
        idea_text = data.get("response", "").strip()

        # Handle empty or weak responses gracefully
        if not idea_text or len(idea_text.split()) < 20:
            print(" Weak Ollama output, falling back.")
            return rule_based_idea(cluster_name, keywords)
        return idea_text

    except Exception as e:
        print(f" Ollama generation failed: {e}")
        return rule_based_idea(cluster_name, keywords)


def generating_idea_with_clusters(clusters: dict, outlines: dict = None):
    ideas = {}
    for name, words in clusters.items():
        outline = outlines.get(name) if outlines else None
        ideas[name] = idea_generator(name, words, outline)
    return ideas

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def cluster(keywords, n_clusters = None):
    if len(keywords) < 2:
        return {'cluster 1': keywords}
    
    vector = TfidfVectorizer(stop_words='english')
    X = vector.fit_transform(keywords)

    if n_clusters is None:
        n_clusters = min(5, len(keywords)// 2 or 1)

    
    kmeans = KMeans(n_clusters = n_clusters , random_state = 42)
    kmeans.fit(X)

    clusters  = {}
    for label , keyword in zip(kmeans.labels_, keywords):
        clusters.setdefault(f'cluster{label+1}', []).append(keyword)
    
    return clusters


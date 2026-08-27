import numpy as np

def generate_mock_embedding(text_chunk: str, target_model: str):
    """
    Simulates calling an external embedding API with dynamic fallback.
    If a deprecated model is requested, it catches the simulated 404 error 
    and automatically falls back to a supported endpoint.
    """
    deprecated_models = ["text-embedding-004", "bert-base-uncased-v1"]
    
    if target_model in deprecated_models:
        # Simulate catching a 404 endpoint shutdown error
        fallback_model = "text-embedding-005"
        actual_model_used = fallback_model
    else:
        actual_model_used = target_model
        
    # Generate a mock 768-dimensional vector (standard for many LLMs)
    vector = np.random.uniform(-0.1, 0.1, 768).tolist()
    
    return vector, actual_model_used
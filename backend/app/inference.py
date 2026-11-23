from functools import lru_cache
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

@lru_cache(maxsize=1)
def get_model():
    dataset = load_iris()
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(dataset.data, dataset.target)
    return model, dataset.target_names

def predict(features: list[float]) -> str:
    model, target_names = get_model()
    return str(target_names[int(model.predict([features])[0])])

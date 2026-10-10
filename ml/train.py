import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

def prepare_text(df):
    subject = df["subject"].fillna("").astype(str)
    text = df["text"].fillna("").astype(str)
    return subject + " " + text

def train_and_export():
    df = pd.read_csv("ml/data/train.csv")
    
    X = prepare_text(df)
    y = df["category"]
    
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    vectorizer = TfidfVectorizer(
        max_features=15000,
        stop_words="english",
        ngram_range=(1, 2)
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    
    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train_vec, y_train)
    
    val_preds = model.predict(X_val_vec)
    acc = accuracy_score(y_val, val_preds)
    print(f"Validation Accuracy: {acc:.4f}")
    print(classification_report(y_val, val_preds, zero_division=0))
    
    joblib.dump(model, "ml/artifacts/model.joblib")
    joblib.dump(vectorizer, "ml/artifacts/vectorizer.joblib")
    print("Model and vectorizer saved to ml/artifacts/")

if __name__ == "__main__":
    train_and_export()
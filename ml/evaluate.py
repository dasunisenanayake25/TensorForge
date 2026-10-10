import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score

def prepare_features(df):
    channel = df["channel"].fillna("").astype(str)
    language = df["language"].fillna("").astype(str)
    subject = df["subject"].fillna("").astype(str)
    text = df["text"].fillna("").astype(str)
    return channel + " " + language + " " + subject + " " + text

def evaluate():
    model = joblib.load("ml/artifacts/model.joblib")
    vectorizer = joblib.load("ml/artifacts/vectorizer.joblib")
    
    df_val = pd.read_csv("ml/data/validation.csv")
    X_val = prepare_features(df_val)
    y_val = df_val["category"]
    
    X_val_vec = vectorizer.transform(X_val)
    preds = model.predict(X_val_vec)
    
    print(f"Final Validation Accuracy: {accuracy_score(y_val, preds):.4f}")
    print(classification_report(y_val, preds, zero_division=0))

if __name__ == "__main__":
    evaluate()
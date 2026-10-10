import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion
from sklearn.metrics import accuracy_score

def prepare_text(df):
    channel = df["channel"].fillna("").astype(str)
    subject = df["subject"].fillna("").astype(str)
    text = df["text"].fillna("").astype(str)
    return channel + " " + subject + " " + text

def train_and_export():
    train_df = pd.read_csv("ml/data/train.csv")
    val_df = pd.read_csv("ml/data/validation.csv")
    
    X_train = prepare_text(train_df)
    y_train = train_df["category"]
    
    X_val = prepare_text(val_df)
    y_val = val_df["category"]
    
    vectorizer = FeatureUnion([
        ("word_tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=25000, sublinear_tf=True)),
        ("char_tfidf", TfidfVectorizer(ngram_range=(2, 5), analyzer="char", max_features=35000, sublinear_tf=True))
    ])
    
    print("Vectorizing multilingual data...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    
    print("Training LogisticRegression (with native predict_proba support)...")
    # Logistic Regression natively supports predict_proba for confidence estimation
    model = LogisticRegression(C=2.0, max_iter=1000, class_weight="balanced", random_state=42)
    model.fit(X_train_vec, y_train)
    
    val_preds = model.predict(X_val_vec)
    acc = accuracy_score(y_val, val_preds)
    print(f"\nModel Validation Accuracy: {acc:.4f}")
    
    # Export artifacts
    joblib.dump(model, "ml/artifacts/model.joblib")
    joblib.dump(vectorizer, "ml/artifacts/vectorizer.joblib")
    print("Successfully exported model and vectorizer with confidence support!")

if __name__ == "__main__":
    train_and_export()
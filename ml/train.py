import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import FeatureUnion
from sklearn.metrics import classification_report, accuracy_score
from sklearn.calibration import CalibratedClassifierCV

def prepare_features(df):
    channel = df["channel"].fillna("").astype(str)
    language = df["language"].fillna("").astype(str)
    subject = df["subject"].fillna("").astype(str)
    text = df["text"].fillna("").astype(str)
    # Combine channel, language, subject and text for comprehensive context
    return channel + " " + language + " " + subject + " " + text

def train_and_export():
    train_df = pd.read_csv("ml/data/train.csv")
    val_df = pd.read_csv("ml/data/validation.csv")
    
    X_train = prepare_features(train_df)
    y_train = train_df["category"]
    
    X_val = prepare_features(val_df)
    y_val = val_df["category"]
    
    # Advanced Multilingual Vectorizer
    vectorizer = FeatureUnion([
        ("word_tfidf", TfidfVectorizer(
            ngram_range=(1, 3), 
            max_features=30000, 
            sublinear_tf=True
        )),
        ("char_tfidf", TfidfVectorizer(
            ngram_range=(2, 5), 
            analyzer="char", 
            max_features=45000, 
            sublinear_tf=True
        ))
    ])
    
    print("Vectorizing multilingual feature space...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    
    print("Training Calibrated Linear Classifier...")
    base_svc = LinearSVC(C=0.8, class_weight="balanced", random_state=42)
    model = CalibratedClassifierCV(estimator=base_svc, cv=3)
    model.fit(X_train_vec, y_train)
    
    val_preds = model.predict(X_val_vec)
    acc = accuracy_score(y_val, val_preds)
    print(f"\n==========================================")
    print(f"Maximized Validation Accuracy: {acc:.4f}")
    print(f"==========================================\n")
    print(classification_report(y_val, val_preds, zero_division=0))
    
    joblib.dump(model, "ml/artifacts/model.joblib")
    joblib.dump(vectorizer, "ml/artifacts/vectorizer.joblib")
    print("Exported top-performing artifacts to ml/artifacts/")

if __name__ == "__main__":
    train_and_export()
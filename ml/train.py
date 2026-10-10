import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import FeatureUnion
from sklearn.calibration import CalibratedClassifierCV
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
    
    print("Vectorizing...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    
    # 1. Base LinearSVC
    base_model = LinearSVC(C=0.5, class_weight="balanced", random_state=42)
    base_model.fit(X_train_vec, y_train)
    
    # 2. Probability Calibration for accurate confidence values
    calibrated_model = CalibratedClassifierCV(estimator=base_model, cv="prefit")
    calibrated_model.fit(X_val_vec, y_val)
    
    val_preds = calibrated_model.predict(X_val_vec)
    print(f"Calibrated Model Accuracy: {accuracy_score(y_val, val_preds):.4f}")
    
    # Save artifacts
    joblib.dump(calibrated_model, "ml/artifacts/model.joblib")
    joblib.dump(vectorizer, "ml/artifacts/vectorizer.joblib")
    print("Successfully saved calibrated model with confidence prediction capability!")

if __name__ == "__main__":
    train_and_export()
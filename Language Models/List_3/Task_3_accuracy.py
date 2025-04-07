import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


original_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_100.csv"
augmented_mechanical_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_3_a_100.csv"
augmented_generative_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_3_b_100.csv"
augmented_semantic_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_3_c_100.csv"


original_df = pd.read_csv(original_file)
mechanical_df = pd.read_csv(augmented_mechanical_file)
generative_df = pd.read_csv(augmented_generative_file)
semantic_df = pd.read_csv(augmented_semantic_file)

def process_augmentation(original_df, augmented_df, strategy_name):
    combined_df = pd.merge(original_df, augmented_df, on="text", suffixes=("_original", f"_{strategy_name}"))
    print(combined_df.head())
    
    vectorizer = TfidfVectorizer(max_features=1000)
    original_features = vectorizer.fit_transform(combined_df["text"]).toarray()
    kmeans = KMeans(n_clusters=2, random_state=42)
    pseudo_labels = kmeans.fit_predict(original_features)
    combined_df['target'] = pseudo_labels
    
    augmented_features = vectorizer.transform(combined_df[f"augmented_review_{strategy_name}"]).toarray()
    X_train, X_test, y_train, y_test = train_test_split(augmented_features, combined_df['target'], test_size=0.2, random_state=42)
    
    model = LogisticRegression(max_iter=1000, solver='liblinear')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy for {strategy_name} augmentation: {accuracy:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    return accuracy

accuracy_mechanical = process_augmentation(original_df, mechanical_df, "mechanical")
accuracy_generative = process_augmentation(original_df, generative_df, "generative")
accuracy_semantic = process_augmentation(original_df, semantic_df, "semantic")

print("\nFinal Results:")
print(f"Mechanical Augmentation Accuracy: {accuracy_mechanical:.4f}")
print(f"Generative Augmentation Accuracy: {accuracy_generative:.4f}")
print(f"Semantic Augmentation Accuracy: {accuracy_semantic:.4f}")

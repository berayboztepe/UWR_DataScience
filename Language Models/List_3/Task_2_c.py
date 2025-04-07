import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

option_a_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\yelp_sentiment_results_100k.csv"
option_a_df = pd.read_csv(option_a_file)

option_b_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\yelp_contextual_embeddings_100k.csv"
option_b_df = pd.read_csv(option_b_file)

combined_df = pd.merge(option_a_df, option_b_df, on="review")

feature_columns = [f'feature_{i+1}' for i in range(option_b_df.shape[1] - 1)]
combined_df['combined_positive'] = combined_df['positive_score']
combined_df['combined_negative'] = combined_df['negative_score']
features = combined_df[feature_columns + ['combined_positive', 'combined_negative']]

combined_df['target'] = combined_df['predicted_sentiment'].apply(lambda x: 1 if x == "Positive" else 0)
target = combined_df['target']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000, solver='liblinear')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy Logistic Regression: {accuracy:.4f}")
print("Classification Report Logistic Regression:")
print(classification_report(y_test, y_pred))

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy Random Forest: {accuracy:.4f}")
print("Classification Report Random Forest:")
print(classification_report(y_test, y_pred))

model = XGBClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy XGBoost: {accuracy:.4f}")
print("Classification Report XGBoost:")
print(classification_report(y_test, y_pred))


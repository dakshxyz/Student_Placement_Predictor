import pandas as pd
import joblib
from tqdm.auto import tqdm
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('data/final_data.csv')

X = df.drop(columns=['Placement'])
y = df['Placement'].astype(int)

models = {
    'LogisticRegression': LogisticRegression(max_iter=5000, random_state=42),
    'SVC_rbf': SVC(kernel='rbf', probability=True, random_state=42),
    'RandomForest': RandomForestClassifier(n_estimators=400, random_state=42),
    'ExtraTrees': ExtraTreesClassifier(n_estimators=500, random_state=42),
    'GradientBoosting': GradientBoostingClassifier(random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=15),
    'DecisionTree': DecisionTreeClassifier(random_state=42)
}

feature_sets = {
    'basic_scaled': Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]),
    'poly2_scaled': Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('scaler', StandardScaler())
    ])
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

rows = []
for feat_name, feat_pipe in tqdm(feature_sets.items()):
    for model_name, model in models.items():
        pipe = Pipeline([
            ('features', feat_pipe),
            ('model', model)
        ])
        scores = cross_validate(
            pipe,
            X, y,
            cv=cv,
            scoring={'acc': 'accuracy', 'f1': 'f1', 'roc': 'roc_auc'},
            n_jobs=-1
        )
        rows.append({
            'feature_set': feat_name,
            'model': model_name,
            'accuracy_mean': scores['test_acc'].mean(),
            'f1_mean': scores['test_f1'].mean(),
            'roc_auc_mean': scores['test_roc'].mean()
        })

results = pd.DataFrame(rows).sort_values(
    ['f1_mean', 'roc_auc_mean', 'accuracy_mean'],
    ascending=False
)

print(results.head(10))

best_pipe = Pipeline([
    ('features', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])),
    ('model', GradientBoostingClassifier(random_state=42))
])

y_pred = cross_val_predict(best_pipe, X, y, cv=cv, n_jobs=-1, method='predict')
y_prob = cross_val_predict(best_pipe, X, y, cv=cv, n_jobs=-1, method='predict_proba')[:, 1]

print('Accuracy:', accuracy_score(y, y_pred))
print('F1:', f1_score(y, y_pred))
print('ROC AUC:', roc_auc_score(y, y_prob))
print(classification_report(y, y_pred))

cm = confusion_matrix(y, y_pred)
print(cm)


best_pipe.fit(X, y)
joblib.dump(best_pipe, 'placement_predictor.pkl')

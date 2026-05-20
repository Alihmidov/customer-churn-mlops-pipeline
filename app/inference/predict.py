import pandas as pd
from catboost import CatBoostClassifier
from huggingface_hub import hf_hub_download
from app.schemas.request_body import CustomerChurnInput
from pipelines.data_transformation import clean_data, apply_feature_engineering

class ChurnPredictor:
    def __init__(self, model_path: str = None):
        if not model_path:
            model_path = hf_hub_download(
                repo_id="Alihmidov/customer-churn-catboost", 
                filename="catboost_model.cbm"
            )
        
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)
        self.model_features = self.model.feature_names_

    def predict(self, input_data: CustomerChurnInput) -> dict:
        raw_df = pd.DataFrame([input_data.model_dump(by_alias=True)])
        cleaned_df = clean_data(raw_df)
        
        if 'Churn' in cleaned_df.columns:
            cleaned_df = cleaned_df.drop(columns=['Churn'])
            
        final_df = apply_feature_engineering(cleaned_df)
        X_test = pd.DataFrame(0, index=final_df.index, columns=self.model_features)
        final_df_map = {col.lower().strip(): col for col in final_df.columns}
        
        for feature in self.model_features:
            feature_lower = feature.lower().strip()
            if feature_lower in final_df_map:
                X_test[feature] = final_df[final_df_map[feature_lower]]
            elif 'gender' in feature_lower and 'male' in feature_lower:
                gender_col = final_df_map.get('gender')
                if gender_col:
                    X_test[feature] = (final_df[gender_col].astype(str).str.title() == 'Male').astype(int)
            elif 'subscription' in feature_lower and 'premium' in feature_lower:
                sub_col = final_df_map.get('subscription type')
                if sub_col:
                    X_test[feature] = (final_df[sub_col].astype(str).str.title() == 'Premium').astype(int)
            elif 'subscription' in feature_lower and 'standard' in feature_lower:
                sub_col = final_df_map.get('subscription type')
                if sub_col:
                    X_test[feature] = (final_df[sub_col].astype(str).str.title() == 'Standard').astype(int)

        prediction = int(self.model.predict(X_test)[0])
        probability = float(self.model.predict_proba(X_test)[0][1])

        return {
            "customer_id": input_data.CustomerID,
            "churn_prediction": prediction,
            "churn_probability": round(probability, 4),
            "status": "Active" if prediction == 0 else "At Risk"
        }
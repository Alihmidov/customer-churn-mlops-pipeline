import os
import pandas as pd
from catboost import CatBoostClassifier
from app.schemas.request_body import CustomerChurnInput
from pipelines.data_transformation import clean_data, apply_feature_engineering

class ChurnPredictor:
    def __init__(self, model_path: str = None):
        # 1. Əgər model_path ötürülməyibsə, mühit dəyişənini yoxlayırıq
        if model_path is None:
            model_path = os.getenv("MODEL_PATH")
        
        # 2. Docker daxilində tam, dəqiq və zəmanətli mütləq ünvanı (Absolute path) təyin edirik
        if not model_path:
            # predict.py-dan (app/inference/predict.py) düzgün şəkildə 2 addım geri qayıdırıq
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # Layihənin əsl kök qovluğundan models qovluğuna keçid edirik
            model_path = os.path.normpath(os.path.join(base_dir, "..", "models", "catboost_churn_model.cbm"))
            
        # Əgər Docker daxilində hər hansı səbəbdən yol yenə çaşsa, birbaşa workspace yolunu məcburi mənimsədirik
        if not os.path.exists(model_path) and os.path.exists("/workspace/models/catboost_churn_model.cbm"):
            model_path = "/workspace/models/catboost_churn_model.cbm"
        
        self.model = CatBoostClassifier()
        
        # 3. Yoxlama loqu (Render loglarında dəqiq haradan oxuduğunu görəcəksən)
        print(f"--- LOADING CATBOOST MODEL FROM: {model_path} ---")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
            
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
"""
Stock Market Prediction Module
Integrates with existing finance models to provide stock market analysis
"""
import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

class StockMarketPredictor:
    """
    Stock Market Prediction System using ML models from Domain/Finance/Model
    """
    
    def __init__(self, model_dir: str = None):
        """Initialize stock market predictor with pre-trained models"""
        if model_dir is None:
            model_dir = os.path.join(os.path.dirname(__file__), 'models')
        
        self.model_dir = model_dir
        self.models = {}
        self.scalers = {}
        self._load_models()
    
    def _load_models(self):
        """Load all stock market models"""
        try:
            # Load stock-specific models
            self.models['stock_gb'] = joblib.load(
                os.path.join(self.model_dir, 'stock_gb_model.pkl')
            )
            self.models['stock_svm'] = joblib.load(
                os.path.join(self.model_dir, 'svm_model.pkl')
            )
            
            # Load scalers
            self.scalers['stock_scaler'] = joblib.load(
                os.path.join(self.model_dir, 'stock_scaler.pkl')
            )
            
            print("✅ Stock market models loaded successfully")
            print(f"   - Stock Gradient Boosting: {type(self.models['stock_gb']).__name__}")
            print(f"   - Stock SVM: {type(self.models['stock_svm']).__name__}")
            print(f"   - Stock Scaler: {type(self.scalers['stock_scaler']).__name__}")
            
        except Exception as e:
            print(f"⚠️ Error loading stock models: {e}")
            self.models = {}
            self.scalers = {}
    
    def predict_stock_movement(self, features: Dict) -> Dict:
        """
        Predict stock movement direction and confidence
        
        Args:
            features: Dictionary containing stock features like:
                - 'open_price': Opening price
                - 'high_price': Daily high
                - 'low_price': Daily low
                - 'volume': Trading volume
                - 'ma_5': 5-day moving average
                - 'ma_20': 20-day moving average
                - 'rsi': RSI indicator
                - 'volatility': Price volatility
        
        Returns:
            Dictionary with prediction results
        """
        if not self.models:
            return {
                'error': 'Stock models not loaded',
                'prediction': None,
                'confidence': 0.0
            }
        
        try:
            # Prepare features for model
            feature_list = self._prepare_features(features)
            
            # Make predictions with both models
            gb_pred = self.models['stock_gb'].predict([feature_list])[0]
            svm_pred = self.models['stock_svm'].predict([feature_list])[0]
            
            # Get confidence scores
            gb_confidence = max(self.models['stock_gb'].predict_proba([feature_list])[0])
            svm_confidence = max(self.models['stock_svm'].predict_proba([feature_list])[0]) if hasattr(self.models['stock_svm'], 'predict_proba') else 0.7
            
            # Ensemble prediction (weighted average)
            ensemble_confidence = (gb_confidence * 0.6 + svm_confidence * 0.4)
            final_prediction = 1 if gb_pred == 1 else 0  # Binary: 1=UP, 0=DOWN
            
            return {
                'prediction': 'UP' if final_prediction == 1 else 'DOWN',
                'confidence': float(ensemble_confidence),
                'gb_prediction': 'UP' if gb_pred == 1 else 'DOWN',
                'svm_prediction': 'UP' if svm_pred == 1 else 'DOWN',
                'gb_confidence': float(gb_confidence),
                'svm_confidence': float(svm_confidence),
                'features_used': list(features.keys()),
                'timestamp': datetime.now().isoformat(),
                'recommendation': self._get_recommendation(final_prediction, ensemble_confidence)
            }
            
        except Exception as e:
            return {
                'error': f'Prediction failed: {str(e)}',
                'prediction': None,
                'confidence': 0.0
            }
    
    def _prepare_features(self, features: Dict) -> List:
        """Prepare and normalize features for model input"""
        required_features = [
            'open_price', 'high_price', 'low_price', 'close_price',
            'volume', 'ma_5', 'ma_20', 'rsi', 'volatility'
        ]
        
        # Ensure all required features exist
        feature_list = []
        for feature in required_features:
            value = features.get(feature, 0)
            if isinstance(value, str):
                value = float(value.replace(',', '').replace('$', ''))
            feature_list.append(value)
        
        # Normalize using scaler if available
        if self.scalers.get('stock_scaler') and len(feature_list) >= 8:
            try:
                # Scale only the first 8 features (matching training)
                scaled_features = self.scalers['stock_scaler'].transform([feature_list[:8]])
                feature_list = scaled_features[0].tolist() + feature_list[8:]
            except:
                pass  # Use original features if scaling fails
        
        return feature_list
    
    def _get_recommendation(self, prediction: int, confidence: float) -> str:
        """Generate trading recommendation based on prediction and confidence"""
        if confidence < 0.6:
            return "HOLD - Low confidence, wait for clearer signals"
        elif prediction == 1:
            if confidence > 0.8:
                return "STRONG BUY - High confidence upward movement expected"
            else:
                return "BUY - Upward movement expected"
        else:
            if confidence > 0.8:
                return "STRONG SELL - High confidence downward movement expected"
            else:
                return "SELL - Downward movement expected"
    
    def analyze_market_sentiment(self, news_headlines: List[str]) -> Dict:
        """
        Basic sentiment analysis for market news (placeholder for enhancement)
        
        Args:
            news_headlines: List of recent news headlines
        
        Returns:
            Dictionary with sentiment analysis
        """
        positive_words = ['bullish', 'rally', 'surge', 'gain', 'growth', 'strong', 'rise']
        negative_words = ['bearish', 'decline', 'fall', 'drop', 'loss', 'weak', 'decline']
        
        positive_count = sum(1 for headline in news_headlines 
                          for word in positive_words if word.lower() in headline.lower())
        negative_count = sum(1 for headline in news_headlines 
                          for word in negative_words if word.lower() in headline.lower())
        
        total_headlines = len(news_headlines)
        if total_headlines == 0:
            return {'sentiment': 'NEUTRAL', 'score': 0.0, 'confidence': 0.0}
        
        sentiment_score = (positive_count - negative_count) / total_headlines
        confidence = min(abs(sentiment_score), 1.0)
        
        if sentiment_score > 0.1:
            sentiment = 'BULLISH'
        elif sentiment_score < -0.1:
            sentiment = 'BEARISH'
        else:
            sentiment = 'NEUTRAL'
        
        return {
            'sentiment': sentiment,
            'score': round(sentiment_score, 3),
            'confidence': round(confidence, 2),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'total_headlines': total_headlines
        }
    
    def get_risk_assessment(self, portfolio_data: Dict) -> Dict:
        """
        Assess portfolio risk based on stock predictions and diversification
        
        Args:
            portfolio_data: Dictionary with portfolio information
        
        Returns:
            Dictionary with risk assessment
        """
        try:
            total_value = portfolio_data.get('total_value', 0)
            stock_concentration = portfolio_data.get('largest_holding_pct', 0)
            diversification_score = portfolio_data.get('diversification_score', 0.5)
            
            # Risk calculation
            concentration_risk = 'HIGH' if stock_concentration > 0.4 else ('MEDIUM' if stock_concentration > 0.2 else 'LOW')
            diversification_risk = 'HIGH' if diversification_score < 0.3 else ('MEDIUM' if diversification_score < 0.6 else 'LOW')
            
            # Overall risk score
            risk_factors = {
                'HIGH': 3,
                'MEDIUM': 2,
                'LOW': 1
            }
            
            overall_risk_score = (risk_factors[concentration_risk] + risk_factors[diversification_risk]) / 2
            
            return {
                'overall_risk': 'HIGH' if overall_risk_score > 2.5 else ('MEDIUM' if overall_risk_score > 1.5 else 'LOW'),
                'risk_score': round(overall_risk_score, 1),
                'concentration_risk': concentration_risk,
                'diversification_risk': diversification_risk,
                'recommendations': self._get_risk_recommendations(concentration_risk, diversification_risk),
                'portfolio_value': total_value,
                'assessment_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': f'Risk assessment failed: {str(e)}',
                'overall_risk': 'UNKNOWN',
                'risk_score': 0.0
            }
    
    def _get_risk_recommendations(self, concentration_risk: str, diversification_risk: str) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []
        
        if concentration_risk == 'HIGH':
            recommendations.append("Consider diversifying your largest holding to reduce concentration risk")
        elif concentration_risk == 'MEDIUM':
            recommendations.append("Monitor your largest holding closely for rebalancing opportunities")
        
        if diversification_risk == 'HIGH':
            recommendations.append("Increase portfolio diversification across different sectors")
        elif diversification_risk == 'MEDIUM':
            recommendations.append("Consider adding stocks from underrepresented sectors")
        
        if not recommendations:
            recommendations.append("Portfolio appears well-diversified. Continue regular monitoring.")
        
        return recommendations

# Initialize global predictor instance
stock_predictor = StockMarketPredictor()

def get_stock_prediction(features: Dict) -> Dict:
    """Global function to get stock prediction"""
    return stock_predictor.predict_stock_movement(features)

def get_market_sentiment(news_headlines: List[str]) -> Dict:
    """Global function to analyze market sentiment"""
    return stock_predictor.analyze_market_sentiment(news_headlines)

def get_portfolio_risk(portfolio_data: Dict) -> Dict:
    """Global function to assess portfolio risk"""
    return stock_predictor.get_risk_assessment(portfolio_data)

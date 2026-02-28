from .plugin import Strategy
import re

class FinanceStrategy(Strategy):
    def get_system_prompt(self) -> str:
        return (
            "You are a Financial Risk Analyst AI expert. Provide comprehensive, detailed answers. "
            "Rules: 1) Use provided context when available. 2) Give complete explanations. "
            "3) Use bullet points for clarity. 4) Include relevant details and examples. "
            "5) Use clear headings and structure. 6) Provide thorough analysis. "
            "Be comprehensive and professional in your responses."
        )

    def inject_constraints(self, context: str, query: str) -> str:
        if not context:
            return (
                f"Query: {query}\n\n"
                "Note: No domain documents were provided for context. Provide a comprehensive answer using your baseline knowledge. "
                "Include all relevant aspects and details for a complete explanation."
            )
        
        return (
            f"Context Documents:\n{context}\n\n"
            f"User Query: {query}\n\n"
            "Instruction: Provide a comprehensive answer using the context documents above. "
            "Include all relevant details and explanations. Use clear structure with headings and bullet points. "
            "Ensure the answer is complete and thorough."
        )
    
    def format_response(self, response: str) -> str:
        """Clean up response formatting to remove asterisks and improve structure"""
        # Remove asterisks used for bold formatting
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
        
        # Clean up excessive whitespace
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        
        # Ensure proper section breaks
        cleaned = re.sub(r'([.!?])\s*([A-Z])', r'\1\n\n\2', cleaned)
        
        return cleaned.strip()

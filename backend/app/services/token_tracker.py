from typing import Dict, Any


class TokenTracker:
    """
    Tracks estimated input, output, and total token usage and calculates approximate API cost metrics.
    """

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0

    def record_usage(self, prompt_text: str, response_text: str) -> Dict[str, Any]:
        """
        Estimates token usage based on 4-char per token rule of thumb.
        """
        input_tokens = max(1, len(prompt_text) // 4)
        output_tokens = max(1, len(response_text) // 4)
        
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_requests += 1

        # Estimated cost (~$0.15 per million input tokens, $0.60 per million output tokens for mini/flash models)
        cost = (input_tokens / 1_000_000 * 0.15) + (output_tokens / 1_000_000 * 0.60)

        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "estimated_cost_usd": round(cost, 6),
        }

    def get_summary(self) -> Dict[str, Any]:
        total_tokens = self.total_input_tokens + self.total_output_tokens
        avg_tokens = round(total_tokens / self.total_requests, 2) if self.total_requests > 0 else 0.0
        
        return {
            "total_requests": self.total_requests,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": total_tokens,
            "avg_tokens_per_question": avg_tokens,
        }


# Singleton instance
_token_tracker_instance = TokenTracker()


def get_token_tracker() -> TokenTracker:
    return _token_tracker_instance

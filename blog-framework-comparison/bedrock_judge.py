"""Bedrock Claude wrapper for DeepEval.

DeepEval requires a custom model class to use non-OpenAI providers.
This wrapper connects DeepEval metrics to Claude on Amazon Bedrock.
"""

import json
import boto3
from deepeval.models.base_model import DeepEvalBaseLLM


class BedrockJudge(DeepEvalBaseLLM):
    """Use Claude on Amazon Bedrock as the judge model for DeepEval metrics."""

    def __init__(self, model_id, region="us-east-1"):
        self.model_id = model_id
        self.client = boto3.client("bedrock-runtime", region_name=region)
        super().__init__(model=model_id)

    def load_model(self):
        return self.client

    def generate(self, prompt: str, schema=None) -> str:
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "messages": [{"role": "user", "content": prompt}],
            }),
        )
        return json.loads(response["body"].read())["content"][0]["text"]

    async def a_generate(self, prompt: str, schema=None) -> str:
        return self.generate(prompt, schema=schema)

    def get_model_name(self) -> str:
        return self.model_id

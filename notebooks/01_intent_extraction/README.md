# Intent Extraction with Mistral and LangChain

## Running Mistral Locally

To keep things simple the 7B model released by Mistral AI, updated to version 0.2 will be used and hosted locally on the same machine with Ollama. In a production situation this model can be hosted in [AWS SageMaker](https://aws.amazon.com/blogs/machine-learning/mistral-7b-foundation-models-from-mistral-ai-are-now-available-in-amazon-sagemaker-jumpstart/) or a hosted service as provided by [Mistral AI](https://docs.mistral.ai/). 

Linux users can install Ollama with the following command:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

The following commands are then executed to run Mistral:

```bash
ollama pull mistral
ollama run mistral
```

The following command can be executed to confirm that the model is running as expected:

```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt":"Here is a story about llamas eating grass"
 }'
```
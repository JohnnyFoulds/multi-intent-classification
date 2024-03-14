# Multi-intent Natural Language Classification

[![GitHub license](https://img.shields.io/github/license/JohnnyFoulds/multi-intent-classification)](https://github.com/JohnnyFoulds/multi-intent-classification/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/JohnnyFoulds/multi-intent-classification)](https://github.com/JohnnyFoulds/multi-intent-classification/issues)
[![GitHub stars](https://img.shields.io/github/stars/JohnnyFoulds/multi-intent-classification)](https://github.com/JohnnyFoulds/multi-intent-classification/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/JohnnyFoulds/multi-intent-classification)](https://github.com/JohnnyFoulds/multi-intent-classification/network)
[![Python version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Table of Contents
- [Overview](#overview)
- [Project Goals](#project-goals)
- [Methodology](#methodology)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

This project focuses on the challenge of understanding multiple intents in customer reviews, using a mix of Large Language Models (LLMs) and deep learning techniques. Our goal is to improve how we interpret complex feedback from customers, making significant strides in the field of natural language understanding (NLU).


## Installation

To get started with this project, clone the repo and install the required dependencies:

```bash
git clone https://github.com/JohnnyFoulds/multi-intent-classification.git
cd multi-intent-classification
pip install -r requirements.txt
```

## Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Project Goals

The main goal is to create a robust system that can identify and classify various intents within customer reviews. We plan to combine the advanced capabilities of LLMs with traditional deep-learning approaches to uncover the complex layers of intent in text data, providing valuable insights for both businesses and academic research.

## Methodology

Our methodology integrates state-of-the-art language models with deep learning to systematically process and classify customer feedback:

### 1. Intent Extraction with Mistral and LangChain

We start by using Mistral to analyze customer reviews, using a predefined list of categories to identify intents and sentiment. LangChain, a library known for its effectiveness with language models, is crucial in this phase for accurate intent recognition.

### 2. Multi-class Classification Model Development

After extracting intents, we use Keras, a comprehensive deep learning library, to develop a multi-class classification model. This model is trained on the extracted data to accurately classify intents.

### 3. Sentiment Analysis Model Construction

We then create a sentiment analysis model using Keras, which assesses the sentiment for each classified intent. This model processes both the text and its associated classes to provide a sentiment rating for each intent.

### 4. Fine-tuning Small Language Models (SLM)

Additionally, we explore refining Small Language Models (SLMs) with Keras to offer an alternative to Mistral for intent extraction. This step aims to improve our system's efficiency and versatility.

## Roadmap

Our initial focus is on developing the intent extraction and multi-class classification capabilities. Establishing this foundation is essential for the success of the subsequent steps, allowing us to accurately interpret multi-intent customer feedback.

## Impact and Applications

Accurately identifying multi-intent in customer reviews can greatly enhance customer service and inform product development. This project has the potential to make significant contributions to these areas, as well as offer new directions for research in natural language processing (NLP) and artificial intelligence (AI).

## Conclusion

This project merges academic principles with practical application in an effort to deepen our understanding of natural language. By integrating LLMs with deep learning, we aim to uncover more profound insights into customer intent, innovating in the realm of natural language classification.

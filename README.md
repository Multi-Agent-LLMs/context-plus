<br />
<p align="center">
<a><img src="https://raw.githubusercontent.com/Multi-Agent-LLMs/context-plus/main/image/contextplus-circle.png" alt="ContextPlus" width="128" height="128" title="FawnRescue"></a>
  <h3 align="center">ContextPlus</h3>
  <p align="center">
    Empowering Conversations with Real-Time Facts<br />
    <p align="center">
  <a href="https://github.com/Multi-Agent-LLMs/ContextPlus/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Multi-Agent-LLMs/ContextPlus" alt="License"></a>
  <a href="https://github.com/Multi-Agent-LLMs/ContextPlus/network/members"><img src="https://img.shields.io/github/forks/Multi-Agent-LLMs/ContextPlus?style=social" alt="GitHub forks"></a>
  <a href="https://github.com/Multi-Agent-LLMs/ContextPlus/stargazers"><img src="https://img.shields.io/github/stars/Multi-Agent-LLMs/ContextPlus?style=social" alt="GitHub stars"></a>
</p>
    <p>
    <a href="https://github.com/Multi-Agent-LLMs/ContextPlus/issues">Report Bug</a>
    ·
    <a href="https://github.com/Multi-Agent-LLMs/ContextPlus/issues">Request Feature</a>
    </p>
  </p>
</p>

## Overview
**ContextPlus** is a Python library designed to enhance conversations by providing real-time facts and information using large language models (LLMs). It operates completely on the CPU, making it accessible for integration into various applications without the need for specialized hardware.

## Installation

To install ContextPlus, use the following pip command:

```bash
pip install contextplus
```

## Usage

Import and use the `context` function from the `contextplus` library to integrate real-time factual data into your projects:

```python
from contextplus import context

# Example usage
response = context("Who are the family members of Barack Obama?")
print(response)
```

```
>> The family of Barack Obama, the 44th president of the United States, is a prominent American family active in law, education, activism and politics. His immediate family includes his wife Michelle Obama and daughters Malia and Sasha. He often referred to his family during his candidacy and two terms as president. His family is of African-American heritage, descendants of Africans and Europeans of the colonial era and antebellum eras. Michelle Obama's family history traces from colonists and slavery in the South to Reconstruction.
```

<br />
<p align="center">
<a><img src="https://raw.githubusercontent.com/Multi-Agent-LLMs/context-plus/main/image/contextplus-circle.png" alt="ContextPlus" width="128" height="128" title="FawnRescue"></a>
  <h3 align="center">ContextPlus</h3>
  <p align="center">
    Empowering Conversations with Real-Time Facts<br />
    <p align="center">
  <a href="https://github.com/Multi-Agent-LLMs/ContextPlus/blob/main/LICENSE"><img src="https://img.shields.io/github/license/FawnRescue/drone" alt="License"></a>
  <a href="https://github.com/Multi-Agent-LLMs/ContextPlus/network/members"><img src="https://img.shields.io/github/forks/FawnRescue/drone?style=social" alt="GitHub forks"></a>
  <a href="https://github.com/Multi-Agent-LLMs/ContextPlus/stargazers"><img src="https://img.shields.io/github/stars/FawnRescue/drone?style=social" alt="GitHub stars"></a>
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
response = context("What is a LLM?")
print(response)
```

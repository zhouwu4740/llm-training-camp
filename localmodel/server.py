from typing import List

from flask import Flask, request, jsonify
from logger import LOGGER as logger
from base import LocalModel

app = Flask(__name__)


# 模型预测
def invoke_model(prompt, history=None) -> (str, List[str]):
    model, tokenizer = LocalModel().get_model_tokenizer('ZhipuAI/chatglm3-6b')
    response, history = model.chat(tokenizer, prompt, history=history)
    return response, history


@app.route('/', methods=['POST'])
def process():
    try:
        data = request.get_json()
        logger.info(f"收到一个调用请求: {data}")

        # "prompt": prompt,
        # "temperature": self.temperature,
        # "history": self.history,
        # "max_length": self.max_token,
        # "top_p": self.top_p,

        if 'prompt' in data:
            prompt = data['prompt']
            response, history = invoke_model(prompt, history=[])
            logger.info(f"调用成功: {response}")
            return jsonify({'response': response})
        else:
            logger.error(f"调用失败: prompt is missing")
            return jsonify({'error': 'prompt is missing'}), 400
    except Exception as e:
        logger.error(f"调用失败: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

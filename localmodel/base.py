from modelscope import AutoTokenizer, AutoModel, snapshot_download


class LocalModel:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LocalModel, cls).__new__(cls)
            cls._instance._model_tokenizers = {}

        return cls._instance

    def get_model_tokenizer(self, model_id):
        if model_id not in self._instance._model_tokenizers:
            # self._instance._model_tokenizers[model_name] = ModelProvider.get_model(model_name)
            model_dir = snapshot_download(model_id, revision="v1.0.0")
            tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
            model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).quantize(4).cuda()
            model = model.eval()
            self._instance._model_tokenizers[model_id] = (model, tokenizer)
        return self._instance._model_tokenizers[model_id]

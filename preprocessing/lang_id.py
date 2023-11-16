import fasttext

from huggingface_hub import hf_hub_download

class LanguageIdentification:
    def __init__(self):

      model_path = hf_hub_download(repo_id="facebook/fasttext-language-identification", filename="model.bin")

      model = fasttext.load_model(model_path)

    def pred(self,text):

      result = model.predict(text)
      return {'label': result[0][0],
              'score': result[1][0]}

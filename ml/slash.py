import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
import warnings


warnings.filterwarnings('ignore')


offload_folder = './offload'
# device = torch.device('mps') if torch.backends.mps.is_available() else torch.device(
# 'cpu')


def get_text_response_v0(question: str) -> str:
    ## v2 models
    model_path = 'openlm-research/open_llama_3b_v2'
    # model_path = 'openlm-research/open_llama_7b_v2'

    ## v1 models
    # model_path = 'openlm-research/open_llama_3b'
    # model_path = 'openlm-research/open_llama_7b'
    # model_path = 'openlm-research/open_llama_13b'

    DEVICE = 'mps'
    tokenizer = LlamaTokenizer.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32,
        device_map=DEVICE,
        offload_folder=offload_folder,
    )
    model.to(DEVICE)

    # prompt = 'Q: My phone is not working, can I get customer support?\nA:'
    prompt = f"Q: {question}\nA:"
    input_ids = tokenizer(prompt, return_tensors='pt').input_ids.to(DEVICE)

    generation_output = model.generate(
        input_ids=input_ids, max_new_tokens=32
    )
    response = tokenizer.decode(generation_output[0])
    filtered_response = response.split('\n')[1]
    return filtered_response

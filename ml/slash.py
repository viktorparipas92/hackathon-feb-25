import torch
import random

from PIL import Image, ImageDraw
import requests
from transformers import pipeline
from transformers import AutoProcessor, Blip2ForConditionalGeneration
from transformers import LlamaTokenizer, LlamaForCausalLM
import warnings
warnings.filterwarnings("ignore")

from context import fetch_relevant_document, image_requests


    
# Categories Count: {'STATUS_RETURN': 275, 'CANCEL_REQUEST': 29, 'OTHER': 26, 'STATUS_SHIPPING': 66, 'PROOF_COMPLAINT': 94, 'WRONG_ADDRESS': 30, 'EXCHANGE': 51, 'UNCLEAR_C_REQUEST': 1, 'PROFORMA_INVOICE': 11, 'SHIPPING': 43, 'NO_PROOF': 13, 'COMPLAINT': 8, 'DISCOUNT_CODE': 4, 'PRICE_MATCH': 2, 'MISSING': 9, 'CANCEL': 3, 'FW_SHIPPING_PROCESS': 23, 'WRONG_PRODUCT': 16, 'RECEIPT': 22, 'UNSUBSCRIBE': 1, 'HOW_TO_RETURN': 146, 'PRICE': 1, 'PRODUCT': 40, '3F2': 1, 'RETURN': 37}

def text_response_V0(question):
    ## v2 models
    model_path = 'openlm-research/open_llama_3b_v2'
    # model_path = 'openlm-research/open_llama_7b_v2'

    ## v1 models
    # model_path = 'openlm-research/open_llama_3b'
    # model_path = 'openlm-research/open_llama_7b'
    # model_path = 'openlm-research/open_llama_13b'

    tokenizer = LlamaTokenizer.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, device_map='auto',
    )

    # Fetch the relevant document based on the question
    device = "cuda"
    model.to(device)
    # context = fetch_relevant_document(question, "Initial")
    # print(context)
    # Generate the response using the context
    # prompt = f"{context}\nA:"
    prompt = f"Q: {question}\nA:"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    
    generation_output = model.generate(
        input_ids=input_ids, max_new_tokens=32
    )
    # print(tokenizer.decode(generation_output[0]))
    response = tokenizer.decode(generation_output[0])
    filtered_response = response.split("\n")[1]
    image_req = random.choice(image_requests)
    # print(f"{filtered_response} {image_req}")
    return f"{filtered_response} {image_req}"

# print(text_response_V0("Hello,\n\nI have returned the following order: [ORDER_NUMBER]. It was sent via the UPS\nreturn label and according to the tracking information you received it on\n2nd Jan.\n\nUPS tracking number: [TRACKING_NUMBER]\n\nCan you please action the refund please?\n\nThanks\n[NAME]"))

categories= {
    "Software",
    "Damaged_Product",
    "Automotive",
    "Smart_Home",
   "Medical_Equipment"
}

# print(text_response_V0("Software"))
# print(text_response_V0("Damaged_Product"))
# print(text_response_V0("Automotive"))
# print(text_response_V0("Smart_Home"))
# print(text_response_V0("Medical_Equipment"))


# from transformers import AutoTokenizer
# import transformers 
# import torch
# model = "TinyLlama/TinyLlama_v1.1"
# tokenizer = AutoTokenizer.from_pretrained(model)
# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model,
#     torch_dtype=torch.float16,
#     device_map="auto",
# )
# from context import fetch_relevant_document, image_requests

# context = fetch_relevant_document("Damaged_Product", "Initial")
# sequences = pipeline(
#     # 'The TinyLlama project aims to pretrain a 1.1B Llama model on 3 trillion tokens. With some proper optimization, we can achieve this within a span of "just" 90 days using 16 A100-40G GPUs 🚀🚀. The training has started on 2023-09-01.',
#     context,
#     do_sample=True,
#     top_k=10,
#     num_return_sequences=1,
#     repetition_penalty=1.5,
#     eos_token_id=tokenizer.eos_token_id,
#     max_length=500,
# )
# for seq in sequences:
#     print(f"Result: {seq['generated_text']}")

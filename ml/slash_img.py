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


# ##################################### OPT1
# import numpy as np
# # import skimage

image_path = "../assets/pexels-photo-8413299.jpeg"

# vqa_pipeline = pipeline("visual-question-answering") # -- short answer
# # processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
# # model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
# # model.to("cuda")

# image =  Image.open(image_path)
# question = "Is there a woman?"
# prompt = f"Question: {question} Answer:"

# # inputs = processor(image, text=prompt, return_tensors="pt").to("cuda", torch.float16)

# # generated_ids = model.generate(**inputs, max_new_tokens=10)
# # generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

# print(vqa_pipeline(image, question, top_k=1))
# # print(generated_text)


##################################### OPT2

from transformers import AutoProcessor, LlavaForConditionalGeneration

model_id = "bczhou/tiny-llava-v1-hf"
prompt = "USER: <image>\nWhat are these?\nASSISTANT:"
# image_file = "http://images.cocodataset.org/val2017/000000039769.jpg"
model = LlavaForConditionalGeneration.from_pretrained(
model_id,
torch_dtype=torch.float16,
low_cpu_mem_usage=True,
).to(0)
processor = AutoProcessor.from_pretrained(model_id)
# raw_image = Image.open(requests.get(image_file, stream=True).raw)
def process_image(image_path):
    raw_image = Image.open(image_path)
    inputs = processor(prompt, raw_image, return_tensors='pt').to(0, torch.float16)
    output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
    response = processor.decode(output[0][2:], skip_special_tokens=True)
    # split after ASSSITANT: 
    cut_response = response.split("ASSISTANT: ")[1]
    return cut_response

# print(process_image(image_path))
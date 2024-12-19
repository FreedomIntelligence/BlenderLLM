from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def generate_response(model_name: str, prompt: str, max_new_tokens: int = 512) -> str:

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    messages = [
        {"role": "system", "content": "You are an expert in using bpy script to create 3D models. Based on the following instruction, your task is to write the corresponding bpy script that will generate the desired 3D model in Blender. Please pay close attention to every detail in the script and ensure it fully adheres to the provided specifications."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens
    )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return response

if __name__ == "__main__":
    model_name = "BlenderLLM"
    prompt = "Please drow a cube."
    result = generate_response(model_name, prompt)
    print("Generated Response:\n", result)

import argparse
from scripts.infer import generate_response

def parse_arguments():
    """
    Parse command line arguments for model name and prompt.
    """
    parser = argparse.ArgumentParser(description="Generate a response using a specified model.")
    parser.add_argument("--model_name", type=str, required=True, help="Name of the model to use for response generation.")
    parser.add_argument("--prompt", type=str, required=True, help="Input prompt to generate a response.")
    return parser.parse_args()

def main():
    """
    Main function to generate a response using input arguments.
    """
    args = parse_arguments()
    
    # Extract arguments
    model_name = args.model_name
    prompt = args.prompt
    
    # Generate response
    response = generate_response(model_name, prompt)
    
    # Print the result
    print("Generated Response:\n", response)

if __name__ == "__main__":
    main()
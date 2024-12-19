import os
import argparse
from scripts.infer import generate_response
from scripts.blender_runner import run_blender_script
from scripts.geometry_utils import calculate_bounding_box
from scripts.config import CAMERA_ANGLES, BRIGHTNESS

def generate_blender_script(model_name, prompt):
    """Generate a Blender script based on the given model and prompt."""
    return generate_response(model_name, prompt)

def ensure_output_folder_exists(output_folder):
    """Check if the output folder exists, and create it if not."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def run_script_and_save_obj(script, obj_name, output_folder, blender_executable):
    """Run Blender script to save the generated .obj file."""
    ensure_output_folder_exists(output_folder)
    run_blender_script(
        script, obj_name, output_folder, [], [], (), blender_executable, save_obj=True
    )
    return os.path.join(output_folder, f"{obj_name}.obj")

def calculate_and_render_image(script, obj_name, output_folder, obj_path, blender_executable, brightness):
    """Calculate bounding box and render the image using Blender script."""
    ensure_output_folder_exists(output_folder)
    bounding_coords = calculate_bounding_box(obj_path)
    brightness_value = BRIGHTNESS.get(brightness, BRIGHTNESS["Very Dark"])
    run_blender_script(
        script,
        obj_name,
        output_folder,
        bounding_coords,
        CAMERA_ANGLES,
        brightness_value,
        blender_executable,
        save_image=True,
    )

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run Blender Script to Generate 3D Objects and Images.")
    parser.add_argument("--model_name", type=str, default="BlenderLLM", help="Model path to generate the script.")
    parser.add_argument("--prompt", type=str, required=True, default="Please drow a cube.", help="Text prompt to describe the object.")
    parser.add_argument("--obj_name", type=str, default="cube", help="Name of the generated object file.")
    parser.add_argument("--output_folder", type=str, default="images/cube", help="Folder to save output files.")
    parser.add_argument("--blender_executable", type=str, default="blender", help="Path to Blender executable.")
    parser.add_argument("--brightness", type=str, default="Very Dark", choices=BRIGHTNESS.keys(), help="Brightness level for the rendered image. Options: Very Bright, Bright, Medium Bright, Dark, Very Dark.")
    return parser.parse_args()

def main():
    args = parse_arguments()

    script = generate_blender_script(args.model_name, args.prompt)
    print(f"The bpy script of {args.obj_name} is:\n{script}")

    obj_path = run_script_and_save_obj(
        script, args.obj_name, args.output_folder, args.blender_executable
    )
    print(f"OBJ file saved at {obj_path}.")

    calculate_and_render_image(
        script, args.obj_name, args.output_folder, obj_path, args.blender_executable, args.brightness
    )
    print(f"Image rendered and saved in {args.output_folder} folder.")

if __name__ == "__main__":
    main()

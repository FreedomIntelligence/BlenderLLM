import os
import subprocess
import tempfile

def run_blender_script(script_content, name, output_folder, camera_locations, camera_rotations, brightness, blender_executable, save_obj=False, save_image=False):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_script:
        temp_script.write("import bpy\nimport os\nimport math\n")
        temp_script.write("bpy.ops.object.select_all(action='SELECT')\nbpy.ops.object.delete()\n")
        temp_script.write(script_content)

        if save_obj:
            temp_script.write(f"\nbpy.ops.wm.obj_export(filepath=os.path.join(r'{output_folder}', '{name}.obj'))\n")
        
        if save_image:
            i = 1
            for camera_location, camera_rotation in zip(camera_locations, camera_rotations):
                temp_script.write(f"""
# Create camera and light
camera = bpy.data.cameras.new('Camera')
cam_obj = bpy.data.objects.new('Camera', camera)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj
cam_obj.location = {camera_location}
cam_obj.rotation_euler = {camera_rotation}

# Lights
key_light_data = bpy.data.lights.new(name='Key_Light', type='POINT')
key_light_object = bpy.data.objects.new(name='Key_Light', object_data=key_light_data)
bpy.context.collection.objects.link(key_light_object)
key_light_object.location = ({camera_location[0]*1.2}, {camera_location[1]*1.2}, {camera_location[2]*1.2})
key_light_data.energy = {brightness[0][i-1]}

# Render settings
bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = os.path.join(r'{output_folder}', '{name}_view{i}.png')
bpy.ops.render.render(write_still=True)
""")
                i += 1

        script_path = temp_script.name

    command = [blender_executable, '--background', '--factory-startup', '--python', script_path]
    subprocess.run(command)
    os.remove(script_path)

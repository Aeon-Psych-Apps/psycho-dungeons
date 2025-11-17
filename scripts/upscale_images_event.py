import base64
import io
from PIL import Image, ImageSequence

def main(input):
    image_resource = input.get('image_resource', [])
    target_names = input.get('target_names', [])
    scale_factor = input.get('scale_factor', 2.0)
    target_size = input.get('target_size')  # optional: [width, height]
    max_upscale_width = input.get('max_upscale_width', 64)
    max_upscale_height = input.get('max_upscale_height', 64)
    fps = 15  # fallback for GIFs missing frame durations

    output_images = []

    for img_obj in image_resource:
        name = img_obj.get('name')
        contents = img_obj.get('contents')
        mime_type = img_obj.get('type', 'image/png')

        if name not in target_names:
            continue  # skip anything not requested

        image_bytes = base64.b64decode(contents)
        with Image.open(io.BytesIO(image_bytes)) as im:
            width, height = im.size

            # Skip scaling if already larger than allowed
            if width >= max_upscale_width or height >= max_upscale_height:
                new_width, new_height = width, height
                if getattr(im, 'is_animated', False) and im.format == 'GIF':
                    frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
                    durations = [frame.info.get('duration', int(1000 / fps)) for frame in ImageSequence.Iterator(im)]
                else:
                    frames = [im]
                    durations = None
            else:
                if target_size:
                    new_width, new_height = target_size
                else:
                    new_width = int(width * scale_factor)
                    new_height = int(height * scale_factor)

                # Clamp to max upscale limits
                if new_width > max_upscale_width:
                    new_width = max_upscale_width
                if new_height > max_upscale_height:
                    new_height = max_upscale_height

                if getattr(im, 'is_animated', False) and im.format == 'GIF':
                    frames = []
                    durations = []
                    for frame in ImageSequence.Iterator(im):
                        resized_frame = frame.resize((new_width, new_height), Image.Resampling.NEAREST)
                        frames.append(resized_frame)
                        durations.append(frame.info.get('duration', int(1000 / fps)))
                else:
                    frames = [im.resize((new_width, new_height), Image.Resampling.NEAREST)]
                    durations = None

            # Encode back to base64
            buffer = io.BytesIO()
            if getattr(im, 'is_animated', False) and im.format == 'GIF':
                frames[0].save(
                    buffer,
                    format='GIF',
                    save_all=True,
                    append_images=frames[1:],
                    loop=im.info.get('loop', 0),
                    duration=durations,
                    disposal=2
                )
            else:
                frames[0].save(buffer, format=im.format or 'PNG')

            upscaled_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            output_images.append({
                'name': name,
                'type': mime_type,
                'contents': upscaled_b64,
                'width': new_width,
                'height': new_height
            })

    return {'upscaled_images': output_images}

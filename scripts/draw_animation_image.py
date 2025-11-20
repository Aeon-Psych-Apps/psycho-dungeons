from PIL import Image, ImageSequence
import io
import base64

def main(input):
    dungeon_map = input.get('dungeon_map', {})
    char_class = input.get('class', 'Warrior')
    player_pos = input.get('player_pos')
    grid_width = input.get('grid_width', 7)
    grid_height = input.get('grid_height', 5)
    tile_size = input.get('tile_size', 50)
    fps = 15

    image_resources_array = input.get('image_resources', [])
    image_resources = {img['name']: img['contents'] for img in image_resources_array}

    logic_to_image = {
        'gray': 'Gray50.png',
        'player': 'player1_idle32.gif',
        'enemy': 'skeleton_enemy_idle.gif',
        'boss': 'vampire_enemy_idle.gif',
        'enemy_resolved': 'skeleton_enemy_death_still.gif',
        'npc': 'aeonpsEDM50.gif',
        'npc_resolved': 'Trans50.png',
        'rest': 'bed.png',
        'chest': 'Chest.gif',
        'chest_resolved': 'Chest_Open.gif',
        'trap': 'Trap50.gif',
        'trap_resolved': 'Trans50.png',
        'ladder': 'Ladder.png',
        'resolved_placeholder': 'Trans50.png'
    }

    # Assign correct player image by class
    if char_class == 'Warrior':
        logic_to_image['player'] = 'warrior_player_idle.gif'
    elif char_class == 'Rogue':
        logic_to_image['player'] = 'rogue_player_idle.gif'
    elif char_class == 'Mage':
        logic_to_image['player'] = 'skeleton_player_movement.gif'
    else:
        logic_to_image['player'] = 'skeleton_player_idle.gif'

    no_scale_images = {
        logic_to_image['ladder'],
        logic_to_image['trap'],
        logic_to_image['chest'],
        logic_to_image['chest_resolved']
    }

    non_looping_images = {
        logic_to_image['enemy_resolved'],
        logic_to_image['npc_resolved'],
        logic_to_image['chest_resolved'],
        logic_to_image['trap_resolved']
    }

    tile_frames = {}
    max_fg_frames = 1

    # --- Load and preprocess image resources ---
    for name, b64_content in image_resources.items():
        tile_bytes = base64.b64decode(b64_content)
        tile_image = Image.open(io.BytesIO(tile_bytes))

        frames, durations = [], []

        # Base scale to keep small images crisp but proportional
        base_scale = max(1, tile_size // min(tile_image.width, tile_image.height))

        # Shrink abnormally large images further
        max_dim = max(tile_image.width, tile_image.height)
        extra_shrink = 1.0
        if max_dim > tile_size:
            extra_shrink = tile_size / max_dim

        scale = base_scale * extra_shrink
        skip_resize = name in no_scale_images

        # --- Frame iteration ---
        for frame in ImageSequence.Iterator(tile_image):
            img = frame.convert('RGBA')
            if not skip_resize:
                new_w = int(frame.width * scale)
                new_h = int(frame.height * scale)
                img = (
                    img.resize((new_w, new_h), Image.NEAREST)
                       .resize((tile_size, tile_size), Image.NEAREST)
                )
            frames.append(img)
            durations.append(frame.info.get('duration', int(1000 / fps)))

        tile_frames[name] = {'frames': frames, 'durations': durations}
        if name in logic_to_image.values():
            max_fg_frames = max(max_fg_frames, len(frames))

    # --- Helper: frame selection ---
    def get_animation_frame(frames, durations, idx, loop=True):
        if not frames:
            return None
        if loop:
            return frames[idx % len(frames)]
        return frames[idx] if idx < len(frames) else frames[-1]

    # --- Background renderer ---
    def get_bg_tile(coord):
        room = dungeon_map.get(coord)
        gray_tile = tile_frames[logic_to_image['gray']]['frames'][0]
        composed = Image.new('RGBA', (tile_size, tile_size))
        composed.alpha_composite(gray_tile)  # always start with gray

        if room and room.get('visited'):
            base = tile_frames.get('RoomBase50.png', {}).get('frames', [gray_tile])[0]
            composed.alpha_composite(base)

            exits = room.get('exits', [])
            for direction, wall_file in {
                'north': 'WallN50.png',
                'south': 'WallS50.png',
                'west': 'WallW50.png',
                'east': 'WallE50.png'
            }.items():
                if direction not in exits and wall_file in tile_frames:
                    composed.alpha_composite(tile_frames[wall_file]['frames'][0])

        return composed

    # --- Foreground player renderer ---
    def get_fg_tile(coord, idx):
        if coord == player_pos:
            data = tile_frames[logic_to_image['player']]
            return get_animation_frame(data['frames'], data['durations'], idx, loop=True)
        return None

    # --- Overlay renderer (enemy, chests, traps, etc.) ---
    def get_overlay_tile(coord, idx):
        room = dungeon_map.get(coord)
        if not room or not room.get('visited'):  # Only render overlays in visited rooms
            return None

        rtype = room.get('type')
        resolved = room.get('resolved', False)
        overlays = []

        if rtype == 'exit' and not resolved:
            data = tile_frames[logic_to_image['boss']]
            overlays.append(get_animation_frame(data['frames'], data['durations'], idx, loop=True))

        ladder_tile = None
        if rtype == 'start' or (rtype == 'exit' and resolved):
            if logic_to_image['ladder'] in tile_frames:
                ladder_tile = tile_frames[logic_to_image['ladder']]['frames'][0]

        if rtype in ('enemy', 'npc', 'chest', 'trap', 'rest'):
            key = f'{rtype}_resolved' if resolved else rtype
            fname = logic_to_image.get(key, logic_to_image['resolved_placeholder'])
            if fname in tile_frames:
                data = tile_frames[fname]
                loop = fname not in non_looping_images
                overlays.append(get_animation_frame(data['frames'], data['durations'], idx, loop))

        if not overlays and not ladder_tile:
            return None

        composed = Image.new('RGBA', (tile_size, tile_size))
        for o in overlays:
            if o:
                composed.alpha_composite(o)

        if ladder_tile:
            lw, lh = ladder_tile.width, ladder_tile.height
            ladder_x = (tile_size - lw) // 2
            ladder_y = 0
            composed.alpha_composite(ladder_tile, (ladder_x, ladder_y))

        return composed

    # --- Frame composition loop ---
    frames_out = []
    for i in range(max_fg_frames):
        frame = Image.new('RGBA', (grid_width * tile_size, grid_height * tile_size))
        for y in range(grid_height):
            for x in range(grid_width):
                coord = f'{x},{y}'
                bg = get_bg_tile(coord)
                fg = get_fg_tile(coord, i)
                ov = get_overlay_tile(coord, i)

                composed = Image.new('RGBA', (tile_size, tile_size))
                composed.alpha_composite(bg)
                if fg and ov:
                    half = tile_size // 2
                    composed.alpha_composite(fg, ((half - fg.width) // 2, 0))
                    composed.alpha_composite(ov, (half + (half - ov.width) // 2, 0))
                else:
                    if fg:
                        composed.alpha_composite(fg)
                    if ov:
                        composed.alpha_composite(ov)

                frame.paste(composed, (x * tile_size, y * tile_size), composed)
        frames_out.append(frame)

    # --- Timing and output ---
    all_durations = [d for v in tile_frames.values() for d in v['durations']]
    avg_dur = int(sum(all_durations) / len(all_durations)) if all_durations else int(1000 / fps)

    buf = io.BytesIO()
    frames_out[0].save(
        buf,
        format='GIF',
        save_all=True,
        append_images=frames_out[1:],
        loop=0,
        duration=avg_dur,
        disposal=2
    )

    return {'final_map_image': base64.b64encode(buf.getvalue()).decode('utf-8')}

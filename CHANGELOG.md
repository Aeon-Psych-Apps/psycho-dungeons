[11/19/2025 01:49 MST]

### Features
- FEATURE: latest
    - - Added patch_notes page to manual
    - - Including patch notes log up to current patch, including those made before switch to github

- FEATURE: patch_notes
    - - Added patch_notes page to manual
    - - Including patch notes log up to current patch, including those made before switch to github


### Patches
- PATCH: Update loot_generator.py
    - - Updated drop chance for consumables. 50% potion, 25% antidote, 5% elixir to 50% potion, 25% antidote, 25% elixir.
    - - Fixed other minor inconsistencies with loot stat scaling

- PATCH: Update class Mage to skeleton in roll_player_stats.py
    - - Updated character class from mage to skeleton

- PATCH: Update patch_notes version 1.0.1
    - - Updated patch notes manual page for 1.0.1 changes

- PATCH: Update config.json
    - - Updated config to version 1.0.1
    - - Removed folder_id (story/client should now be overwriting anyways
    - - Removed patch url and auth. Patch system migrated off Tines to GitHub instance for better long term reliability.


### Misc
- Rename rogue__player_idle.gif to rogue_player_idle.gif
    - Fixed typo in the name

- Rename rogue_Idle.gif to rogue__player_idle.gif
    - Renamed rogue idle to player specific (right facing)

- Rename vampire_damage.gif to vampire_enemy_damage.gif
    - Rename vampire damage to enemy specific (left facing)

- Rename vampire_death.gif to vampire_enemy_death.gif
    - Renamed vampire death to enemy specific (left facing)

- Rename vampire_death_still.gif to vampire_enemy_death_still.gif
    - Renamed vampire death still to enemy specific (left facing)

- Rename vampire_idle.gif to vampire_enemy_idle.gif
    - Renamed vampire idle to enemy specific (left facing)

- Rename vampire_attack.gif to vampire_enemy_attack.gif
    - Renamed vampire attack to enemy specific (left facing)

- Delete images/test.jjj
    - Deleted the directory file creator (not needed anymore)

- Rename skeleton1_idle.gif to skeleton_enemy_idle.gif
    - Renamed skeleton1 idle to enemy specific (left facing)

- Rename skeleton1_death_still.gif to skeleton_enemy_death_still.gif
    - Renamed skeleton1 death still to enemy specific (left facing)

- Rename skeleton1_death.gif to skeleton_enemy_death.gif
    - Renamed skeleton1 death to enemy specific (left facing)

- Rename skeleton1_damage.gif to skeleton_enemy_damage.gif
    - Renamed skeleton1 damage to enemy specific (left facing)

- Rename skeleton1_attack.gif to skeleton_enemy_attack.gif
    - Renamed skeleton1 attack to enemy specific (left facing)

- Rename skeleton2_movement.gif to skeleton_player_movement.gif
    - Renamed skeleton 2 movement to player specific (right facing)

- Rename skeleton2_death.gif to skeleton_player_death.gif
    - Renamed skeleton 2 death to player specific (right facing)

- Rename skeleton2_damage.gif to skeleton_player_damage.gif
    - Renamed skeleton 2 damage to player specific (right facing)

- Rename skeleton2_attack.gif to skeleton_player_attack.gif
    - Renamed skeleton 2 attack to player specific (right facing)

- Rename skeleton2_idle.gif to skeleton_player_idle.gif
    - Renamed skeleton 2 idle to be player specific (right facing)

- Rename warrior_idle.gif to warrior_player_idle.gif
    - Renamed warrior image to be player specific (right facing)

- Delete manual/latest.json
    - wrong directory

- Update <file-name> via Tines

- Update build_patch.yml
    - Updated logic handling

- Update build_patch.yml
    - Updated changelog function

- Update build_patch.yml
    - Updated to include changelog

- Create CHANGELOG.md
    - Added initial change log markdown file

- Delete Changelog.md
    - Need to rename

- Create Changelog.md
    - Added initial change log md file

- Update build_patch.yml
    - Typo fixed

- Update build_patch.yml
    - Added display logo to images. Not sure if necessary, but the native Tines add image to resource includes it

- Update build_patch.yml
    - Updated

- Update build_patch.yml
    - Added access

- Update build_patch.yml
    - Import and run on Python instead

- Create build_patch.yml
    - Added github actions to automate the json versioning file

- Add files via upload
    - Added originally packaged images (whether the game actually used them or not)

- Create test.jjj
    - create directory for images

- Create developer_commentary.md
    - Added base developer commentary manual page

- Create developer_log_5.md
    - Added base developer log 5 manual page

- Create developer_log_4.md
    - Added base developer log 4 manual page

- Create developer_log_3.md
    - Added base developer log 3 manual page

- Create developer_log_2.md
    - Added base developer log 2 manual page

- Create developer_log_1.md
    - Added base developer log 1 manual page

- Create tips_and_tricks.md
    - Added base tips and tricks manual page

- Create death_and_revival.md
    - Added base death and revival manual page

- Create progression_and_scaling.md
    - Added base progression and scaling manual page

- Create town_and_shop.md
    - Added base town and shop manual page

- Create combat.md
    - Added base combat manual page

- Create dungeons.md
    - Added base dungeons manual page

- Create inventory_and_items.md
    - Added base inventory and items manual page

- Create stats_and_leveling.md
    - Added base stats and leveling manual page

- Create characters.md
    - Added base characters manual page

- Create getting_started.md
    - Added the base getting started manual page

- Create introduction.md
    - Added base introduction manual page

- Create update_combat_heal.py
    - Added base update combat heal python script

- Create upscale_images.py
    - Added base upscale images python script

- Create die_character_payload.py
    - Added base die character payload python script

- Create revive_character_payload.py
    - Added base revive character payload python script

- Create upscale_images_combat.py
    - Added base upscale images combat python script

- Create update_char_battle_loot.py
    - Added base update character battle loot python script

- Create upscale_images_battle.py
    - Added base upscale images battle python script

- Create update_char_enemy_gen.py
    - Added base update character enemy generator python script

- Create upscale_images_event.py
    - Added base upscale images event python script

- Create update_char_payload_event.py
    - Added base update character payload event python script

- Create update_char_payload_move_movement.py
    - Added base update character payload move movement python script

- Create update_char_payload_move_quick.py
    - Added base update character payload move quick python script

- Create update_char_dungeon_exit.py
    - Added base update character dungeon exit python script

- Create update_char_dungeon_map.py
    - Added base update character dungeon map python script

- Create update_char_town_rest.py
    - Added base update character town rest python script

- Create update_char_shop_equip.py
    - Added base update character shop equip python script

- Create update_char_shop_sell.py
    - Added base update character shop sell python script

- Create update_char_buy.py
    - Added base update character buy python script

- Create delete_character_payload.py
    - Added base delete character payload python script

- Create loot_generator.py
    - Added base loot generator python script

- Create create_player_payload.py
    - Added base create player payload python script

- Create roll_player_stats.py
    - Added base roll player stats python script

- Create draw_animation_image.py
    - Added base draw animation image python script

- Create map_generator.py
    - Added base map generator python script

- Create config.json
    - Add version 1.0 config

- Update README.md
    - Updated with work in progress details as well as backstory behind the project.

- Initial commit
    - ---

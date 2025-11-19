[11/18/2025 23:55 MST]

### Misc
- Update CHANGELOG & patch_notes for 11/18/2025 23:50 MST [skip ci]

- Update CHANGELOG & patch_notes for 11/18/2025 23:43 MST [skip ci]

- Create patch_notes.md
    - Added base patch notes manual page
    - Update build_patch.yml
    - Updated logic handling
    - Update CHANGELOG for main [skip ci]

- Update CHANGELOG.md

- Update CHANGELOG for main [skip ci]

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
    - Update latest.json and versioned JSON [skip ci]

- Update build_patch.yml
    - Typo fixed
    - Update build_patch.yml
    - Added display logo to images. Not sure if necessary, but the native Tines add image to resource includes it
    - Update latest.json and versioned JSON [skip ci]

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
[11/18/2025 23:50 MST]

### Misc
- Update CHANGELOG & patch_notes for 11/18/2025 23:43 MST [skip ci]
[11/18/2025 23:43 MST]


[test] - 11/18/2025 23:34 MST


[11/18/2025 23:31 MST]


[1763533446] - 11/18/2025 23:24 MST



# Patch 1.0.1 - 10/28/25 22:36 PST

# IMPORTANT
If you patched the game to version 1.0.1 (which you definitely did if you are reading this 😂), your game actually just broke since I'm a dummy and decided to use dynamic folder_id referencing in the game config file which is used at least in the "Get Saved Player List" Tines action about 4 actions after the last login page sequence and "Setup Player Profile Resource" action above the Character Create Page UI action. To get the game working again after patching, both the "Replace Game Config Resource" actions in the live patch branch of the workflow (the right side branch of the Trigger action "No Live Branch") need to have their builder payload formulas updated to: 
```
MERGE(patch_updater.body.config, {"folder_id": IF(create_game_resource_folder, create_game_resource_folder.body.id, FIND(list_resource_folders.body.folders, LAMBDA(folder, folder.name = "Psycho Dungeons")).id)})
```
Afterwards, re-patch the game, and should be all set!
Hopefully Tines will let me update the project natively for a fix for this (and other misc. and minor issues) before this gets published to the Tines Library. 🙏
Don't remember if this reference is used anywhere else in the workflow, have not been able to test enough. 
Also, patching may also break the client admin access menu for patching too due to how the throttle formula in the advanced disable option works. 🤦‍♂️ I think I fixed it server side, but this is an FYI if not.

Luckily, the reinstall game button should still work to get you back playing in the meantime on vanilla version 1.0.0! 


# Update Patch / notes:
- Increased drop rates for elixir consumables from 5% to 25% from the total chances of IF a consumable is dropped. So once a consumable is triggered to drop, there should be a 50% chance of it being a potion, 25% an antidote, and 25% an elixir.
- New characters now start with 1 elixir in inventory (up from 0)
- There is a bug where a character equipping HP increasing gear actually doesn't apply to the actual character's real HP, but effective HP (backend logic). This results in enemies thinking the player's character is a lot strong than reality, and may be way more difficult to beat. Until I can figure out if that is fixable from server side, I recommend (unfortunately) not to keep HP increasing gear equipped.




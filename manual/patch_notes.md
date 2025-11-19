[11/18/2025 23:16 MST]

### Features
- FEATURE: latest

- FEATURE: latest

- FEATURE: latest

- FEATURE: patch_notes

- FEATURE: patch_notes



### Patches
- PATCH: Update loot_generator.py

- PATCH: Update class Mage to skeleton in roll_player_stats.py

- PATCH: Update patch_notes version 1.0.1

- PATCH: Update config.json



### Misc
- update workflow logic

- updated workflow logic

- revert from incorrect workflow

- Update CHANGELOG & patch_notes for latest test build [skip ci]

- 

- updated workflow logic

- Restore patch notes from incorrect over write

- update the workflow logic

- Update latest changelog and patch notes [skip ci]

- 

- updated workflow logic

- Restore previous patch_notes that got overwritten

- updated workflow logic

- Update CHANGELOG & patch_notes for test [skip ci]

- 

- Update no commit messages

- Update CHANGELOG & patch_notes for test [skip ci]

- 

- fix commit issue?

- Button not showing up for some reason

- Updated test build_patch yml to hopefully fix and get the changelog and latest.json working

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

- - Updated drop chance for consumables. 50% potion, 25% antidote, 5% elixir to 50% potion, 25% antidote, 25% elixir.

- - Fixed other minor inconsistencies with loot stat scaling

- - Updated character class from mage to skeleton

- - Updated patch notes manual page for 1.0.1 changes

- - Updated config to version 1.0.1

- - Removed folder_id (story/client should now be overwriting anyways

- - Removed patch url and auth. Patch system migrated off Tines to GitHub instance for better long term reliability.

- - Added patch_notes page to manual

- - Including patch notes log up to current patch, including those made before switch to github

- - Added patch_notes page to manual

- - Including patch notes log up to current patch, including those made before switch to github

- Delete manual/latest.json

- wrong directory

- - Added patch_notes page to manual

- - Including patch notes log up to current patch, including those made before switch to github

- - Added patch_notes page to manual

- - Including patch notes log up to current patch, including those made before switch to github

- - Added patch_notes page to manual

- - Including patch notes log up to current patch, including those made before switch to github

- Update <file-name> via Tines

- 
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

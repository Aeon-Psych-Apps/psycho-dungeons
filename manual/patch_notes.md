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



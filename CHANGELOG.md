# Changelog
All notable changes will be documented here.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]
### Added
- Disclaimer to in game patch UI that downgrading to a game patch lower than the current story client UI version may cause the game to break.
### Changed
- Update Image References in draw_animation_image.py
    - Changed the naming references for images to reflect the updated naming schema
- mage class in draw_animation_image.py
    - updated the mage class assign to player to correctly reflect the change to skeleton
    - Previous players using the skeleton mage need to have their account config for the old "mage" character class under their account manually updated to have the new image references work for the skeleton character the new class is `Skeleton`. Deleting and remaking the specific character should also fix.
- Added enemy label to current dungeon map type
    Added enemy/boss label to current map type. This will now make it such that players leaving in the middle of a enemy/boss encounter will now resume once re-loading the game
- Updated Tines Story "client" UI v1.0.2
    - Updated image name reference logic (heal, battle, revive, combat, dungeon, town, shop) to account for Mage class change to Skeleton. Also improved the ability to potentially introduce new character/class types and/or re-use character graphics between player/enemy.
    - Integrated the helper web apps (script/image resource manager) to the game client instead of separate web apps. These should only be accessible by users signed into the Tines tenant hosting the game client. This integration also has the benefit of reducing the required licensed flows to 1.
    - Updated the Patch service UI to allow switching between historical patch versions. Although not very useful as some patch versions are dependent on specific client UI versions to run.
    - Switched patch server URL to GitHub repository.
    - Fixed a minor issue where each action in the login page would attempt to login to the game regardless of the action taken, resulting in an extra event output as well as error.
    - Updated the Email invite UI to automatically submit. Reducing account invite process by a minimum of 5 seconds.

### Deprecated
- Tines Story version 1.0.1 and lower are now deprecated.
    - A new story UI needs to be imported/patched in order to completely use this and future patches with minimal issues.
### Removed
### Fixed
- syntax error in update_char_enemy_gen.py script
    - Fixed a syntax error causing the script to fail
- syntax errors in update_combat_heal.py script
    - fixed syntax errors in the combat heal script that would cause failures
- Syntax in update_char_payload_move_quick.py
    Fixed syntax error causing fail in script
- Syntax error
    Fixed the syntax error from the previous change to enemy/bass labeling change
- Syntax in update_char_shop_equip.py script
    Fixed bad syntax in script for processing shop equipping feature that resulted in failed execution.

### Security
### Known Issues / Bugs
- Status effects/bonuses do not apply for either enemies nor players regardless of status indication in the UI. This mechanic will be modified and introduced at a later date.
- HP increasing gear may not correctly apply to the player when equipped, but still be calculated internally for damage calculation. This results in an outcome where enemies may be stronger than they should be (enemies scale against player stats). Advise is to not equip HP increasing gear until a fix is confirmed. 
### Misc
- Update CHANGELOG.md
- Update CHANGELOG.md

---

### v1.0.1 - [2025/11/19 01:49 MST]

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

- Update build_patch.yml
    - Added display logo to images. Not sure if necessary, but the native Tines add image to resource includes it

- Add files via upload
    - Added originally packaged images (whether the game actually used them or not)

---

### v1.0.0 - [2025/10/28]
- Initial commit






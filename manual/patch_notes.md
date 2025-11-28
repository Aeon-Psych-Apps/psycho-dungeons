1.0.2 - [2025/11/27]

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
    - Fixed syntax errors in the combat heal script that would cause failures
- Syntax in update_char_payload_move_quick.py
    - Fixed syntax error causing fail in script
- Syntax error
    - Fixed the syntax error from the previous change to enemy/bass labeling change
- Syntax in update_char_shop_equip.py script
    - Fixed bad syntax in script for processing shop equipping feature that resulted in failed execution.

### Security
### Known Issues / Bugs
- Status effects/bonuses do not apply for either enemies nor players regardless of status indication in the UI. This mechanic will be modified and introduced at a later date.
- HP increasing gear may not correctly apply to the player when equipped, but still be calculated internally for damage calculation. This results in an outcome where enemies may be stronger than they should be (enemies scale against player stats). Advise is to not equip HP increasing gear until a fix is confirmed. 
### Misc
- Update CHANGELOG.md







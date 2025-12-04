# psycho-dungeons
Psycho Dungeons - An RPG dungeon crawler game made by Tyler Wong / Tines with Tyler under the Aeon Psych / "Aeon Apps" branding and also built fully within and hosted with [Tines](https://www.tines.com/) no/low code automation platform. This is a game where players can pick between 3 different character types and descend into the dungeon... A randomly generated labyrinth with scattered enemies, traps, chests, and bystanders. Fight enemies to level up their characters and find dynamically generated gear to equip to make themselves even stronger!

![Psycho Dungeons Title Screen Animated](https://github.com/user-attachments/assets/5ff5d147-dd74-4776-9934-2fc227d85cb1)

# About The Project  
Psycho Dungeons was created for the sole purpose of competing in the ["You Did What?! With Tines" Fall 2025](https://www.tines.com/you-did-what-with-tines/fall-2025/) community competition. It was designed to push the limits (both personally and with the platform) to see what was possible/capable to do fully within the platform. As such, everything was created within, hosted, served, played via the Tines platform. For submission, even the patch service was contained within Tines, but I have decided it was not best for longterm reliability/stability and have thus created this repo to host the patch server/service as well as function as a public landing page of sorts for the game/app. Additionally, some updates to the game may be made that would require a re-import of the JSON story file, which hosting the updated file here would also accomplish (something I did not originally think possible to do fully contained within the original story / patch service, but is something I am currently playing around with to see if it actually is possible).

The winners were announced in November 2025, and Psycho Dungeons won best "Build Interactive Apps" category!

![Psycho Dungeons Tines YDWWT Fall 2025 Build Interactive Apps Winner](https://github.com/user-attachments/assets/f623959f-f217-4dd3-8935-afbb6bd8e4fc)

# About The Game  
Players play through a Tines tenant hosted client via a public page URL. The game is an event based game (the game is not realtime, but instead only progresses when the player picks an action) in the style of an RPG rogue-like dungeon crawler, where a player can choose between 3 different character classes with different stats and explore randomly generated dungeons with different event types. During play, players are also able to get dynamically generated gear from events and/or as drops from defeated enemies/bosses. Dynamic and randomness of the game allows for increased replayability along with the fact that a lot of the game is capable of being patched and/or updated with new features and content.

# How To Install
The latest Psycho Dungeons JSON Story file should be downloaded from the main branch of this repo and then inported as a new story into a [Tines](https://www.tines.com/) tenant.

For brand new installs:
- Once imported, open up the story as an admin user and create and link a Tines API credential to the story (This can easily be done by looking in the right tab settings of the story under Credentials section "Psycho Games API Key"). Search for and create a new "Tines" credential. Select at least a Team or higher access level and follow the rest of the prompts. Keeping the same name "Psycho Games API Key" may not be necessary, but recommended. With a sufficient permissioned Tines API key attached to the story, the game is now technically installed and runnable/playable from the top most page action URL in the story "Game Login". The default URL will be something like this `(tines_tenant_url_game_is_installed_on).tines.com/pages/psycho-dungeons/` The story should come packaged with the most recent game version that was released at time of story export so it may still be necessary to use the in game patch service to update before playing.

For re-imports on previously working installs:
- The current story in the Tines tenant just needs to be replaced with the latest version story from this repo and then have an admin patch to the latest production release in game client. A story only needs to be re-imported if the story has been updated compared to the previous story, otherwise the game can just be patched via the patch service. If you kept the Tines API key and default game login URL the same from your initial install configuration, no further action should be needed and the game should still be live and playable via whichever URL you accessed it previously. Sometimes (will try to make these rare, if never) updates to the story "UI" may break/deprecate older code that is already embedded into player accounts' "saved games". These issues will usually require manual fixes from a tenant/game admin into each player's saved game profile resource(s) and/or a remake of players' accounts either by deleting their full account resource file and/or the individual characters within their account. I don't currently know of a way to avoid this from happening. The final step for re-importing may be best to reinstall the game via the in game login admin menu. This should put you on the correlated working patch file for the specific story UI version. If wanted, could also patch up to the highest level game version that the story UI supports.

# Minimum requirements
The minimum requirements (as of November 2025) for running this game in your own Tines tenant is:
- At least 1 licensed flow available
- At least 1 send email event (to create a game account) available
- Enough tenant/story events available for as long as you (including other concurrent players) whish to play the game, factoring in any other story events outside of the game story. Events can be cleared manually to continue playing if event limits are hit.

# Socials  
This is my first "production" GitHub that I made specifically to host this project with since learning that it could also function as a better patch and maintenance server. Originally, the patch server was fully contained within Tines, but I thought it was not optimized for long term viability based off current limitations/implementation).

If you have any comments or want to support, leave a message on here or find me on social media:  
[Tines with Tyler | Instagram](https://www.instagram.com/tineswithtyler/)  
[Tines with Tyler | YouTube](https://www.youtube.com/@tineswithtyler)  
[Insane Asylum (my public/community Discord) | Discord](https://discord.gg/wHwKj7k)  
[tylertwong.com | Website](https://tylertwong.com)

I can also provide an invite to my personal hosted instance of the game via private request (my instance is not setup for mass player account invites and/or concurrent players, so I have to limit access in case this project gets popular.

# Images  
![Psycho Dungeons Create Character Screen Animated](https://github.com/user-attachments/assets/5bcc7591-5346-438b-9a97-0de979061df2)  
![Psycho Dungeons Town Animated](https://github.com/user-attachments/assets/0133b5f0-125c-4a33-8db9-ac3ef461ce50)  
![Psycho Dungeons Shop](https://github.com/user-attachments/assets/4155b919-fee1-4fbf-bb75-245ce8b011fe)  
![Psycho Dungeons Enemy Room Animated](https://github.com/user-attachments/assets/e9577d0d-c4eb-46ac-ab3e-9b7e8c32f94f)  
![Psycho Dungeons Enemy Battle Animated](https://github.com/user-attachments/assets/4795ad45-764c-48bb-97d4-53310823e591)  
![Psycho Dungeons Enemy Battle Attack Animated](https://github.com/user-attachments/assets/9dd4d437-f889-4611-acea-4391ef89ece8)  
![Psycho Dungeons Enemy Battle Attack K Animated](https://github.com/user-attachments/assets/806fceea-829d-4152-9549-f062ab5e925f)  

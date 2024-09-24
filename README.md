# osu!scorepost

This is osu!scorepost, the quickest and easiest way to generate a scorepost for sharing on r/osugame and becoming a part of osu! history!

A generated scorepost includes a post title and an image that replicates a screenshot of the osu! results screen. Here's an example:

![Example scorepost](/app/static/example.gif)

This scorepost was generated with just a score link, [https://osu.ppy.sh/scores/1777987420](https://osu.ppy.sh/scores/1777987420), and a single click!

The project can be accessed at [https://osuscorepost.wesleyxie.com/](https://osuscorepost.wesleyxie.com/).

## Features
* A scorepost can be generated for all 4 gamemodes
* Supports Ranked, Qualified, Loved, Graveyarded, and WIP maps
* Option to enter a custom message to scorepost title
* Toggle auto mode to automate copying screenshot, opening Reddit with scorepost title already typed in as soon as the scorepost is generated
* Click the r/osugame button (or use shortcut CTRL/CMD + D) to open the [submissions page](https://www.reddit.com/r/osugame/submit/?type=IMAGE) of r/osugame, the scorepost title is already written for you
* Clipboard button to easily copy the generated scorepost title
* Shortcut (CTRL/CMD + S) to copy the scorepost screenshot
* All scoreposts titles matches the [criteria]("https://www.reddit.com/r/osugame/wiki/scoreposting/") set on r/osugame


## Usage
 Here are three ways to generate a scorepost:
1. **Using a Score Link (e.g., https://osu.ppy.sh/scores/2803336922):** \
Simply enter a score link to generate a scorepost. Even links in the "old ID" format work (e.g., [https://osu.ppy.sh/scores/osu/4100884541](https://osu.ppy.sh/scores/osu/4100884541)). Just make sure the full link is entered correctly, without omitting "osu.ppy.sh."

2. **Using a User Profile Link (e.g., https://osu.ppy.sh/users/26080649):** \
Entering the link to a user's profile will generate a scorepost of that user's most recent score (even if it's a failed attempt!). You can also specify the game mode by using links that include the game mode in the URL (e.g., [https://osu.ppy.sh/users/4504101/taiko](https://osu.ppy.sh/users/4504101/taiko)).
3. **Using a Username (e.g., lifeline):** \
Entering just a username will also generate a scorepost of the user's most recent score! This method will only work for the user's default game mode.

### Auto Mode:
On the top right of the screenshot image, there is an option to toggle "Auto Mode". When Auto Mode is on, the app will copy your screenshot to your clipboard, and open Reddit in a new tab with your generated scorepost title already written in! All you would have to do is set the flair to "Gameplay," paste (CTRL/CMD + V) the screenshot, and click post!

![Example post](/app/static/auto_mode.gif)

## Setup

### Prerequisites 
- Python3 (version 3.12.4 or 3.12.5)
- pip (Python package installer)

### Steps
1. Clone the repository: 
```
git clone https://github.com/wesleyyxie/osu-scorepost.git
cd osu-scorepost
```
2. Install requirements
```
pip install -r requirements.txt
```
3. Copy your API key, and create a Client to get Client Secret and Client ID from your [osu! profile settings](https://osu.ppy.sh/home/account/edit#oauth).<details><summary>Further Instructions</summary><ul>
    <li>
        Scroll to new the bottom and click "New OAuth Application" in the OAuth section and give it any name you want. Copy the client ID and client secret for later.
    </li>
    <li>
        Under the "Legacy API" tab, create an API key.
        The application name can be anything and the URL can be any localhost (e.g. http://localhost:5000/). Copy the API key for later.
    </li>
</ul>
</details>

4. Create a file called `.env` in the repository folder and paste your API Key, Client Secret, and Client ID accordingly.
```
CLIENT_ID = # Paste Client ID
CLIENT_SECRET = # Paste Client Secret
API_KEY = # Paste API key
```
5. Start the Development Server
```
cd app
python main.py
```
## Limitations
- Unfortunately, scores that are not the user's best on the map will not display the Geki and Katu counts.
- Geki and Katu counts for Taiko scores are not available yet.
- Differentiating between S-Ranks with sliderbreaks and FC's with some sliderend drops is not perfect. This is because the osu! API does not differientiate between the 2 scenarios. The current temporary solution is that a score that has a 0 miss count and a max combo of more than or equal to 20 less than the beatmap's max combo is counted as an FC. (TLDR: A score is counted as an FC if score max combo >= beatmap max combo - 20)
- The generated screenshot is not draggable
- Screenshot generator can only use the beatmapset background instead of beatmap background.
- This website is still in the early stages of development, so there may be bugs. Please report any issues, and I'll address them as soon as possible.

## Sample Posts
Here are some examples of real scoreposts on Reddit that I have created using this website. This will help assure you that they meet the scorepost criteria for r/osugame.

- [https://www.reddit.com/r/osugame/comments/1ew5hin/abyssal_pathfinder_the_whisper_of_ancient_rocks/](https://www.reddit.com/r/osugame/comments/1ew5hin/abyssal_pathfinder_the_whisper_of_ancient_rocks/)
- [https://www.reddit.com/r/osugame/comments/1eqk6v7/sytho_xi_over_the_top_expert_nc_tynamo_1035_9627/](https://www.reddit.com/r/osugame/comments/1eqk6v7/sytho_xi_over_the_top_expert_nc_tynamo_1035_9627/)
- [https://www.reddit.com/r/osugame/comments/1f0hkss/lexu2s_mitsukiyo_unwelcome_school_sotarks/](https://www.reddit.com/r/osugame/comments/1f0hkss/lexu2s_mitsukiyo_unwelcome_school_sotarks/)

## Acknowledgements
- The skin used for the results screen is [Aristia(Edit)](https://skins.osuck.net/skins/485?v=0).
- All icons are from [FontAwesome](https://fontawesome.com/icons)
- Performance points calculation: [rosu-pp-py](https://github.com/MaxOhn/rosu-pp-py)
- osu!api: [ossapi](https://github.com/tybug/ossapi)
- Geki and Katu count from replay data: [circlecore](https://github.com/circleguard/circlecore)

## Contact
Feel free to reach out to report any bugs or ask any questions

- osu! profile: [sm4ko](https://osu.ppy.sh/users/26080649)
- Reddit: [dopeapple](https://www.reddit.com/user/dopeapple/)
- Discord: smaako

## License
osu!scorepost is released under the [GNU General Public License v3.0](https://github.com/wesleyyxie/osuScorepost/blob/main/LICENSE). See `LICENSE` for more info.

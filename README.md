# osu!Scorepost

This is osu!scorepost, the quickest and easiest way to generate a scorepost for sharing on r/osugame and becoming a part of osu! history!

A scorepost includes a post title and an image that replicates a screenshot of the osu! results screen. Here's an example:

**9MlCE | VINXIS - Sidetracked Day [Infinity Inside] +HDDT (DendyHere, 10.50\*) 96.69% FC #1 | 1711pp**
![Example scorepost](/app/static/example.jpg)

This scorepost was generated with just a score link, <a  target="_blank"  href="https://osu.ppy.sh/scores/1777987420">https://osu.ppy.sh/scores/1777987420</a>, and a single click!

## Usage
### Here are three ways to generate a scorepost:
1. **Using a Score Link (e.g., https://osu.ppy.sh/scores/2803336922):** \
Simply enter a score link to generate a scorepost. Even links in the "old ID" format work (e.g., <a  target="_blank" href="https://osu.ppy.sh/scores/osu/4100884541">https://osu.ppy.sh/scores/osu/4100884541</a>). Just make sure the full link is entered correctly, without omitting "osu.ppy.sh."

2. **Using a User Profile Link (e.g., https://osu.ppy.sh/users/26080649):** \
Entering the link to a user's profile will generate a scorepost of that user's most recent score (even if it's a failed attempt!). You can also specify the game mode by using links that include the game mode in the URL (e.g., <a  target="_blank"  href="https://osu.ppy.sh/users/4504101/taiko">https://osu.ppy.sh/users/4504101/taiko</a>).
3. **Using a Username (e.g., lifeline):** \
Entering just a username will also generate a scorepost of the user's most recent score! This method will only work for the user's default game mode.

### After your scorepost is created
* You can easily copy the title to your clipboard by clicking the clipboard icon located right next to the scorepost title.
* If your screenshot was created, you can click the Reddit logo in the navigation bar to open the r/osugame submit page in a new tab, then simply drag the generated screenshot into the image drop field.
* Paste your copied scorepost title into the post title field on Reddit, set the flair to "Gameplay," and click "Post!"

## Features
* A scorepost can be generated for all 4 gamemodes! (osu!, osu!mania, osu!taiko, and osu!catch)
* Click the r/osugame button to conveniently open the submit post page of r/osugame
* Clipboard button to easily copy the generated scorepost title
* All scoreposts titles matches the <a target="_blank" href="https://www.reddit.com/r/osugame/wiki/scoreposting/">criteria</a> set on r/osugame

## Setup

### Prerequisites 
- Python (version 3.12.4) 
- pip (Python package installer)

### Steps
1. Clone the repository: 
```
git clone https://github.com/wesleyyxie/osuScorepost.git
cd osuScorepost
```
2. Install requirements
```
pip install -r requirements.txt
```
3. Get an API key, and create a new Client with a Client Secret and Client ID from your [osu! profile settings](https://osu.ppy.sh/home/account/edit#oauth).
4. Paste your API Key, Client Secret, and Client ID into the `.env` file located in the root folder of the repository.
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
- This website is still in the early stages of development, so there may be bugs. Please report any issues, and I'll address them as soon as possible.

## Credits
- The skin used for the results screen is [Aristia(Edit)](https://skins.osuck.net/skins/485?v=0).
- All icons are from [FontAwesome](https://fontawesome.com/icons)

## Internals
- Performance points calculation: [rosu-pp-py](https://github.com/MaxOhn/rosu-pp-py)
- osu!api: [ossapi](https://github.com/tybug/ossapi)
- Geki and Katu count from replay data: [circlecore](https://github.com/circleguard/circlecore)

## License
osu!scorepost is released under the [GNU General Public License v3.0](https://github.com/wesleyyxie/osuScorepost/blob/main/LICENSE). See `LICENSE` for more info.
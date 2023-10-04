
# Spotify Mixer

An open-source tool to generate new playlists from existing ones by your own rules.

WIP

The goal of this program is that the user defines rules, in which it defines a source playlist (the user must have at least read-only access to it), some rules and the result will be a new playlist, uploaded to the Spotify account of the user, which is a "remixed" version of the original one, thus having a playlist, which is not all random as it has predefined ratios. Rules have a type (e.g. year), a min and a max parameter (if any of that is left empty, the interval is open on one way) and a probability (see below). For a better view see the prepared settings.py in the source code.

For a more detailed view, here is the idea of how the program works:
The rules define a tree-like data structure. On top of the tree is a rule with a "ROOT" type. This is the only ROOT typed rule, as its only purpose is to contain the user defined rules as subrules, the children of the node. Only the leaves contain songs. The way we decide which song is next is that we start from ROOT, on every level we generate a random number between 1 and 100 which decides which child node we choose (the probability of every rule must be between 1 and 100 and the probabilities of the children of a node must add up to 100), and we repeat this until we reach a leaf, where we pick a random song. We continue this until the newly generated playlist reaches its desired length.

The current feature set works well, if you create a Spotify application on the developer dashboard and enter the credentials in the settings file it will work, however, it could use some polish (enter settings in a JSON file instead of a Python constructor, more verbosity, authentication will successfully finish only on Windows right now) and some new features (author as rule type).

## Available settings:
### Rules:
 - Type: YEAR/POPULARITY (a number between 0 and 1)
 - min
 - max
 - (between min and max the user has to choose at least one, they are both inclusive)
 - finishBeforeRepeat: It decides if the program picks songs from a node purely random (False) or if it has to use up all songs before picking an already selected song in/under the node (True).

### Related to the whole generated playlist:
 - name
 - source: Spotify ID of the source playlist, or "liked" if the source is the liked songs of the user
 - length: The desired length of the playlist, if -1 then the program will generate until it uses up all of the songs of the source, this may generate playlists which are longer than the current limitations of Spotify.

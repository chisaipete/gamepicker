# Game Picker

The objective of the game picker is to create an aggregate PC game library from which to select a random game to play. We'd like to support all game libraries, with a fallback to a local flat file.

Also, would like to select a game which hasn't been selected previously. 

This needs to support multiple apis for each type of digital distribution platform.  Each should return a current game listing.

We should securely handle credentials, so as not to compromise the user's data.

## Services Supported, and Possible Methods

We could just add all our games to Steam.  This is cop out solution.  
Just use a list--brute force!  

### Steam

- Multiple packages (authentication?)

### Humble Bundle

- Non DRM titles (non-Steam, i.e. Humble Trove)

### GOG

- A package

### Epic Games

- Research Needed

### Twitch

- Research Needed (Fruitful)

### Ubisoft

- Research Needed

### Bethesda

- Research Needed

### Other

- Custom list of games that don't fit these categories
- Games I could still play (because I have the disk)

## Structure & TDD Planning

Main -> [ Distributor(steam, gog, hb, ...) -> get_library() ] -> uniquify && combine -> random selection -> present to user

# Getting Started
- Have Python 3.* as default version on OS (`python`)
- At base of repository run: 
    + `python -m venv venv`
    + Activate your venv: `. ./venv/bin/activate`
    + `pip install --upgrade pip`
    + `pip install -r requirements.txt`
- Use the following shebang: `#!/usr/bin/env python`
- Before running any script, activate your venv: `./venv/bin/activate`
- Before releasing, use pip freeze > requirements.txt
    + remove `pkg-resources` line from requirements.txt
- To run tests: `python -m unittest discover`
- To run tests with coverage: `coverage run -m unittest discover`
- To generate coverage report: `coverage html --omit="*/venv*"`
- View report by opening: `./htmlcov/index.html`
- You'll need to provide credentials for each piece of the flow to work
    + Oauth tokens will be used for most authetication
- These credentials should be stored in *.cred files in the `credentials` directory
- At work, you'll need to `set http_proxy=http://...` and `set https_proxy=http://...` to punch through that proxy
- Also, in a Windows terminal, you may encounter issues when echoing unicode characters for debug purposes, so execute the following: `chcp 65001`

Now all scripts should reference the version of python in that venv, install all additional libs from that path

`python -m pip install git+https://github.com/MestreLion/humblebundle.git`

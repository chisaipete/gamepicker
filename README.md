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



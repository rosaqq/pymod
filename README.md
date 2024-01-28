# pymod
modular python bot under development  
requires [discord.py](https://github.com/Rapptz/discord.py/tree/async)

The idea behind pymod for it to be a generic bot that allows the user to easily extend and customise it's functionality by adding modules, which will then be automatically recognised and loaded by the core file.  

"ExampleMod.py" inside the "mods" folder provides an example how these modules should be structured:  
* One class per file, with the same name as the file;
* Class must have a static rank variable, an int set to the minimum rank users must have to access the commands inside it;
* Class must have a static help_dict variable, a dictionary with keys for every command inside the class and a description of what they do for values;
* Class must have an \_\_init__ method that takes client and message as arguments;
* All the commands inside the class must be coroutine functions.


TODO:  
- [ ] Make help command completely docstring based;
- [x] Get rid of the triple-quoted voice bot & turn it into a voice module;
- [ ] Make sure pymod taking complete advantage of the asynchronous marvel;
- [ ] Alias support for private messages?

Requires pymod.ini file locally - example:
```
[GENERAL]
adminID     = 999
adminID2    = 998
[AUTH]
token = ...
```
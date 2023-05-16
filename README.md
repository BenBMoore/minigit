# What?
Creating a small project that implements a small subset of a the basic features of git in python to get a better understanding of how it all works behind the scenes.
Following the amazing tutorial from https://www.leshenko.net/p/ugit/ - and adding further functionality (mainly through the use of pathlib)

# Install 
Clone the repo

Install locally using `pip -e .`

# Commands
`minigit init ` Initializes the .minigit directory 

`minigit hash-object <filepath>` Creates a SHA256 hash of the file

`minigit cat-file <filepath>` Point this to the file within the objectstore (.minigit/object/<file>) to read the contents

`minitgit write-tree` Creates a tree based hashed file structure of the current directory

`minitgit read-tree` Recreates the original files/file structure based on what's currently stored in the object store
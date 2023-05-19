# simple python to-do list

this is an extremely barebones to-do list app, that will hopefully become a
little more full-featured as I go, without getting too bloated.

for now:

```sh
-a --add        adds a new to do list item with the following STR as the title
-e --edit       edits an existing item with the following INT being the ID of the
                item to edit
-p --priority   sets the priority of the item being added or edited
                ["none", "low", "medium", "high"]
-s --status     sets the status of the item being added or edited
                ["to-do", "done", "in-progress", "on-hold"]
-d --done       sets an item's status to done with the following INT being the
                ID of the item to set
```

# SUAS-2023
Do not change SUAS_Code unless you intend to change the main SUAS repository. Because it is a git submodule, any changes in there will affect the main SUAS repository. Submodules are useful because that way we can stay up to date with changes in the SUAS vision and flight code, but try not to accidentally delete everything. When programming new simulation code, do it outside of the SUAS_Code file.  

If you find you have cloned this branch and SUAS_Code is empty, do "git clone --recurse-submodules" or "git submodule update --init --recursive"

To update this branch the newest SUAS code do: "git submodule update --remote" then commit and push after testing

TODO: Find a simpler alternative to git submodules
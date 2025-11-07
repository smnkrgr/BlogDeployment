# Posting from Obsidian
Jekyll can take markdown files and translate it into a static HTML page.
However, Obsidian does have some differences with how it includes images into a note.
I therefore created a script that reads notes from a specific folder in your Obsidian vault, converts image links to the standard markdown format and copies both note and images to the respective Jekyll folders.
You can find the script and a configuration template in this folder of the repository.
Copy the template to `config.yaml` and enter your folders:
```
cp config_template.yaml config.yaml
vim config.yaml
```
After specifying your folders, you can create a test note in Obsidian and execute the Python script to test it:
```
python3 convert_obsidian_to_jekyll.py
```
If everything looks as expected it can be pushed to your repository, where the workflow automatically updates your blog.
This could be further automated by triggering the script from within Obsidian or creating bash scripts that push right away.

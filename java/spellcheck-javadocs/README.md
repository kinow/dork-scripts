Spell checks Java javadoc blocks in classes, constructors, and methods.

Uses javalang to parse and retrieve a tree from a Java file. BeautifulSoup
is used to extract HTML. PyEnchant is used for tokenizing (it's used in
mwic as well). And mwic is the spell checker.

You must execute the script in the java project folder. It will expand the
glob *.java recursively, then parse, and print the output in the console.

Licensed under the MIT licence. See TODO for pending issues.

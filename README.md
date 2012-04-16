# GoToDoc
GoToDoc is a Sublime Text 2 plugin to quickly open Go programming language document in your browser 
base on the selected packages, functions, types and keywords in Go source file.


## Usage
GoToDoc supports 2 modes to open the corresponding document in your web browser

### Exact Mode: (Windows/Linux: Ctrl+Alt+E, OSX: Super+Ctrl+E)
Go to the exact package document at http://golang.org/pkg for standard or http://gopkgdoc.appspot.com for non-standard
Package alias is supported, it's automatically looked up in the imported package list.

### Lucky Mode: (Windows/Linux: Ctrl+Alt+L, OSX: Super+Ctrl+L)
Google search on golang.org and go to the first result using "I'm Feeling Lucky".

Besides shortcut, you can access from menu `Tools -> GoToDoc`

## Installation
You can install from github.com, or using Sublime Text 2 Package Control

### From Github
	$ cd ${ST2_Package_Folder}
	$ git clone git://github.com/jtdeng/GoToDoc.git GoToDoc

### Using Package Control
	TODO


## Settings
You can customize the key bindings of GoToDoc by going to the menu `Preferences -> Package Settings -> GoToDoc -> Key Bindings - Default`. 

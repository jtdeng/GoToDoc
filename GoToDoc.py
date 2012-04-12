import sublime, sublime_plugin
import webbrowser

# 1. go to only package document at http://golang.org/pkg/
# 2. google search on golang.org and go to the first result like "I'm Feeling Lucky"
# 3. 

class GoToDocCommand(sublime_plugin.TextCommand):
	
	def description(self):
		return 'A Sublime Text 2 plugin to quickly open go package document base on the selected text'

	def get_full_pkg_name(self, edit):	
		'''Try to find the full package name in go import statement'''
		pass

	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, World!")
		sels = self.view.sel()
		for sel in sels:
			#print(self.view.substr(sel))
			webbrowser.open_new_tab('http://golang.org/pkg/' + self.view.substr(sel))
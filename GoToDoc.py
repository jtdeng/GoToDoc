import sublime, sublime_plugin
import webbrowser
import re

GO_KEYWORDS = { 
	'if':'If_statements',			'break':'Break_statements',        
	'default':'Switch_statements',	'func':'Function_declarations',         
	'interface':'Interface_types',	'select':'Select_statements',
	'case':'Switch_statements',		'defer':'Defer_statements',
	'go':'Go_statements',			'map':'Map_types',   
	'struct':'Struct_types',		'chan':'Channel_types',
	'else':'If_statements',			'goto':'Goto_statements',  
	'package':'Packages',			'switch':'Switch_statements',
	'const':'Constant_expressions',	'fallthrough':'Fallthrough_statements',  
	'type':'Type_declarations',		'continue':'Continue_statements',     
	'for':'For_statements',			'import':'Import_declarations',
	'return':'Return_statements',	'var':'Variable_declarations',
	'range':'RangeClause'
}

GO_BUILTINS = ['append','close','delete','panic','recover','ComplexType','complex',
				'FloatType','imag','real','IntegerType','Type','make','new','Type1', 
				'bool','byte','complex128','complex64','error','float32','float64',
				'int','cap','copy','len','int8','int16','int32','int64','rune','string',
				'uintptr','uint','uint8','uint16','uint32','uint64']


def get_imports(src):
	''''build a list of imported packages from src, each tuple is (pkg_alias, pkg_path)
		[('', 'compress/bzip2'), ('E', 'errors'), ('.', 'archive/tar'), ('_', 'database/sql/driver')]
	'''
	single_import_pattern = ''' import \s+ (\w+|\.){0,1} \s* "(.*?)"  '''
	single_imports = re.findall(single_import_pattern, src, re.M | re.X | re.S)

	multi_import_pattern0 = '''import \s* \(  (.*?) \)'''
	multi_imports0 = re.findall(multi_import_pattern0, src, re.M | re.X | re.S)

	multi_import_pattern = ''' (\w+|\.){0,1} \s* "(.*?)"  '''
	multi_imports = re.findall(multi_import_pattern, ''.join(multi_imports0), re.M | re.X | re.S)

	return single_imports + multi_imports


def get_full_pkg(imports, pkg):
	'''get full pkg path like "encoding/json" for json, pkg could be an alias'''
	for alias, fpkg in imports:
		#print alias, fpkg
		if pkg in (alias, fpkg, fpkg.split('/')[-1]): 
			return fpkg
		
	return ''		


def get_pkg_doc_url(view, sel):
	'''return pkg doc url for the selected obj in src'''
	region = sublime.Region(0, view.size())
	src = view.substr(region)
	imports = get_imports(src)
	#print imports

	selected = view.substr(sel)
	pkg,typ = '', ''
	if selected[0].isupper() and view.substr(sel.begin()-1) == '.':
		pkg = view.substr(view.word(sel.begin()-1))
		typ = selected
	else:
		pkg = selected

	#pkg could be an alias,
	fpkg = get_full_pkg(imports, pkg)
	#print 'pkg:', pkg, 'typ:', typ, 'fpkg:', fpkg
	
	#check if it's non-std package like "launchpad.net/mgo"
	if re.match('.*?\..*?/.*', fpkg):
		return 'http://gopkgdoc.appspot.com/pkg/' + fpkg + '#' + typ	
	else:
		return 'http://golang.org/pkg/' + fpkg + '/#' + typ




class GoToDocExactCommand(sublime_plugin.TextCommand):
	
	def description(self):
		return 'Open go document exactly base on selected text'

	def run(self, edit):
		sels = self.view.sel()
		for sel in sels:
			sel_txt = self.view.substr(sel).strip()
			if sel_txt == '': continue
			
			if GO_KEYWORDS.has_key(sel_txt):
				doc_url = 'http://golang.org/ref/spec#' + GO_KEYWORDS[sel_txt]	
			elif sel_txt in GO_BUILTINS:
				doc_url = 'http://golang.org/pkg/builtin/#' + sel_txt
			else:
				doc_url = get_pkg_doc_url(self.view, sel)

			webbrowser.open_new_tab(doc_url)


class GoToDocLuckyCommand(sublime_plugin.TextCommand):

	LUCKY_SEARCH_URL="http://google.com/search?btnI=1&q=site:golang.org+"
	
	def description(self):
		return "Search the selected text on golang.org using Google - I'm Feeling Lucky"

	def run(self, edit):
		sels = self.view.sel()
		for sel in sels:
			#print(self.view.substr(sel))
			kw = self.view.substr(sel).strip()
			if kw:
				webbrowser.open_new_tab(self.LUCKY_SEARCH_URL + kw)


class GoToDocTestCommand(sublime_plugin.TextCommand):


	def run(self, edit):
		sels = self.view.sel()
		for sel in sels:
			#print self.view.substr(sel.begin())
			#print self.view.substr(sel.end())
			#print self.view.substr(self.view.word(sel.begin()))
			#print self.view.substr(self.view.word(sel.end()))
			selected = self.view.substr(sel)
			pkg,typ = None, None
			if selected[0].isupper() and self.view.substr(sel.begin()-1) == '.':
				pkg = self.view.substr(self.view.word(sel.begin()-1))
				typ = selected
			else:
				pkg = selected

			#print pkg,typ		



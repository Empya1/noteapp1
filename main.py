import os
from kivymd.app import MDApp
from kivy.lang import Builder 
from kivy.base import EventLoop
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import WipeTransition,FadeTransition, ScreenManager
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.core.clipboard import Clipboard
from kivymd.uix.snackbar import Snackbar

def get_path(fn): 
	return os.path.join(os.path.dirname(__file__), fn)

try: 
	from mysql import Database
	
except: 
	pass

try:
	import shelve
except:
	pass

try:
	from datetime import datetime
except: 
	pass
	
try:
	import random
	
except: 
	pass
	
try:
	from plyer import notification
	
except: 
	pass

try:
	import sqlite3
	
except: 
	pass
	
try:
	from sqlite3 import Error
except: 
	pass

# database class

def snack(txt): 
	try:
		Snackbar(text=str(txt)).open()
		
	except: 
		pass
	

def Notify(title,msg): 
	notification.notify(title=title,message=msg,app_icon=get_path("notification_icon.jpg"))


def alert(txt): 
	toast(gravity=80, y=150, text=str(txt))
	
class MyBs(MDBoxLayout): 
	pass
	
class TransparentBar(MDTopAppBar):
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		self.md_bg_color = 1,1,1, .05
		self.elevation = 0
		#self.theme_cls.theme_style = "Dark"
		
class PwdInput(MDBoxLayout):
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		
	def toggle(self, item): 
		if item.password == True: 
			item.password = False 
		else: 
			item.password = True
		
class IconText(MDBoxLayout): 
	pass
	
class NoteCard(MDCard): 
	pass
	
class NoteViewer(MDCard): 
	pass
	
class MyScreenManager(ScreenManager): 
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		self.transition = FadeTransition()
		self.transition.duration = 0.5
		
class MDTextFieldWithTarget(MDTextField): 
	pass
		

class NoteApp(MDApp): 
	def build(self): 
		self.theme_cls.theme_style = "Dark" 
		self.theme_cls.primary_palette = "Teal"
		self.theme_cls.primary_hue = "400"
		self.theme_cls.material_style = "M2"
		
		self.testing = True
			
		self.path = ("/data/data/org.test.notes/files/app/" if self.testing==False else "")
		
		self.logo = get_path("empya_logo.png")
		
		self.smoke = get_path("smoke.jpg")
		
		self.profont = get_path("profont")
		
		return Builder.load_file("app.kv")
		
	def on_start(self):
				
		try:  
			from android.permissions import request_permissions, Permission
			
			request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
			
		except:  
			alert("Permission request error")
		
				
		try:  
			self.db = Database(get_path("MyNotes"))
			
		except: 
			pass
			
		
		try:
	
			self.root.ids.bottomnav.transition = WipeTransition
			self.root.ids.bottomnav.transition_duration = 0.6
		except: 
			pass
		
		#self.show_notes
		set_bars_colors(
		(0,0,0,.5),
		(0,0,0,.5),
		"Light"
		)
		#create database connection
		
		try: 
			self.db.create_table("Notes", "id INTEGER PRIMARY KEY,", "note_title CHAR,", "note_body TEXT,", "added CHAR,", "img CHAR")
			
		except: 
			alert("Error occured in Database")
		try:	
			#alert("checking notes zero")
			if len(self.db.select_all("Notes")) == 0: 
				self.root.ids.sm2.current = "nonoteview"
				
			else: 
				#alert("switch to noteview")
				self.root.ids.sm2.current = "noteview"
				try:
					#alert("show notes")
					self.show_notes()
				except: 
					pass
				
		except: 
			pass
			
			
		#self.root.ids.sm2.current = "noteview"
		try:
			"""alert("importing shelve file")
			import shelve
			alert("creating shelve file")"""
			self.store = shelve.open(get_path("appData"))
			
		except: 
			alert("unknown error")
			
			
		try:	
			#alert("changing bar1 to m3")
			self.root.ids.bar1.theme_cls.material_style = "M3"
		except: 
			#alert("couldnt changed bar1 to M3")
			pass
		
		try:
			#alert("creating exit dialog")
			self.exit_dialog = MDDialog(
	        title="Do you want to leave", buttons=[
	        MDFlatButton(text="Yes", on_press=lambda x: self.get_running_app().stop()),
	        MDFlatButton(text="No", on_press=lambda x: self.exit_dialog.dismiss())])       
	       
		except: 
			#alert("couldnt create exit dialog")
			pass
			
		try:
			#alert("binding keyboard")
			EventLoop.window.bind(on_keyboard=self.hook)
		except: 
			#alert("couldnt bind keyboard to hook function")
			pass
		
		self.images = ["a.jpg","b.jpg","c.jpg","d.jpg","e.jpg","f.jpg","g.jpeg"]
		
		#self.show_notes()
	
	def confirm_delete(self, note_title,id): 
		self.deldialog = MDDialog(auto_dismiss=False,
		title=f"""Do you want to delete this note titled : {note_title}""",
		buttons=[MDFlatButton(text="Yes", on_press=lambda x: self.remove_note(id)),
        MDFlatButton(text="No", on_press=lambda x: self.deldialog.dismiss())]
		)
		self.deldialog.open()
		
		
		
	def remove_note(self, id): 
		self.db.delete_specific("Notes", ["id", int(id)])
		self.deldialog.dismiss()
		self.show_notes()
		#toast("Note Deleted")
			
		
	def show_notes(self): 
		Notes = self.db.select_all("Notes")
		self.root.ids.rv.data = []
		nice_note = ""
		
		for note in Notes: 
			#print(note)
			limit = 50
			
			if len(note[1]) >= limit: 
				nice_note = note[1][0:limit] + "..."
				
			else: 
				nice_note = note[1]
				
			nice_note = nice_note.title()
			
			self.root.ids.rv.data.append(
			{"viewclass":"NoteCard", 
			 "title": nice_note,
			 "date": note[3],
			 "source":note[4],
			 "pid":str(note[0]),
			 "body":note[2],
			 "actual": note[1]
			 }
			)

		if len(self.db.select_all("Notes")) == 0: 
			self.root.ids.sm2.current = "nonoteview"
			
		else: 
			self.root.ids.sm2.current = "noteview"
		
		note_num = len(self.db.select_all("Notes"))
		self.root.ids.note_count.text = f"Available Notes : {note_num}"
		
	
		
	def hook(self, *args): 
		if args[1] == 27 or args[1] == "27": 
			if self.root.ids.sm.current == "Login":
				self.exit_dialog.open()
				
			elif self.root.ids.sm.current == "Main":			
				self.exit_dialog.open()
				
			elif self.root.ids.sm.current == "Opennote": 
				self.root.ids.sm.current = "Main"
				
			elif self.root.ids.sm.current == "edit": 
				self.root.ids.sm.current = "Main"
				
			elif self.root.ids.sm.current == "changepwd": 
				self.root.ids.sm.current = "Main"
				
			elif self.root.ids.sm.current == "credits": 
				self.root.ids.sm.current = "Main"
				
			
			
		return True
		
	def set_login_or_login(self, name, pwd): 
	
		if name == "" or len(name)== 0 or len(pwd) == 0 or pwd == "": 
			return True
			
		#if name != self.store["name"]: 
			#alert("check your input")
#			return True
	
		try: 
			if name == self.store["name"] and pwd == self.store["pwd"]: 
				self.root.ids.sm.current = "Main"
				
			else: 
				try:
					alert("password or username incorrect")
				except: 
					pass
				
		except: 
			try:
				self.store["name"] = name 
				self.store["pwd"] = pwd
				alert("password and username set")
				Notify("Username and Password Set","You may now login")
				snack("Enter the password you just set")
			except: 
				if self.storage_access == False:
					try:
						alert("Storage Permission Needed")
					except: 
						pass
			
					
				else:
					alert("Couldn't set password")
				
		self.root.ids.username.text = ""
		self.root.ids.password.ids.mtf.text = ""
				
	def save_note(self, title,body): 
		#alert(str("%s : %s"%(title.text,body.text)))
		
		
		time_obj = datetime.now()
		date_and_time = time_obj.strftime("%d %b %Y | %H:%M")
		
		img = random.choice(self.images)
		
		id = 0
		
		all_ids = self.db.get_column("Notes", "id")
		
		try:
		
			if all_ids == 0:
				id = 0
				
			else: 
				id = max(all_ids)[0] +1
				
		except: 
			id = 0
			
		if title.text == "" or title.text == " ": 
			alert("Title cannot be empty")
			return True
			
		
		txt = str(body.text)
		#alert(txt)
		
			
		self.db.insert("Notes", [(id, str(title.text), txt, date_and_time, get_path(img))])
		
		if len(self.db.select_all("Notes")) == 0: 
			self.root.ids.sm2.current = "nonoteview"
			
		else: 
			self.root.ids.sm2.current = "noteview"
			
		self.show_notes()
		alert("Note Saved")
		self.root.ids.bottomnav.switch_tab("view")
		
		self.root.ids.notebody.text = ""
		self.root.ids.notetitle.text = ""
		
	
	def delnote(self, id,title): 
		id = int(id)  
		self.confirm_delete(title, id)
		
	def show_content(self, title, body, date,actual):
		self.root.ids.nv.title = actual
		self.root.ids.nv.date = date 
		
		if body == "":
			self.root.ids.nv.content = "No Content"
			
		else: 
			outp = body
			self.root.ids.nv.content  = outp.replace("\\n","\n")
 
			
		self.root.ids.sm.current = "Opennote"
		
	def edit_note(self, id,title,body): 
	
		self.root.ids.edititle.text = str(title)
		#alert(body)
		self.root.ids.editbody.text = body.replace("\\n", "\n")
		self.root.ids.editbody.target = str(id)
		self.root.ids.sm.current = "edit"
		
	def save_changes(self, newtitle, newbody, targetid): 
		
		if newtitle == "" or newtitle== " ": 
			alert("Title cannot be empty")
			return True
			
		try:
		
			self.db.update("Notes", ("id", int(targetid)), [("note_title",newtitle), ("note_body",newbody)])
		
			alert("Changes Saved")
			
		except: 
			alert("Failed to alter note")
	
		self.show_notes()
		self.root.ids.sm.current = "Main"
		
	def changepwd(self, old_pwd, new_pwd, conf_pwd): 
		##print((item.ids.mtf.text))
		if old_pwd.ids.mtf.text == "" or new_pwd.ids.mtf.text == "" or conf_pwd.ids.mtf.text == "": 
			alert("Please Fill In All The Fields")
			return True
			
		else: 
			if old_pwd.ids.mtf.text == self.store["pwd"] and new_pwd.ids.mtf.text == conf_pwd.ids.mtf.text: 
				self.store["pwd"] = new_pwd.ids.mtf.text
				alert("Password Changed Successfully")
				
				Notify("Password Changed Successfully", "You have successfully changed your login password")
				
				self.root.ids.sm.current = "Login"
			else: 
				alert("Please check your input and try again")
		
	def clear_notes(self):  
		
		self.delalldialog = MDDialog(auto_dismiss=False,
		title="Do you want to clear all notes",
		buttons=[MDFlatButton(text="Yes", on_press=lambda x: self.clear()),
        MDFlatButton(text="No", on_press=lambda x: self.delalldialog.dismiss())]
		)
		self.delalldialog.open()
		
	def clear(self): 
		try: 
			self.db.delete_all("Notes")
			alert("All Notes Cleared")
			
		except: 
			alert("Deletion Failed")
			
		finally: 
			self.show_notes()
			self.delalldialog.dismiss()
			
	def show_credit(self): 
		pass
		
	def copy_note(self, txt): 
		try: 
			txt = txt.replace("\\n", "\n")
			Clipboard.copy(txt)
			alert("Content copied to clipboard")
			
		except: 
			alert("Failed to copy content")
		
if __name__ == "__main__": 
	NoteApp().run()
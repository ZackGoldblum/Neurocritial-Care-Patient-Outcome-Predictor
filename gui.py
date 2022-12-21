# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 14:41:34 2022

@authors: Zack Goldblum, Josh Miller, Kevin Ramirez Chavez
"""

import wx
import os
import sqlite3
from similarity_search import similarity_search
import sys
from bmes import tempdir

# Load unique medications into list for autocomplete

sql_filepath_pharm = os.path.join(tempdir(), "final_project_sql", "pharmacy_unique.sqlite")
unique_pharm_db = sqlite3.connect(sql_filepath_pharm)
cur = unique_pharm_db.cursor()
cur.execute('''SELECT medication_unique FROM pharmacy_unique''')
rows = cur.fetchall()
unique_pharm_db.close()
unique_meds = [row[0] for row in rows]

# Load unique icd codes into list for autocomplete

sql_filepath_icd = os.path.join(tempdir(), "final_project_sql", "d_icd_diagnoses.sqlite")
unique_icd_db = sqlite3.connect(sql_filepath_icd)
cur = unique_icd_db.cursor()
cur.execute('''SELECT icd_code FROM d_icd_diagnoses''')
rows = cur.fetchall()
unique_icd_db.close()
unique_icds = [row[0] for row in rows]

class GUIFrame ( wx.Frame ):
	"""
	GUI layout and functionality 
	"""
	
	def __init__(self, *args, **kw):
		super(GUIFrame, self).__init__(*args, **kw, title = "BMES 550 Group 24 | Neurocritical Care Patient Outcome Prediction", pos = wx.DefaultPosition, size = wx.Size( 600,360 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		main_sizer = wx.BoxSizer( wx.VERTICAL )

		self.patient_dict = {"age": None, "gender": None, "medication": [], "first_careunit": [], "icd_code": None}

		# patient -----
		
		patient_sizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, "Patient Information" ), wx.VERTICAL )
		patient_age_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.age_text = wx.StaticText( patient_sizer.GetStaticBox(), wx.ID_ANY, "Age:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.age_text.Wrap( -1 )
		patient_age_sizer.Add( self.age_text, 0, wx.ALL, 5 )
		self.age_input = wx.TextCtrl( patient_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		patient_age_sizer.Add( self.age_input, 0, wx.ALL, 5 )
		patient_sizer.Add( patient_age_sizer, 1, wx.EXPAND, 5 )
		
		patient_gender_sizer = wx.BoxSizer( wx.HORIZONTAL )
		self.gender_text = wx.StaticText( patient_sizer.GetStaticBox(), wx.ID_ANY, "Sex:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.gender_text.Wrap( -1 )
		patient_gender_sizer.Add( self.gender_text, 0, wx.ALL, 5 )
		gender_selectChoices = [ "M", "F" ]
		self.gender_select = wx.ComboBox( patient_sizer.GetStaticBox(), wx.ID_ANY, "M", wx.DefaultPosition, wx.DefaultSize, gender_selectChoices, 0 )
		self.gender_select.SetSelection( 0 )
		patient_gender_sizer.Add( self.gender_select, 0, wx.ALL, 5 )
		patient_sizer.Add( patient_gender_sizer, 1, wx.EXPAND, 5 )
		
		patient_med_sizer = wx.BoxSizer( wx.HORIZONTAL )
		self.med_text = wx.StaticText( patient_sizer.GetStaticBox(), wx.ID_ANY, "Medication:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.med_text.Wrap( -1 )
		patient_med_sizer.Add( self.med_text, 0, wx.ALL, 5 )
		self.med_input = wx.TextCtrl( patient_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 233,-1 ), 0 )
		self.med_input.AutoComplete(MyClassCompleter(unique_meds))
		patient_med_sizer.Add( self.med_input, 0, wx.ALL, 5 )
		self.med_text2 = wx.StaticText( patient_sizer.GetStaticBox(), wx.ID_ANY, "*leave blank if no medication", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.med_text2.Wrap( -1 )
		patient_med_sizer.Add( self.med_text2, 0, wx.ALL, 5 )
		patient_sizer.Add( patient_med_sizer, 1, wx.EXPAND, 5 )
		
		main_sizer.Add( patient_sizer, 1, wx.EXPAND, 5 )

		# injury -----
	
		injury_sizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, "Injury Information" ), wx.VERTICAL )	
		injury_unit_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.unit_text = wx.StaticText( injury_sizer.GetStaticBox(), wx.ID_ANY, "First care unit:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.unit_text.Wrap( -1 )
		injury_unit_sizer.Add( self.unit_text, 0, wx.ALL, 5 )
		unit_selectChoices = [ "Medical Intensive Care Unit", "Surgical Intensive Care Unit", "Medical/Surgical Intensive Care Unit", "Cardiac Vascular Intensive Care Unit", "Coronary Care Unit", "Trauma Surgical Intensive Care Unit", "Neuro Intermediate", "Neuro Stepdown", "Neuro Surgical Intensive Care Unit", "Coronary Care Unit" ]
		self.unit_select = wx.ComboBox( injury_sizer.GetStaticBox(), wx.ID_ANY, "Medical Intensive Care Unit", wx.DefaultPosition, wx.DefaultSize, unit_selectChoices, 0 )
		self.unit_select.SetSelection( 0 )
		injury_unit_sizer.Add( self.unit_select, 0, wx.ALL, 5 )
		injury_sizer.Add( injury_unit_sizer, 1, wx.EXPAND, 5 )
		
		injury_icd_sizer = wx.BoxSizer( wx.HORIZONTAL )
		self.icd_text = wx.StaticText( injury_sizer.GetStaticBox(), wx.ID_ANY, "Diagnosis ICD code:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.icd_text.Wrap( -1 )
		injury_icd_sizer.Add( self.icd_text, 0, wx.ALL, 5 )
		self.icd_input = wx.TextCtrl( injury_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.icd_input.AutoComplete(MyClassCompleter(unique_icds))
		injury_icd_sizer.Add( self.icd_input, 0, wx.ALL, 5 )
		self.icd_text2 = wx.StaticText( injury_sizer.GetStaticBox(), wx.ID_ANY, "*leave blank if no diagnosis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.icd_text2.Wrap( -1 )
		injury_icd_sizer.Add( self.icd_text2, 0, wx.ALL, 5 )
		injury_sizer.Add( injury_icd_sizer, 1, wx.EXPAND, 5 )
		
		main_sizer.Add( injury_sizer, 1, wx.EXPAND, 5 )

		# buttons -----

		buttons_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.submit_button = wx.Button( self, wx.ID_ANY, "Submit all", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.submit_button.Bind(wx.EVT_BUTTON, self.handle_submit_press)
		buttons_sizer.Add( self.submit_button, 0, wx.ALL, 5 )
		self.reset_button = wx.Button( self, wx.ID_ANY, "Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.reset_button.Bind(wx.EVT_BUTTON, self.handle_reset_press)
		buttons_sizer.Add( self.reset_button, 0, wx.ALL, 5 )
		
		main_sizer.Add( buttons_sizer, 1, wx.EXPAND, 5 )

		# results -----
		
		results_sizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, "Results" ), wx.VERTICAL )
		self.results_text = wx.StaticText( results_sizer.GetStaticBox(), wx.ID_ANY, "Press 'Submit all' to get results.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.results_text.Wrap( -1 )
		results_sizer.Add( self.results_text, 0, wx.ALL, 5 )
		main_sizer.Add( results_sizer, 1, wx.EXPAND, 5 )
		
		self.SetSizer( main_sizer )
		self.Layout()		
		self.Centre( wx.BOTH )

		self.status_bar = self.CreateStatusBar()

	def handle_submit_press(self, evt):
		"""
		Called when the submit button is pressed
		"""
		
		self.update_all_vals()
		if self.check_all_vals():
			dialog = wx.ProgressDialog('Patient survival rate calculation in progress.', 'Please wait...')
			survival_rate = self.get_patient_results()
			wx.CallAfter(dialog.Destroy)
			self.update_results(survival_rate)

	def handle_reset_press(self, evt):
		"""
		Called when the reset button is pressed
		"""

		self.age_input.Clear()
		self.gender_select.SetSelection( 0 )
		self.med_input.Clear()
		self.unit_select.SetSelection( 0 )
		self.icd_input.Clear()
		self.results_text.SetLabel("Press 'Submit all' to get results.")
		self.update_status_bar("")

	def update_all_vals(self):
		"""
		Update the patient dictionary with the current values from the GUI
		"""

		self.patient_dict["age"] = self.age_input.GetValue()
		self.patient_dict["gender"] = self.gender_select.GetStringSelection()
		self.patient_dict["medication"] = self.med_input.GetValue()
		self.patient_dict["first_careunit"] = self.unit_select.GetStringSelection()
		self.patient_dict["icd_code"] = self.icd_input.GetValue()

	def check_all_vals(self):
		"""
		Check that the user input correct values
		"""

		if not self.patient_dict["age"].isnumeric():
			self.update_status_bar("ERROR: Enter a valid age (integer).")
			return None
		else:
			self.update_status_bar("")
			return True

	def get_patient_results(self):
		"""
		Calls the similarity_search function to determine the survival rate of similar patients
		"""
		
		survival_rate, _ = similarity_search(int(self.patient_dict["age"]), self.patient_dict["gender"], self.patient_dict["medication"], self.patient_dict["first_careunit"], self.patient_dict["icd_code"])
		return survival_rate

	def update_results(self, survival_rate):
		"""
		Update the results with the survival rate
		"""
		
		self.results_text.SetLabel(f"{survival_rate}% of the most similar patients survived.")

	def update_status_bar(self, message):
		"""
		Display messages on the status bar
		"""
		
		self.status_bar.SetStatusText(message)

class MyClassCompleter(wx.TextCompleter):
	"""
	Implements autocomplete functionality to text input boxes

	Modified from https://wiki.wxpython.org/How%20to%20create%20a%20text%20control%20with%20autocomplete%20%28Phoenix%29
	"""
	
	def __init__(self, unique_list):
		wx.TextCompleter.__init__(self)
		self._iLastReturned = wx.NOT_FOUND
		self._sPrefix = ''
		self._unique_list = unique_list

	def Start(self, prefix):
		self._sPrefix = prefix.lower()
		self._iLastReturned = wx.NOT_FOUND
		for item in self._unique_list:
			try:
				if item.lower().startswith(self._sPrefix):
					return True
			except AttributeError:
				pass
		# Nothing found
		return False

	def GetNext(self):
		for i in range(self._iLastReturned+1, len(self._unique_list)):
			try:
				if self._unique_list[i].lower().startswith(self._sPrefix):
					self._iLastReturned = i
					return self._unique_list[i]
			except AttributeError:
				pass
		# No more corresponding itemd
		return ""
	
def main():
	"""
    Run the GUI
	"""

	app = wx.App()
	frame=GUIFrame(None)
	frame.Show()
	frame.RequestUserAttention()
	app.MainLoop()
	del app

if __name__ == '__main__':
    main()
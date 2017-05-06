from locust import HttpLocust, TaskSet, task
from pyquery import PyQuery
import random
import names

class WebsiteTasks(TaskSet):
	def on_start(self):
		self.client.post("/login", {
			"username": "ascour01",
			"password": "wellness"})
		self.patients = []
		r = self.client.post("/index", {"keyword":""})
		pq = PyQuery(r.content)
		elems = pq('th p a')
		self.patients = [link.attrib["href"] for link in elems]

	@task
	def index(self):
		self.client.get("/")
		
	@task
	def get_patient(self):
		try:
			patient = random.choice(self.patients)
			r = self.client.get(patient)
			pq = PyQuery(r.content)
			elems = pq('#edit')
			self.to_edit = [link.attrib["href"] for link in elems]
		except IndexError:
			self.client.get('/patient_data/1/1')
			
	#@task(10)
	#def create_patient(self):
	#	self.client.post('/new_patient', {
	#		"name": names.get_full_name(),
	#		"DOB": "{}/{}/{}".format(random.randint(1,12), random.randint(1,25), random.randint(1950, 2016)),
	#		"hx": "none",
	#		"phone_number": str(random.randint(1000000000, 9999999999)),
	#		"address": "nowhere",
	#		"visit_date": "05/02/2017",
	#		"visit_doctor": "Dr. Eads",
	#		"visit_notes": "randomly generated",
	#		"patient_note": "eat an apple"})

	#@task(10)
	#def update_patient(self):
	#	try:
	#	self.client.post('/update_patient', {
	#		"name": names.get_full_name(),
	#		"DOB": "{}/{}/{}".format(random.randint(1,12), random.randint(1,25), random.randint(1950, 2016)),
	#		"hx": "none",
	#		"phone_number": str(random.randint(1000000000, 9999999999)),
	#		"address": "nowhere",
	#		"visit_date": "05/02/2017",
	#		"visit_doctor": "Dr. Eads",
	#		"visit_notes": "randomly generated",
	#		"patient_note": "eat an apple"})
			
	#	except:
	#		pass

class WebsiteUser(HttpLocust):
	task_set = WebsiteTasks
	min_wait = 10000
	max_wait = 60000

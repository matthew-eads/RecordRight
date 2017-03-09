# RecordRight
## Project Proposal:

Brief summary: We will implement an electronic medical record (EMR) system that is designed for developing regions. It will be served locally from a cheap computer in a hospital/clinic as a web page so that it is accessible from any device with a web browser/access to the local network. 

Why this is important:
Most hospitals and clinics use paper health records, which are typically disorganized and can easily be lost, misplaced, destroyed, and are difficult to sort through1,2,3,4
Health records are a vital aspect to providing the best care to a patient because:
Seeing past illnesses and conditions can help doctors find correlations between symptoms in the case of long-term diseases/conditions4
Having access to the family history of patients allows doctors to consider the individual’s predispositions to various illnesses/conditions4
Being able to view the allergies/pre-existing conditions of a patient can allow doctors to prescribe medication and treatment more safely4
In developing regions, it is critical for hospital and clinic staff to know what resources are available at any given time and how many patients may need to use them, so there are no drug shortages -- EMR systems allow clinicians to easily keep track of medications and resources and account for patient need and demand1
Existing solutions/problems:1,2,3,4
Numerous products for recording medical records exist but they are…
Unreliable - rely on poor internet connection, buggy, etc.
Inaccessible - few devices with the software installed, or few devices exist for the doctors
Inflexible - software doesn’t track data workers would like to track, lacks ability to be easily expanded to do so
Hard to use - for those with low computer literacy, poor user interfaces and other challenges make the systems hard to use and a burden rather than a help; trainings for the software are costly and take time away from clinicians
How we’ll improve on these:
Make the software fully tolerant of poor internet connections, allowing the full service to be served locally without any internet connection. Also add inter-hospital data sharing/synchronization using principles from DTN, KioskNet, etc.
By serving as a simple web page, workers can access it from any computer or smartphone
A mobile application or mobile-friendly web page, which would be served over the local network so that clinicians can access the EMR system without needing to go to a computer
Allow for workers to easily add new fields to a medical record so that the software is easily expandable and adaptable
Allows patients to view aspects of their medical record through a SMS interface, and also edit some fields (address, phone number, etc). 
Keep the UI as simple and as streamlined as possible to make it easy to use for those with low computer literacy.
If time allows, include voice functionality to patient SMS and clinician mobile side 
Challenges:
Understanding how we can best utilize messaging and phone apps to allow the user to quickly and easily update medical records from their mobile phone
Successfully emulating an environment where there is only an intermittent Internet link and power outages are possible at any moment
Successfully handling data transmission when a link is interrupted (e.g. if the power goes out, if there’s a bad connection, etc)
Ensuring that the system is quick to access so that doctors aren’t dissuaded from using it, but not compromising functionality and security
Potential tools:
Emulab, a tool used to emulate intermittent links and low bandwidth
Org.json, an Android JSON API that would be used if we create a mobile Android application
MySQL database (subject to change)
Evaluation Plan:
We’ll use Emulab to test how the system handles various types of connections (low bandwidth, delays, etc.); amount of data successfully transferred in a given amount of time will serve as a metric for success
The web interface and texting application will be mostly evaluated based on what features we are able to provide. Any texting/phone app will also be evaluated based on how its functionality compares to the web interface, and how easy/quick it is to accomplish tasks via phone instead of via computer
Students will be asked to use the system and evaluate its ease of navigation and usability; additionally, we may ask a physician we know who does work in rural Uganda to review it
Work division:
One person is primarily in charge of their assigned component, but others may help:
Azmina -- Web interface and layout with mobile interface (probably for Android), building the database
Matt -- setting up the intranet system, delay tolerant link, and testing the link
Ari -- creating the system to allow patients to access medical information through SMS; additional research
Milestones:
Mid March -- further research into all aspects of the project should be completed by this point (including pin-pointing exact features, identifying all APIs, etc.), along with a wireframe design concept for the web and mobile interfaces, and a structural concept for the database and network system
End of March/beginning of April -- basic webpage should function with a rudimentary database; should be able to successfully alter database from mobile phone; delay tolerant link should mostly work
Mid April --  corner cases should be addressed; interruption of data transmission should be handled; testing of systems should be completed; interface should be refined; security measures should be addressed, if time
End of April/beginning of May -- project should be completed and ready to present! Additional features, such as voice-to-text data entry and more intense security measures may be employed by now, time-permitting


Sources:
Fraser, H., Biondich, P., Moodley, D., Choi, S., Mamlin, B., & Szolovits, P. (2005). Implementing electronic medical record systems in developing countries. Journal of Innovation in Health Informatics, 13(2), 83-95.
Kahouei, M., Zadeh, J. M., & Roghani, P. S. (2015). The evaluation of the compatibility of electronic patient record (EPR) system with nurses’ management needs in a developing country. International journal of medical informatics, 84(4), 263-270.
Ohuabunwa, E. C., Sun, J., Jubanyik, K. J., & Wallis, L. A. (2016). Electronic Medical Records in low to middle income countries: the case of Khayelitsha Hospital, South Africa. African Journal of Emergency Medicine, 6(1), 38-43.
Sikhondze, N. C., & Erasmus, L. Electronic Medical Records: A Developing and Developed Country Analysis.






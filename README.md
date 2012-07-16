6th June, 12
Basic Tabs done. 
Please take care of the different settings that need for dajax to run.
Dont use 'shaastra' as your project folder's name. Dajax was not accepting hyphens for some reason. My folder's name is 'shaastra'.
If you have a different name please change 'Dajaxice.shaastra.events.<some_func>' to 'Dajaxice.<your_project_folder>.events.<some_func>' in all the templates. 
Dont forget to add AUTH_PROFILE_MODULE = 'events.UserProfile' to your local settings.

9th June, 12
Tab files added. they have add, delete functionality.
sending file uses ajax. rest can be done by dajax.
Renaming files has to be done.

15th June, 12 Renaming of files done

16th June, Chosen-JQuery plugin implemented in the form for adding events. 'Tags' for events can now be added in a more presentable way.

25th June, Coords can now add questionnares. He/She can choose to add an mcq or a subjective. After adding an mcq, he/she can add choices for it. editing/deleting of options/questions can be done.
As suggested by Suraj, I have made some changes so that you dont need to name your project folder as 'shaastra'. I have added some lines to global_settings.py and added a file called context_processors.py. So in templates just use {{pro_dir}} instead of 'shaastra' now, and your folder name will get rendered there. Just add the following line as it is in your TEMPLATE_CONTEXT_PROCESSORS - "events.context_processors.project_dir_name".

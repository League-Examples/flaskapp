# Demo Application 

The demo application is implemented in the blueprint 'demo', 
rooted at '/demo/'. It has these routes: 

'/demo/index.html': Lists the other demo pages. 
'/demo/hello.html': A simple page that says hello and displays the flag.png image.
'/demo/form.html': A form that accepts a name and displays a greeting.

Extend `base/page.html` 

 We are using bootstrap-flask, and font-awesome-flask for the UI. Ensure that these are setup properly in application creation. 

Forms are implemented using Flask-WTF.